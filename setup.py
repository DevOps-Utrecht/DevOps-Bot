from setuptools import setup
import pathlib
from devbot import VERSION

required_dirs = ['logs']

setup(
    name="devbot",
    version=VERSION,
    description="A discord bot created to work with the DevOps server",
    url="https://github.com/DevOps-Utrecht/DevOps-Bot",
    install_requires=[
        "discord.py",
        "asyncio",
        "python-dotenv",
        "sqlalchemy",
        "apscheduler",
    ],
    python_requires='>=3.6',
    packages=["devbot", "devbot.commands", "devbot.tools"],
    scripts=["scripts/xkcd_crawler.py"],
    zip_safe=False,
    license="MIT",
    entry_points={"console_scripts": ["start=devbot.bot:main"]},
)

[pathlib.Path(dir).mkdir(exist_ok=True) for dir in required_dirs]
