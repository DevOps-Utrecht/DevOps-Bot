"""
    A tool to allow for the easy aquisition of data from RESTfull API's.
"""

import aiohttp
import logging

LOGGER = logging.getLogger(__name__)


async def get_json(url, *params):
    """
        Sends a request to a RESTfull API and returns it's JSON

        use: get_json(url, (key,val), (key,val)) to include key-val pairs as params
    """
    parameters = [p for p in params]  # Make a list of tuples
    async with aiohttp.get(url, params=parameters) as r:
        if r.status == 200:
            json = await r.json()
            return json
        else:
            LOGGER.error(f"Status code {r.status} returned from {r.url}")
            raise APIAccessError(f"HTTP status code {r.status} was returned")


async def get_text(url, *params):
    """
        Sends a request to a RESTfull API and returns it's contents

        use: get_text(url, (key,val), (key,val)) to include key-val pairs as parameters
    """
    parameters = [p for p in params]  # Make a list of tuples
    async with aiohttp.get(url, params=parameters) as r:
        if r.status == 200:
            t = await r.text(encoding="utf-8")
            return t
        else:
            LOGGER.error(f"Status code {r.status} returned from {r.url}")
            raise APIAccessError(f"HTTP status code {r.status} was returned")


class APIAccessError(Exception):
    pass
