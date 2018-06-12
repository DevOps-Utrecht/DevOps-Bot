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

    pass


async def safe_call(target_dict, key, *args, **kwargs):
    """ Wrapper that 'safely' calls a function, it disables a function if it breaks. """

    command_name = key.upper()
    if command_name not in target_dict:
        raise CommandNotFoundError("Command not found: %s", key)

    try:
        return await target_dict[key.upper()](*args, **kwargs)
    except (NameError, TypeError):
        raise
    except Exception as e:
        del target_dict[key.upper()]
        LOGGER.warning("Exception occurred, disabled %s", key)
        LOGGER.exception(e)
        return "Something is wrong, command disabled."
