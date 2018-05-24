"""
    Main entry point for devbot.
"""

import os
import discord
import dotenv
import devbot.commands
from devbot.registry import COMMAND_DICT, safe_call, CommandNotFoundError
from devbot.tools.logging import get_logger

CLIENT = discord.Client()
#: The main discord client.
LOGGER = get_logger(__name__)
#: An Easy_logger instance.
SYMBOL = '!'
#: The command symbol


@CLIENT.event
async def on_ready():
    """ Log bot info. """
    LOGGER.info('Bot logged is as: %s, with id: %s.',
                CLIENT.user.name, CLIENT.user.id)


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
                COMMAND_DICT, message_command[1:],
                message_contents,
                message,
                CLIENT
            )
            LOGGER.info("command")
        except CommandNotFoundError:
            LOGGER.debug('Command %s is unknown.', message_command[1:])
            return

        if not response:
            return

        if isinstance(response, discord.Embed):
            await CLIENT.send_message(message.channel, embed=response)
        else:
            await CLIENT.send_message(message.channel, response)


def main():
    """ Initialize the bot. """
    # Load environment variables using dotenv.
    dotenv.load_dotenv('.env')

    # Load commands
    devbot.commands.load_plugins()

    # Connect to discord.
    CLIENT.run(os.environ['TOKEN'])


if __name__ == '__main__':
    main()
