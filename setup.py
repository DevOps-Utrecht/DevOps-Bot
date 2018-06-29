from setuptools import setup
from devbot import VERSION

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
    packages=["devbot", "devbot.commands", "devbot.tools"],
    scripts=["scripts/xkcd_crawler.py"],
    zip_safe=False,
    license="MIT",
    entry_points={"console_scripts": ["start=devbot.bot:main"]},
)
