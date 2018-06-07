"""
    Main entry point for devbot.
"""

import os
import discord
import datetime
import asyncio
import dotenv
import logging
import devbot.commands
import devbot.database as db
from devbot.registry import COMMAND_DICT, safe_call, CommandNotFoundError
from devbot.tools.wrap import FileWrapper
from devbot.tools.delay import TASK_QUEUE, schedule_from_database
from sqlalchemy import and_

CLIENT = discord.Client()
#: The main discord client.
LOGGER = logging.getLogger(__name__)
#: An Easy_logger instance.
SYMBOL = "!"
#: The command symbol


async def task_scheduler():
    """ Sets a repeating task that checks whether there are messages to be sent. """
    await CLIENT.wait_until_ready()
    while not CLIENT.is_closed:
        LOGGER.debug("Checking schedule")
        while not TASK_QUEUE.empty():
            timestamp, _task_id, message, _channel = TASK_QUEUE.queue[0]
            LOGGER.debug(f"{timestamp}, {message} at Queue HEAD")
            if timestamp > datetime.datetime.now().timestamp():
                break
            timestamp, task_id, message, channel = TASK_QUEUE.get()

            if isinstance(message, discord.Embed):
                await CLIENT.send_message(channel, embed=message)
            elif isinstance(message, FileWrapper):
                await CLIENT.send_file(channel, message.name)
            else:
                await CLIENT.send_message(channel, message)

            # Set database to executed
            session = db.Session()
            entry = (session.query(db.Task).filter(db.Task.id == task_id).first())
            entry.executed = True
            session.commit()

        await asyncio.sleep(10)  # Sleep for 10 seconds


@CLIENT.event
async def on_ready():
    """ Log bot info. """
    LOGGER.info("Bot logged is as: %s, with id: %s.", CLIENT.user.name, CLIENT.user.id)


@CLIENT.event
async def on_message(message):
    """ Process incoming message. """
    if message.content.startswith(SYMBOL):
        # Split message into command and list of the remainder.
        message_command, *message_contents = message.content.split()

        if message.author == CLIENT.user:
            return  # Prevent any self-activation.

        response = None
        try:
            response = await safe_call(
                COMMAND_DICT, message_command[1:], message_contents, message, CLIENT
            )
            LOGGER.info("command")
        except CommandNotFoundError:
            LOGGER.debug("Command %s is unknown.", message_command[1:])
            return

        if not response:
            return

        if isinstance(response, discord.Embed):
            await CLIENT.send_message(message.channel, embed=response)
        elif isinstance(response, FileWrapper):
            await CLIENT.send_file(message.channel, response.name)
        else:
            await CLIENT.send_message(message.channel, response)


def main():
    """ Initialize the bot. """
    # Load environment variables using dotenv.
    dotenv.load_dotenv(".env")

    # set up logger
    logging_setup()

    # Load commands
    devbot.commands.load_plugins()

    # Load schedule from database
    schedule_from_database()

    # Add the command scheduler as task
    CLIENT.loop.create_task(task_scheduler())

    # Connect to discord.
    CLIENT.run(os.environ["TOKEN"])


def logging_setup():
    file_level = logging.DEBUG
    console_level = logging.INFO
    if "FILE_LOGLEVEL" in os.environ.keys():
        file_level = os.environ["FILE_LOGLEVEL"]
    if "CONSOLE_LOGLEVEL" in os.environ.keys():
        console_level = os.environ["CONSOLE_LOGLEVEL"]
    # Set up basic functions to log to a file
    logging.basicConfig(level=file_level,
                        format="%(asctime)s %(levelname)-8s-%(name)-12s: %(message)s",
                        datefmt="%y-%m-%d %H:%M",
                        filename=f"./logs/bot.log",
                        filemode="w")
    # Make a console handler to pass INFO+ messages to console
    console = logging.StreamHandler()
    console.setLevel(console_level)
    # Set up logging formatter for console
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    main()


