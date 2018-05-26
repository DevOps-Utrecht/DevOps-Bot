# DevOps-Bot
A discord bot for DevOps

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/60f49e554e4445e69208a2f1ae45a5f0)](https://www.codacy.com/app/RobinSikkens/bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DevOps-Utrecht/bot&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Set-up
Setting up a running version of DevBot is easy.

Follow the following steps:
1. Clone the repository.

use: `git clone git@github.com:DevOps-Utrecht/bot.git`
    or `git clone https://github.com/DevOps-Utrecht/bot.git`


2. Set up a python virtual env.

use: `python3.6 -m venv venv`


3. Activate the virtual env.

use: `source venv/bin/activate`


4. Set up dependencies.

use: `python setup.py install` or `python setup.py develop`


5. Make a .env file.

Create a `.env` file in the root directory containing `TOKEN=<Your Discord Token>`.


6. Run the bot

use: `start`

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
