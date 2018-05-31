""" A helper tool to delay messages or schedule messages """

import asyncio
import datetime
import logging

LOGGER = logging.getLogger(__name__)


async def delay_message(delay, message):
    """ Returns the message after delay or, if delay is of type datetime/time at that time. """
    # If delay is a datetime return at given time
    if isinstance(delay, datetime.datetime):
        if delay < datetime.datetime.now():
            return "Time is in the past dummy."
        delta = delay - datetime.datetime.now()
        seconds = delta.total_seconds()
        LOGGER.debug(f"Scheduled to return {message} at {delay}")
        await asyncio.sleep(seconds)
        LOGGER.debug(f"Returning {message} after {delay}")
        return message
    # If delay is time return at time on same date
    elif isinstance(delay, datetime.time):
        if delay < datetime.datetime.now().time():
            return "Time is in the past dummy."
        delta = delay - datetime.datetime.now().time()
        seconds = delta.total_seconds()
        LOGGER.debug(f"Scheduled to return {message} at {delay}")
        await asyncio.sleep(seconds)
        LOGGER.debug(f"Returning {message} after {delay}")
        return message
    # If delay is timedelta
    elif isinstance(delay, datetime.timedelta):
        seconds = delay.total_seconds()
        LOGGER.debug(f"Scheduled to return {message} after {seconds} seconds")
        await asyncio.sleep(seconds)
        LOGGER.debug(f"Returning {message} after {seconds} seconds")
        return message
    # If we get an int take it as seconds
    elif isinstance(delay, int):
        if delay < 0:
            return "I cant delay into the past dummy."
        LOGGER.debug(f"Scheduled to return {message} after {delay} seconds")
        await asyncio.sleep(delay)
        LOGGER.debug(f"Returning {message} after {delay} seconds")
        return message

    raise ValueError(f"Delay ({delay}) is of a none supported type. Only datetime, time, deltatime and int are "
                     f"supported")
