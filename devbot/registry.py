"""
    Allows the registering of new commands

    Hugely inspired by https://github.com/RobinSikkens/Sticky-discord
"""

from collections import defaultdict
import logging

LOGGER = logging.getLogger(__name__)


class RegisteringDecorator(object):
    """
        General decorator for registering.
        Must be overridden.
    """

    target_dict = {}

    def __init__(self, name):
        """ Register command by name or list of aliasses. """
        self.name = name

    def __call__(self, func):
        """ Register the callable under the given name. """

        # If name is a list of aliasses register all
        if isinstance(self.name, list):
            for alias in self.name:
                self.target_dict[alias.upper()] = func
        else:
            self.target_dict[self.name.upper()] = func

        return func


#: Dict for all registered commands, maps uppercase commands to functions
COMMAND_DICT = {}

#: Dict for categorization, usefull when listing usable commands
COMMAND_CATEGORIES = defaultdict(list)


class Command(RegisteringDecorator):
    """
        Decorator that registers it's function as a usable command.
    """

    target_dict = COMMAND_DICT
    categories = COMMAND_CATEGORIES

    def __init__(self, name, category=None):
        """ Store params and call super """
        self.category = category
        super().__init__(name)

    def __call__(self, func):
        """ Register command category and call super. """
        if isinstance(self.name, str):
            self.categories[self.category].append((self.name, None, func))
        else:
            self.categories[self.category].append((self.name[0], self.name[1:], func))
        return super().__call__(func)


class CommandNotFoundError(Exception):
    """ Exception for when the command is unknown. """

    def __init__(self, command):
        message = f"Command not found: {command}"
        super().__init__(message)


async def safe_disable(target_dict, key, *args, **kwargs):
    """ Wrapper that 'safely' calls a function, it disables a function if it breaks. """

    command_name = key.upper()
    if command_name not in target_dict:
        raise CommandNotFoundError(key)

    try:
        return await target_dict[key.upper()](*args, **kwargs)
    except (NameError, TypeError):
        raise
    except Exception as exc:  # pylint: disable=broad-except
        del target_dict[key.upper()]
        LOGGER.warning("Exception occurred, disabled %s", key)
        LOGGER.exception(exc)
        return "Something is wrong, command disabled."


async def safe_call(target_dict, key, *args, **kwargs):
    """ Wrapper that safely calls a function and returns the error thrown. """

    # Throw error when the called command does not exist in the dictionary.
    # Should only happen when a safe call fails while bot is doing another
    # command async.
    command_name = key.upper()
    if command_name not in target_dict:
        raise CommandNotFoundError(key)

    try:
        return await target_dict[command_name](*args, **kwargs)
    except (NameError, TypeError):
        raise
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Exception occurred, passed with safe_call %s", key)
        LOGGER.exception(exc)
        return str.format("Something went wrong, could not complete command: "
                          + "\n%s", exc)
