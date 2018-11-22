from setuptools import setup
from devbot import VERSION

try:
    import pathlib
except ImportError:
    raise ImportError("Install requires Python>=3.4")


required_dirs = ["logs"]

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
    python_requires=">=3.6",
    extras_require={"dev": ["black", "pylint"]},
    packages=["devbot", "devbot.commands", "devbot.tools"],
    scripts=["scripts/xkcd_crawler.py"],
    zip_safe=False,
    license="MIT",
    entry_points={"console_scripts": ["start=devbot.bot:main"]},
)

for required_dir in required_dirs:
    pathlib.Path(required_dir).mkdir(exist_ok=True)
