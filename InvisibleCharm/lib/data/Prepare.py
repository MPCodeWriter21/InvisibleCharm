# InvisibleCharm.lib.data.Prepare.py
# CodeWriter21


import os as _os
# We use zlib library to compress and decompress data
import zlib as _zlib
from typing import Union as _Union
from log21 import get_colors as _gc
from Crypto.PublicKey import RSA as _RSA

from InvisibleCharm.lib.Console import logger as _logger
from InvisibleCharm.lib.Exceptions import CouldNotDecompressError as _CouldNotDecompressError
from InvisibleCharm.lib.data.Encryption import encrypt_aes as _encrypt_aes, decrypt_aes as _decrypt_aes, \
    encrypt_rsa as _encrypt_rsa, decrypt_rsa as _decrypt_rsa

__all__ = ['prepare_data', 'add_num']


# Prepares data(compression and encryption)
def prepare_data(data: _Union[str, bytes], hiding: bool = True, compress: bool = False,
                 aes_encrypt_pass: _Union[str, bytes] = '', rsa_encrypt_key: _RSA.RsaKey = None) -> bytes:
    """
    Prepares data(compression and encryption)

    :param data: Union[str, bytes]: Data to prepare.
    :param hiding: bool = True: Are you going to hide this data?
    :param compress: bool = False: Do you want to compress this file?
    :param aes_encrypt_pass: Union[str, bytes] = '': A password for encrypting the data.
    :param rsa_encrypt_key: Crypto.PublicKey.RSA.RsaKey: A public key or a private key for encrypting or decrypting the
        data.
    :return: bytes: Prepared data.
    """

    # Checks whether the inputs are valid
    if not isinstance(data, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if not isinstance(aes_encrypt_pass, (str, bytes)) and aes_encrypt_pass:
        raise TypeError('`aes_encrypt_pass` must be an instance of str or bytes.')
    if not isinstance(rsa_encrypt_key, _RSA.RsaKey) and rsa_encrypt_key:
        raise TypeError('`rsa_encrypt_key` must be an instance of Crypto.PublicKey.RSA.RsaKey.')

    if hiding:
        if compress:
            _logger.debug(_gc("ly") + ' * Compressing data...', end='')
            data = _zlib.compress(data)
            _logger.debug('\r' + _gc("lg") + ' = Data compressed.')
        if aes_encrypt_pass:
            data = _encrypt_aes(data, aes_encrypt_pass)
        if rsa_encrypt_key:
            data = _encrypt_rsa(data, rsa_encrypt_key, True)
    else:
        if rsa_encrypt_key:
            data = _decrypt_rsa(data, rsa_encrypt_key)
        if aes_encrypt_pass:
            data = _decrypt_aes(data, aes_encrypt_pass)
        if compress:
            _logger.debug(_gc("ly") + ' * Trying to decompress data...', end='')
            try:
                data = _zlib.decompress(data)
                _logger.debug('\r' + _gc("lg") + ' = Data decompressed.')
            except _zlib.error:
                raise _CouldNotDecompressError("Couldn't decompress! Data may not be compressed or may be encrypted.")
                # exit('\r' + _gc("lr") +
                #      " ! Error: Couldn't decompress!\n + Data may not be compressed or may be encrypted.")
    return data


# Adds a numeric identifier
def add_num(name: str) -> str:
    """
    Adds a numeric identifier to the input name.

    :param name: str: The name that needs an identifier.
    :return: str: The name with a new identifier.
    """

    # Checks whether the input is valid
    if not isinstance(name, str):
        raise TypeError('`name` must be an instance of str.')

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
