""" A helper tool to delay messages or schedule messages """

import os
import logging
import datetime
import discord
import dotenv
from devbot.bot import SCHEDULER, send_response

# Load dotenv
dotenv.load_dotenv(".env")

# Get id of default channel
DEFAULT_CHANNEL = os.environ.get("REMINDER_CHANNEL")

LOGGER = logging.getLogger(__name__)


async def schedule_message(delay, message, channel=None):
    """ Schedules the message on DateTime entered. """
    if channel is None:
        if DEFAULT_CHANNEL:
            channel = discord.Object(id=DEFAULT_CHANNEL)
        else:
            raise ValueError(
                f"Default channel not set, add REMINDER_CHANNEL=<id> to the .env file"
            )
    dt = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    job = SCHEDULER.add_job(
        send_response, trigger="date", run_date=dt, args=[message, channel]
    )


async def delay_message(delay, message, channel=None):
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
        job = SCHEDULER.add_job(
            send_response, trigger="date", run_date=delay, args=[message, channel]
        )
        return
    # If delay is time return at time on same date
    elif isinstance(delay, datetime.time):
        if delay < datetime.datetime.now().time():
            return "Time is in the past dummy."
        dt = datetime.combine(datetime.date.today(), delay)
        job = SCHEDULER.add_job(
            send_response, trigger="date", run_date=dt, args=[message, channel]
        )
        return
    # If delay is timedelta
    elif isinstance(delay, datetime.timedelta):
        dt = datetime.datetime.now() + delay
        job = SCHEDULER.add_job(
            send_response, trigger="date", run_date=dt, args=[message, channel]
        )
        return
    # If we get an int take it as seconds
    elif isinstance(delay, int):
        if delay < 0:
            return "I cant delay into the past dummy."
        dt = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        job = SCHEDULER.add_job(
            send_response, trigger="date", run_date=dt, args=[message, channel]
        )
        return
    else:
        raise ValueError(
            f"Delay ({delay}) is of an unsupported type. Only datetime, time, "
            f"deltatime and int are supported"
        )
