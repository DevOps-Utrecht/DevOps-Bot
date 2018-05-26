from setuptools import setup
from devbot import VERSION

setup(
    name="devbot",
    version=VERSION,
    description="A discord bot created to work with the DevOps server",
    url="https://github.com/DevOps-Utrecht/DevOps-Bot",
    install_requires=["discord.py", "asyncio", "python-dotenv", "easy_logger", "sqlalchemy"],
    packages=["devbot"],
    zip_safe=False,
    license="MIT",
    entry_points={"console_scripts": ["start=devbot.bot:main"]},
)

