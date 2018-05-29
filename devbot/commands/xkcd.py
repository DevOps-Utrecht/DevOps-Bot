""" Latest XKCD command. """
import json
import urllib.request

from devbot.registry import Command
from devbot.tools import api_requests as API

@Command(["xkcd"])
async def xkcd(*_args, **_kwargs) -> str:
    url = "https://xkcd.com/info.0.json"
    latest_xkcd = await API.get_json(url)
    return latest_xkcd['img']
