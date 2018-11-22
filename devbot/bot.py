"""
    Main entry point for devbot.
"""

import logging
import os

import discord
import dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import devbot.commands
from devbot.database import DB_URL
from devbot.registry import COMMAND_DICT, KEYWORD_DICT, safe_call, CommandNotFoundError
from devbot.tools.wrap import FileWrapper

CLIENT = discord.Client()
#: The main discord client.
LOGGER = logging.getLogger(__name__)
#: An Easy_logger instance.
SYMBOL = "!"
#: The command symbol

# Jobstore
JOBSTORES = {"default": SQLAlchemyJobStore(url=DB_URL)}

# Setup apscheduler
SCHEDULER = AsyncIOScheduler(jobstores=JOBSTORES)


@CLIENT.event
async def on_ready():
    """ Log bot info. """
    LOGGER.info("Bot logged is as: %s, with id: %s.", CLIENT.user.name, CLIENT.user.id)


@CLIENT.event
async def on_message(message):
    """ Process incoming message. """
    if message.author == CLIENT.user:
        return  # Prevent any self-activation.

    response = None

    if message.content.startswith(SYMBOL):
        # Split message into command and list of the remainder.
        message_command, *message_contents = message.content.split()

        try:
            response = await safe_call(
                COMMAND_DICT, message_command[1:], message_contents, message, CLIENT
            )
            LOGGER.info("Command %s received.", message_command[1:])
        except CommandNotFoundError:
            LOGGER.debug("Command %s is unknown.", message_command[1:])
            return

    for keyword in KEYWORD_DICT.keys():
        if keyword in message.content.upper():

            message_contents = message.content.split()

            response = await safe_call(
                KEYWORD_DICT, keyword, message_contents, message, CLIENT
            )
            LOGGER.info("Keyword %s matched.", keyword)
            break

    if not response:
        return

    await send_response(response, message.channel)


async def send_response(response, channel):
    """ Send some kind of response to a channel. """
    if isinstance(response, discord.Embed):
        await CLIENT.send_message(channel, embed=response)
    elif isinstance(response, FileWrapper):
        await CLIENT.send_file(channel, response.name)
    else:
        await CLIENT.send_message(channel, response)


def main():
    """ Initialize the bot. """
    # Load environment variables using dotenv.
    dotenv.load_dotenv(".env")

    # set up logger
    logging_setup()

    # Load commands
    devbot.commands.load_plugins()

    # Start the scheduler
    SCHEDULER.start()

    # Connect to discord.
    CLIENT.run(os.environ["TOKEN"])


def logging_setup():
    """ Sane logging config. """
    file_level = os.environ.get("FILE_LOGLEVEL", logging.DEBUG)
    console_level = os.environ.get("CONSOLE_LOGLEVEL", logging.INFO)

    # Set up basic functions to log to a file
    logging.basicConfig(
        level=file_level,
        format="%(asctime)s %(levelname)-8s-%(name)-12s: %(message)s",
        datefmt="%y-%m-%d %H:%M",
        filename=f"./logs/bot.log",
        filemode="w",
    )
    # Make a console handler to pass INFO+ messages to console
    console = logging.StreamHandler()
    console.setLevel(console_level)
    # Set up logging formatter for console
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    main()
