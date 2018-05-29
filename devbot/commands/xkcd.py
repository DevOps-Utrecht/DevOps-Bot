""" Latest XKCD command. """
import json
import urllib.request

from devbot.registry import Command
from devbot.tools import api_requests

@Command(["xkcd"])
async def xkcd(*_args, **_kwargs):
    url = "https://xkcd.com/info.0.json"
    image_url = api_requests.get_text(url, ("data", "img"))
    return image_url
