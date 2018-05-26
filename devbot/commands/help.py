"""
    Command module that contains help functions.
"""

from inspect import cleandoc
from devbot.registry import Command, COMMAND_CATEGORIES


@Command(["help", "commands", "list"])
async def list_commands(*_args, **_kwargs):
    """ Print this help message. """
    return_list = []
    category_list = COMMAND_CATEGORIES.keys()

    for c in category_list:
        category = c or "No category"
        return_list.append(f"**{category}**")

        for command in COMMAND_CATEGORIES[c]:
            name, aliases, func = command

            if func.__doc__:
                helpmessage = cleandoc(
                    func.__doc__
                )  # use the function docstring as help message.
            else:
                helpmessage = "You're on your own here."

            if aliases:
                name = f"`!{name}` (`{'`,`'.join(aliases)}`)"
            else:
                name = f"`!{name}`"

            return_list.append(f"{name}: {helpmessage}")

    return "\n".join(return_list)
