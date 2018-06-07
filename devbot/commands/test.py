""" Basic test command. """

from devbot.registry import Command
from devbot.tools.delay import delay_message
import discord


@Command(["ping"])
async def ping(*_args, **_kwargs):
    return "pong!"


@Command("delay")
async def delays(contents, message, *_args, **_kwargs):
    print(contents)
    if len(contents) > 1:
        seconds = int(contents[0])
        msg = discord.Embed(title="testEmbed")
        msg.set_image(url="https://vignette.wikia.nocookie.net/homelandtv/images/8/8e/DOD.png/revision/latest?cb=20180322155006")# " ".join(contents[1:])
        await delay_message(seconds, msg)
        return "Gotcha!"
    else:
        return "Did not understand!"
