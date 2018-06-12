""" Basic test command. """

from devbot.registry import Command
from devbot.tools.delay import schedule_message
from devbot.bot import SCHEDULER
import discord


@Command(["ping"])
async def ping(*_args, **_kwargs):
    return "pong!"
