# InvisibleCharm.lib.Console.py
# CodeWriter21

import sys as _sys
from log21 import get_logger as _get_logger, INFO as _INFO, DEBUG as _DEBUG, WARNING as _WARNING

__all__ = ['logger', 'input', 'verbose', 'quiet', 'exit']

_input_backup = input

logger = _get_logger(show_level=False, level=_INFO)


def input(*args, end='') -> str:
    logger.info(*args, end=end)
    return _input_backup('')


# Exits
def exit(*args) -> None:
    if args:
        logger.error(*args)
    logger.error(end='\033[0m')
    _sys.exit()


# Enables verbose mode
def verbose() -> int:
    logger.setLevel(_DEBUG)
    return logger.level


# Enables quiet mode
def quiet() -> int:
    logger.setLevel(_WARNING)
    return logger.level
