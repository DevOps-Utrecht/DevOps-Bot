""" A helper tool to delay messages or schedule messages """

import os
import pickle
import datetime
import logging
import queue
import discord
import dotenv
import devbot.database as db
from devbot.tools.wrap import FileWrapper

# Load dotenv
dotenv.load_dotenv(".env")
# Get id of default channel
DEFAULT_CHANNEL = os.environ.get("REMINDER_CHANNEL")


LOGGER = logging.getLogger(__name__)
TASK_QUEUE = queue.PriorityQueue()


async def delay_message(
    delay, message, channel=None
):
    """ Returns the message after delay or, if delay is of type datetime/time at that time. """
    if channel is None:
        if DEFAULT_CHANNEL:
            channel = discord.Object(id=DEFAULT_CHANNEL)
        else:
            raise ValueError(f"Default channel not set, channel cannot be None")

    # If delay is a datetime return at given time
    if isinstance(delay, datetime.datetime):
        if delay < datetime.datetime.now():
            return "Time is in the past dummy."
        return await schedule(message, channel, delay)
    # If delay is time return at time on same date
    elif isinstance(delay, datetime.time):
        if delay < datetime.datetime.now().time():
            return "Time is in the past dummy."
        return await schedule(
            message, channel, datetime.combine(datetime.date.today(), delay)
        )
    # If delay is timedelta
    elif isinstance(delay, datetime.timedelta):
        dt = datetime.datetime.now() + delay
        return await schedule(message, channel, dt)
    # If we get an int take it as seconds
    elif isinstance(delay, int):
        if delay < 0:
            return "I cant delay into the past dummy."
        dt = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        return await schedule(message, channel, dt)
    else:
        raise ValueError(
            f"Delay ({delay}) is of an unsupported type. Only datetime, time, "
            f"deltatime and int are supported"
        )


async def schedule(message, channel, date_time):
    """ Schedules a specific event. """
    if isinstance(message, str):
        ret_type = db.ReturnType.string
        val = message
    elif isinstance(message, discord.Embed):
        ret_type = db.ReturnType.embed
        val = pickle.dumps(message)
    elif isinstance(message, FileWrapper):
        ret_type = db.ReturnType.file
        val = message.name
    else:
        raise ValueError(
            f"The return type: {typeof(message)} is unsupported at this time."
        )

    session = db.Session()
    entry = db.Task(
        datetime=date_time, channel=channel.id, type=ret_type, value=val,
        executed=False
    )
    LOGGER.info(f"Adding task {entry} to the scheduled db.")
    session.add(entry)  # Add entry to the database
    session.flush()  # Flush to enforce id assignment
    t_id = entry.id  # Catch entry id
    session.commit()  # Commit changes

    LOGGER.info(f"Adding task ({t_id}, {date_time}, {channel},  {message}) to the "
                f"queue.")
    TASK_QUEUE.put((date_time.timestamp(), t_id, message, channel))
    return


def schedule_from_database():
    """ Constructs a priority Queue from the task database table. """
    session = db.Session()
    entries = session.query(db.Task).filter(db.Task.executed == False).all()
    session.close()
    for entry in entries:
        ts = entry.datetime.timestamp()
        chan = discord.Object(id=entry.channel)
        ret_type = entry.type
        val = entry.value

        if ret_type == db.ReturnType.string:
            ret_val = val
        elif ret_type == db.ReturnType.file:
            ret_val = FileWrapper(val)
        elif ret_type == db.ReturnType.embed:
            ret_val = pickle.loads(val)

        TASK_QUEUE.put((ts, entry.id, ret_val, chan))
