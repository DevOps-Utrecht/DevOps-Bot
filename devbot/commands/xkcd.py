""" Latest XKCD command. """
from sqlalchemy import or_
import discord
import devbot.database as db
from devbot.registry import Command
from devbot.tools import api_requests as API


def embed(title, image_url) -> discord.Embed:
    result = discord.Embed()
    result.title = title
    result.set_image(url=image_url)
    return result

@Command(["xkcd"])
async def xkcd(message_contents, *_args, **_kwargs) -> (str, discord.Embed):
    url = "https://xkcd.com/info.0.json"  # latest XKCD

    if message_contents:
        # specifiying a nr results in that # comic being returned
        if len(message_contents) == 1:
            if message_contents[0].split() == [c for c in message_contents if c.isdigit()]:
                url = f"https://xkcd.com/{message_contents[0]}/info.0.json"

        # adding anything else queries the database
        query = f"%{' '.join(message_contents)}%"
        session = db.Session()
        entry = session.query(db.XKCD).filter(or_(db.XKCD.title.like(query),
                                                  db.XKCD.alt.like(query),
                                                  db.XKCD.transcript.like(query),
                                                  )).first()
        session.close()
        if entry:
            return embed(entry.safe_title, entry.img)

    # retrieve comic meta data
    try:
        xkcd_json = await API.get_json(url)
    except API.APIAccessError:
        return "Comic not found."

    # add comic meta data to database
    session = db.Session()
    entry = db.XKCD(**xkcd_json)
    session.merge(entry)
    session.commit()

    return embed(xkcd_json.get("safe_title"), xkcd_json['img'])
