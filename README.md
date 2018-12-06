# DevOps-Bot
A discord bot for DevOps

[![Build Status](https://travis-ci.org/DevOps-Utrecht/bot.svg?branch=master)](https://travis-ci.org/DevOps-Utrecht/bot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/60f49e554e4445e69208a2f1ae45a5f0)](https://www.codacy.com/app/RobinSikkens/bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DevOps-Utrecht/bot&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/DevOps-Utrecht/bot/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![GitHub issues](https://img.shields.io/github/issues/DevOps-Utrecht/bot.svg)](https://github.com/DevOps-Utrecht/bot/issues)
[![GitHub forks](https://img.shields.io/github/forks/DevOps-Utrecht/bot.svg)](https://github.com/DevOps-Utrecht/bot/network)
[![GitHub stars](https://img.shields.io/github/stars/DevOps-Utrecht/bot.svg)](https://github.com/DevOps-Utrecht/bot/stargazers)
![meme](https://img.shields.io/badge/Uses-Badges-00aa00.svg)

## Set-up
Setting up a running version of DevBot is easy.

Follow the following steps:
1. Clone the repository.

use: `git clone git@github.com:DevOps-Utrecht/bot.git`
    or `git clone https://github.com/DevOps-Utrecht/bot.git`


2. Create a virtualenv and install dependencies:

use: `pipenv sync [--dev]`


3. Make a .env file.

Create a `.env` file in the root directory and place the required variables in it, for example:
```
TOKEN=1234567890
DEFAULT_CHANNEL=461951313547362318
````
 Check the end of this README for more info.


4. Run the bot

use: `pipenv run start`

## Contributing Commands
DevBot uses a modular command system which makes it very easy for multiple
developers to contribute commands.

To start make a python file in `devbot/commands`.

Use the `@Command([Name, alias*])` decorator to register functions as commands.

Commands are coroutines so make sure to use `async def` when defining them.

Example:

```python
#example.py

from devbot.registry import Command

@Command('ping')
async def ping_command(*_args, **_kwargs):
    """ On !ping replies pong! """
    return 'pong!'

@Command(['echo', 'repeat'])
async def echo_command(message_contents, *_args, **_kwargs):
    """ On !echo string or !repeat string replies with string """
    return ' '.join(message_contents)
```

## Required `.env` variables
`TOKEN` sets the Discord API key, which you can get from [this website](https://discordapp.com/developers/applications/me).

## Optional `.env` variables

`CONSOLE_LOGLEVEL` sets the loglevel of what log messages get sent to the console. This value can be `DEBUG`, `INFO`
*(Default)*, `WARNING`, `ERROR` and `CRITICAL`.

`FILE_LOGLEVEL` sets the loglevel of what log messages get sent to the log file (`/logs/bot.log`). This value
 can be `DEBUG` *(Default)*, `INFO`, `WARNING`, `ERROR` and `CRITICAL`.

`DATABASE` sets the url to the database for the bot. A SQLite database will be created automatically if this variable is missing. 
Using a different database than SQLite, might require installing additional dependencies.

`REMINDER_CHANNEL` sets the default channel id. Any delayed message without a
specific channel passed will use this channel to post to.   
