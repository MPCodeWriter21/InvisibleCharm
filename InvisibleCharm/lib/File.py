# InvisibleCharm.lib.File.py
# CodeWriter21

import os as _os
# We use getoutput function to get the output of a command
from subprocess import getoutput as _getoutput
from log21 import get_colors as _gc
from InvisibleCharm.lib.Console import logger as _logger
from InvisibleCharm.lib.data.Prepare import prepare_data as _prepare_data, add_num as _add_num


# Opens a file and returns prepared content
def open_file(path: str, name: str, hiding: bool = True, compress: bool = False, encrypt_pass: str = None) -> bytes:
    _logger.debug(_gc("ly") + f' * Reading {name.lower()} file...', end='')
    with open(path, 'rb') as file:
        data = file.read()
    _logger.debug('\r' + _gc("lg") + f' = {name.capitalize()} file opened.')
    return _prepare_data(data, hiding, compress, encrypt_pass)


# Writes data in the given path
def save_file(path: str, data: bytes) -> None:
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
    _logger.debug(_gc("ly") + ' * Deleting source file...', end='')
    _os.remove(path)
    _logger.debug('\r' + _gc("ly") + ' = Source file deleted')


# Returns the possible names of the embedded files in a windows path
def get_names(path: str) -> list:
    output = _getoutput('dir ' + _os.path.split(path)[0] + ' /r /a')
    names = []
    for line in output.split('\n'):
        if line.endswith(':$DATA'):
            if line[39:].startswith(_os.path.split(path)[1]):
                names.append(line[39:].split(':')[1])
    return names
