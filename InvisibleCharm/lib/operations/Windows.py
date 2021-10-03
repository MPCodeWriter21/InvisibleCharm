# InvisibleCharm.lib.operations.Windows.py
# COdeWriter21


import os as _os
from typing import Union as _Union
from log21 import get_colors as _gc
from InvisibleCharm.lib.Console import logger as _logger, input, exit
from InvisibleCharm.lib.data.Prepare import add_num as _add_num
from InvisibleCharm.lib.File import get_names as _get_names, open_file as _open_file, save_file as _save_file, \
    delete_source_file as _delete_source_file
from InvisibleCharm.lib.Exceptions import WinEmbeddedFileNotFoundError as _WinEmbeddedFileFoundError, \
    NoWinEmbeddedFileFoundError as _NoWinEmbeddedFileFoundError

__all__ = ['win_embed', 'win_extract', 'win_attrib_hide', 'win_attrib_reveal']


# Hides a file in another Windows file
def win_embed(source: str, dest: str, delete_source: bool, compress: bool, cover: str = None,
              encrypt_pass: _Union[str, bytes] = '') -> None:
    """
    Hides a file in another Windows file.

    :param source: str: Source file path.
    :param dest: str: Destination file path.
    :param delete_source: bool: Do you want to delete the source file after embed process?
    :param compress: bool: Do you want to compress the source data?
    :param cover: str: Cover file path.
    :param encrypt_pass: Union[str, bytes] = '': A password for encrypting the file
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(source, str):
        raise TypeError('`source` must be an instance of str.')
    if not _os.path.exists(source):
        raise FileNotFoundError('`source` must be an existing file path.')
    if not isinstance(dest, str):
        raise TypeError('`dest` must be an instance of str.')
    if cover:
        if not isinstance(cover, str):
            raise TypeError('`cover` must be an instance of str.')
        if not _os.path.exists(cover):
            raise FileNotFoundError('`cover` must be an existing file path.')
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    # Gets the list of available embedded names in the destination path
    names = _get_names(dest)
    # Generates a default name
    default_name = _os.path.split(source)[1]
    # Makes sure that default name is unique
    while default_name in names:
        default_name = _add_num(default_name)

    while True:
        # Gets name from user
        name = input(_gc("ly") + f' * Enter a name for embedded file' + _gc("lw") +
                     f'({_gc("lm")}Default{_gc("lr")}: {_gc("lc")}{default_name}{_gc("lw")}){_gc("lr")}: '
                     + _gc("lg"))
        if name in names:
            # Makes sure that user wants to replace the existing file
            confirm = input(_gc("ly") + f' * `{_gc("lc")}{name}{_gc("ly")}` already exists!' +
                            '\n * Do you want to replace it?' +
                            f'{_gc("lw")}({_gc("lr")}y{_gc("lw")}/{_gc("lg")}N{_gc("lw")}) ' +
                            _gc("lg")).lower()
            if confirm == 'n':
                continue
        break
    # Sets name to default_name value
    if not name:
        name = default_name

    _logger.debug(_gc("ly") + ' * Preparing path...', end='')
    if cover and cover != dest:
        # Writes the cover data in the destination path
        with open(cover, 'rb') as cover_file:
            cover = cover_file.read()
        with open(dest, 'wb') as dest_file:
            dest_file.write(cover)
    elif not _os.path.exists(dest):
        # Creates an empty file in the destination path
        with open(dest, 'w') as dest_file:
            dest_file.write('')
    _logger.debug('\r' + _gc("lg") + ' = File is ready.')

    # Reads and prepares the source data
    data = _open_file(source, 'source', True, compress, encrypt_pass)

    # Saves the prepared data
    _save_file(dest + ':' + name, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Extracts a hidden file from a file in windows
def win_extract(source: str, dest: str, delete_source: bool, compress: bool, name: str = '',
                encrypt_pass: _Union[str, bytes] = '') -> None:
    """
    Extracts a hidden file from a file in Windows.

    :param source: str: Source file path.
    :param dest: str: Destination file path.
    :param delete_source: bool: Do you want to delete the source file after embed process?
    :param compress: bool: Do you want to decompress the source data?
    :param name: str = '': The name of the embedded file to extract(Automatically finds if the
    :param encrypt_pass: Union[str, bytes] = '': A password for decrypting the file
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(source, str):
        raise TypeError('`source` must be an instance of str.')
    if not _os.path.exists(source):
        raise FileNotFoundError('`source` must be an existing file path.')
    if not isinstance(dest, str):
        raise TypeError('`dest` must be an instance of str.')
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    # Gets the list of available embedded names in destination path
    possible_names = _get_names(source)
    if len(possible_names) == 0:
        # Raises an exception if no embedded file is available
        raise _NoWinEmbeddedFileFoundError("No win-embedded file found!")
    elif len(possible_names) == 1:
        # Choose the only embedded file automatically
        name = possible_names[0]

    if name not in possible_names:
        raise _WinEmbeddedFileNotFoundError(f"There is no win-embedded file in '{source}' with name: '{name}'")

    # Reads and prepares data
    data = _open_file(source + ':' + name, 'source', False, compress, encrypt_pass)

    # Saves the prepared data in the destination path
    _save_file(dest, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Changes a file windows attributes not to be shown in Windows explorer
def win_attrib_hide(path: str) -> None:
    """
    Changes a file windows attributes not to be shown in Windows explorer

    :param path: str: File path.
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not _os.path.exists(path):
        raise FileNotFoundError('`path` must be an existing file path.')

    _logger.info(_gc("ly") + ' * Running `attrib` command...', end='')
    # Runs Windows attrib command
    # +h : Adds Hidden File attribute
    # -a : Removes Archive File attribute
    # +s : Adds System File attribute
    _os.system('attrib +h -a +s "' + path + '"')
    _logger.info('\r' + _gc("lg") + ' = Done.')


# Changes a file windows attributes to be shown in Windows explorer
def win_attrib_reveal(path: str) -> None:
    """
    Changes a file windows attributes to be shown in Windows explorer

    :param path: str: File path.
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not _os.path.exists(path):
        raise FileNotFoundError('`path` must be an existing file path.')

    _logger.info(_gc("ly") + ' * Running `attrib` command...', end='')
    # Runs Windows attrib command
    # -h : Removes Hidden File attribute
    # +a : Adds Archive File attribute
    # -s : Removes System File attribute
    _os.system('attrib -h +a -s "' + path + '"')
    _logger.info('\r' + _gc("lg") + ' = Done.')
