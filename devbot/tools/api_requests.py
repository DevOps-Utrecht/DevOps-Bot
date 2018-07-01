"""
    A tool to allow for the easy aquisition of data from RESTful API's.
"""

import logging
import aiohttp

LOGGER = logging.getLogger(__name__)


async def get_json(url, *params):
    """
        Sends a request to a RESTfull API and returns it's JSON

        use: get_json(url, (key,val), (key,val)) to include key-val pairs as params
    """
    parameters = [p for p in params]  # Make a list of tuples
    async with aiohttp.get(url, params=parameters) as req:
        if req.status == 200:
            json = await req.json()
            return json
        else:
            LOGGER.error(f"Status code {req.status} returned from {req.url}")
            raise APIAccessError(f"HTTP status code {req.status} was returned")


async def get_text(url, *params):
    """
        Sends a request to a RESTfull API and returns it's contents

        use: get_text(url, (key,val), (key,val)) to include key-val pairs as parameters
    """
    parameters = [p for p in params]  # Make a list of tuples
    async with aiohttp.get(url, params=parameters) as req:
        if req.status == 200:
            return await req.text(encoding="utf-8")
        else:
            LOGGER.error(f"Status code {req.status} returned from {req.url}")
            raise APIAccessError(f"HTTP status code {req.status} was returned")


class APIAccessError(Exception):
    """ Base class for API access errors. """

    pass
