# InvisibleCharm.lib.File.py
# CodeWriter21

import os as _os
from log21 import get_colors as _gc
from typing import Union as _Union, List as _List
# We use getoutput function to get the output of a command
from subprocess import getoutput as _getoutput
from InvisibleCharm.lib.Console import logger as _logger
from InvisibleCharm.lib.data.Prepare import prepare_data as _prepare_data, add_num as _add_num


# Opens a file and returns prepared content
def open_file(path: str, name: str, hiding: bool = True, compress: bool = False,
              encrypt_pass: _Union[str, bytes] = '') -> bytes:
    """
    Gets a file path and a name and reads the contents of the file and prepares it using
    InvisibleCharm.lib.data.Prepare.prepare_data function.

    :param path: str: Input file path
    :param name: str: A name to use for debug messages
    :param hiding: bool = True: Are you going to hide this file?
    :param compress: bool = False: Do you want to compress this file?
    :param encrypt_pass: Union[str, bytes] = '': A password for encrypting the file
    :return: bytes: Prepared data
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not _os.path.exists(path):
        raise FileNotFoundError('`path` must be an existing file path.')
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    name = str(name)
    _logger.debug(_gc("ly") + f' * Reading {name.lower()} file...', end='')
    with open(path, 'rb') as file:
        data = file.read()
    _logger.debug('\r' + _gc("lg") + f' = {name.capitalize()} file opened.')
    return _prepare_data(data, hiding, compress, encrypt_pass)


# Writes data in the given path
def save_file(path: str, data: _Union[bytes, str]) -> None:
    """
    Writes data in the given path.

    :param path: str: File path to write the data.
    :param data: Union[bytes, str]: Content to write.
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not isinstance(data, (str, bytes)):
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')
    if isinstance(data, str):
        data = data.encode()

    _logger.debug(_gc("ly") + ' * Writing in destination file...', end='')
    try:
        with open(path, 'wb') as dest_file:
            dest_file.write(data)
    except PermissionError:
        _logger.info('\r' + _gc("lr") + ' ! Error: PermissionError: Save in path `' + path + '` failed!')
        path = _add_num(path)
        while _os.path.exists(path):
            path = _add_num(path)
        with open(path, 'wb') as dest_file:
            dest_file.write(data)
        _logger.info(_gc("lg") + ' = File saved in New Path: ' + path)
    _logger.info('\r' + _gc("lg") + ' = File saved.')


# Deletes the file in the given path
def delete_source_file(path: str) -> None:
    """
    Deletes the file in the given path.

    :param path: str: File path to write the data.
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not _os.path.exists(path):
        raise FileNotFoundError('`path` must be an existing file path.')

    _logger.debug(_gc("ly") + ' * Deleting source file...', end='')
    _os.remove(path)
    _logger.debug('\r' + _gc("ly") + ' = Source file deleted')


# Returns the possible names of the embedded files in a Windows path
def get_names(path: str) -> _List[str]:
    """
    Returns the possible names of the embedded files in a Windows path.

    :param path: str: File path to write the data.
    :return: List[str]
    """

    # Checks whether the inputs are valid
    if not isinstance(path, str):
        raise TypeError('`path` must be an instance of str.')
    if not _os.path.exists(path):
        raise FileNotFoundError('`path` must be an existing file path.')

    output = _getoutput('dir ' + _os.path.split(path)[0] + ' /r /a')
    names = []
    for line in output.split('\n'):
        if line.endswith(':$DATA'):
            if line[39:].startswith(_os.path.split(path)[1]):
                names.append(line[39:].split(':')[1])
    return names
