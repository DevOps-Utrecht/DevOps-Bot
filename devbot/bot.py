"""
    Main entry point for devbot.
"""

import os
import discord
import dotenv
import logging
import devbot.commands
from devbot.registry import COMMAND_DICT, safe_call, CommandNotFoundError
from devbot.tools.wrap import FileWrapper

CLIENT = discord.Client()
#: The main discord client.
LOGGER = logging.getLogger(__name__)
#: An Easy_logger instance.
SYMBOL = "!"
#: The command symbol


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

    # Load commands
    devbot.commands.load_plugins()

    # Connect to discord.
    CLIENT.run(os.environ["TOKEN"])


def logging_setup():
    # Set up basic functions to log to a file
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)-8s-%(name)-12s: %(message)s",
                        datefmt="%y-%m-%d %H:%M",
                        filename=f"./logs/bot.log",
                        filemode="w")
    # Make a console handler to pass INFO+ messages to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Set up logging formatter for console
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    # set up logger
    logging_setup()
    main()


