""" Latest XKCD command. """
import json 
import urllib.request

from devbot.registry import Command


@Command(["xkcd"])
async def xkcd():
    url = 'https://xkcd.com/info.0.json'
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    data = json.loads(text)
    return data['img']   
