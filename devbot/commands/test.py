""" Basic test command. """

from devbot.registry import Command


@Command(["ping"])
async def ping(*_args, **_kwargs):
    """ Pong! """
    return "pong!"
