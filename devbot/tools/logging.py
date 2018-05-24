"""
    Contains the standard logging config function to make it easier.
"""

import logging


def get_logger(name, level=None):
    """ Create logger with given name and level. """
    result = logging.getLogger(name)
    if level:
        result.setLevel(level)

    return result
