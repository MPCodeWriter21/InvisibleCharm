# InvisibleCharm.lib.Console.py
# CodeWriter21

import sys as _sys
from log21 import get_logger as _get_logger, INFO as _INFO, DEBUG as _DEBUG, WARNING as _WARNING

__all__ = ['logger', 'input', 'verbose', 'quiet', 'exit']

_input_backup = input

logger = _get_logger(show_level=False, level=_INFO)


def input(*args, end='') -> str:
    """
    Prints the input arguments and returns the user input.

    :param args: Input arguments to write in the console.
    :param end:
    :return: str
    """
    logger.info(*args, end=end)
    return _input_backup('')


# Exits
def exit(*args) -> None:
    """
    Prints the input arguments and exits the program.

    :param args: Input arguments to write in the console.
    :return: None
    """
    if args:
        logger.error(*args)
    logger.error(end='\033[0m')
    _sys.exit()


# Enables verbose mode
def verbose() -> int:
    """
    Enables verbose mode.

    :return: int: logger.level
    """
    logger.setLevel(_DEBUG)
    return logger.level


# Enables quiet mode
def quiet() -> int:
    """
    Enables quiet mode.

    :return: int: logger.level
    """
    logger.setLevel(_WARNING)
    return logger.level
