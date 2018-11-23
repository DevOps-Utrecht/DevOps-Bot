""" Doodle link """
import devbot.database as db
from devbot.registry import Command, Keyword


@Keyword(["https://doodle.com/poll/"])
async def doodle_url(message_contents, *_args, **_kwargs):
    """ Called when a message contains a Doodle poll URL and saves it to the database. """
    doodle_url = [i for i in message_contents if "https://doodle.com/poll/" in i][0]

    session = db.Session()
    session.merge(db.Doodle(url=doodle_url, deadline=None))
    session.commit()

    return "Doodle registered"


@Command(["doodle"])
async def doodle(*_args, **_kwargs):
    """ Return the last registered Doodle URL. """
    session = db.Session()
    entry = session.query(db.Doodle).order_by(db.XKCD.id.desc()).first())  # last is backwards first
    session.close()
    if entry:
        return entry.value
    else:
        return "No Doodle found"
