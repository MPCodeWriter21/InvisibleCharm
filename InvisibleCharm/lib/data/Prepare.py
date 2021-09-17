# InvisibleCharm.lib.data.Prepare.py
# CodeWriter21

import os as _os
from log21 import get_colors as _gc
# We use zlib library to compress and decompress data
import zlib as _zlib
from InvisibleCharm.lib.Console import logger as _logger, exit
from InvisibleCharm.lib.data.Encryption import encrypt as _encrypt, decrypt as _decrypt

__all__ = ['prepare_data', 'add_num']


# Prepares data(compression and encryption)
def prepare_data(data: bytes, hiding: bool = True, compress: bool = False, encrypt_pass: str = None) -> bytes:
    if hiding:
        if compress:
            _logger.debug(_gc("ly") + ' * Compressing data...', end='')
            data = _zlib.compress(data)
            _logger.debug('\r' + _gc("lg") + ' = Data compressed.')
        if encrypt_pass:
            data = _encrypt(data, encrypt_pass)
    else:
        if encrypt_pass:
            data = _decrypt(data, encrypt_pass)
        if compress:
            _logger.debug(_gc("ly") + ' * Trying to decompress data...', end='')
            try:
                data = _zlib.decompress(data)
                _logger.debug('\r' + _gc("lg") + ' = Data decompressed.')
            except _zlib.error:
                exit('\r' + _gc("lr") +
                     " ! Error: Couldn't decompress!\n + Data may not be compressed or may be encrypted.")
    return data


# Adds a numeric identifier
def add_num(name: str):
    n = ''
    prefix = ''
    extension = ''
    if _os.sep in name:
        prefix = name[:name.rfind(_os.sep) + 1]
        name = name[name.rfind(_os.sep) + 1:]
    if ':' in name:
        prefix += name[:name.rfind(':') + 1]
        name = name[name.rfind(':') + 1:]
    if len(name) > 1 and '.' in name[1:]:
        extension = name[name.rfind('.'):]
        name = name[:-1 * len(extension)]
    while len(name) > 0 and name[-1].isdigit():
        n = name[-1] + n
        name = name[:-1]
    if not n:
        n = 0
    else:
        n = int(n)
    n += 1
    return prefix + name + str(n) + extension
