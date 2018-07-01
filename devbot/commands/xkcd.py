""" xkcd comic command. """
import random
import discord
from sqlalchemy import or_

import devbot.database as db
from devbot.registry import Command
from devbot.tools import api_requests


def embed(title, image_url) -> discord.Embed:
    """ Build an Embed with the given image URL. """
    result = discord.Embed()
    result.title = title
    result.set_image(url=image_url)
    return result


@Command(["xkcd"])
async def xkcd(message_contents, *_args, **_kwargs) -> str or discord.Embed:
    """ Returns a xkcd comic """
    url = "https://xkcd.com/info.0.json"  # latest xkcd

    if message_contents:
        if len(message_contents) == 1:
            # return comic by number
            if all(map(str.isdigit, message_contents[0].strip())):
                url = f"https://xkcd.com/{message_contents[0]}/info.0.json"

            # return random comic
            elif message_contents[0].strip() == "?":
                try:
                    # most recent comic from url
                    xkcd_json = await api_requests.get_json(url)
                    max_id = xkcd_json["num"]
                except api_requests.APIAccessError:
                    # most recent comic from database
                    session = db.Session()
                    entry = (
                        session.query(db.XKCD).order_by(db.XKCD.id.desc()).first()
                    )  # last is backwards first
                    session.close()
                    max_id = entry.num
                random_id = random.randint(1, max_id)
                url = f"https://xkcd.com/{random_id}/info.0.json"

            # search the database
            else:
                session = db.Session()
                query = f"%{' '.join(message_contents)}%"
                entry = (
                    session.query(db.XKCD)
                    .filter(
                        or_(
                            db.XKCD.title.like(query),
                            db.XKCD.transcript.like(query),
                            db.XKCD.alt.like(query),
                        )
                    )
                    .first()
                )
                session.close()
                if entry:
                    return embed(entry.safe_title, entry.img)

    # retrieve comic meta data from url
    try:
        xkcd_json = await api_requests.get_json(url)
    except api_requests.APIAccessError:
        return "Comic not found."

    # add comic meta data to database
    session = db.Session()
    entry = db.XKCD(**xkcd_json)
    session.merge(entry)
    session.commit()

    return embed(xkcd_json.get("safe_title"), xkcd_json["img"])
