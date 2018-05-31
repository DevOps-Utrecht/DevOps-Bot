"""
    Plugins folder to house all modular command files.
"""

import logging
import os.path
import importlib

LOGGER = logging.getLogger(__name__)


def load_plugins():
    """
        Import all python files in directory as plugins.
    """
    root = os.path.dirname(__file__)
    LOGGER.info("Importing files from %s", root)

    for _root, _dirs, files in os.walk(root):
        python_files = [file for file in files if file.endswith(".py")]
        for plugin in python_files:
            plugin_name = plugin[:-3]  # Strip extension
            LOGGER.info("Loading plugin %s", plugin_name)

            try:
                importlib.import_module(f".{plugin_name}", package=__name__)
            except (NameError, SyntaxError) as err:
                LOGGER.error("Error loading %s", plugin_name)
                LOGGER.exception(err)
