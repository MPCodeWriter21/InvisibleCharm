# InvisibleCharm.lib.data.Encryption.py
# CodeWriter21

# We use hashlib library to hash passwords
import hashlib
from log21 import get_colors as _gc
from typing import Union as _Union, Tuple as _Tuple
# We use _AES to encrypt and decrypt data
from Crypto.Cipher import AES as _AES
from InvisibleCharm.lib.Console import logger as _logger

__all__ = ['encrypt', 'decrypt']


def __prepare(data: _Union[str, bytes], password: _Union[str, bytes]) -> _Tuple[bytes, bytes, bytes]:
    """
    Prepares data for encrypt and decrypt functions.

    :param data: Union[str, bytes]
    :param password: Union[str, bytes]
    :return: Tuple[bytes, bytes, bytes]: data, md5_password_hash, sha512_password_hash
    """
    # Checks whether the inputs are valid
    if not isinstance(data, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if isinstance(data, str):
        data = data.encode()
    if not isinstance(password, (str, bytes)):
        raise TypeError('`password` must be an instance of str or bytes.')
    if isinstance(password, str):
        password = password.encode()

    _logger.debug(_gc("ly") + ' * Hashing password...')
    md5 = hashlib.md5(password).digest()
    sha512 = hashlib.sha512(password).digest()

    return data, md5, sha512


# Encrypts data using AES and costume password
def encrypt(data: _Union[str, bytes], password: _Union[str, bytes]) -> bytes:
    """
    Encrypts data using AES and costume password.

    :param data: Union[str, bytes]: Data to encrypt.
    :param password: Password for encryption.
    :return: bytes: Encrypted data.
    """

    data, md5, sha512 = __prepare(data, password)

    _logger.debug(_gc("ly") + ' * Encrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.encrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data encrypted.')
    return data


# Decrypts data using AES and costume password
def decrypt(data: _Union[str, bytes], password: _Union[str, bytes]) -> bytes:
    """
    Decrypts data using AES and costume password.

    :param data: Union[str, bytes]: Data to decrypt.
    :param password: Password for decryption.
    :return: bytes: Decrypted data.
    """

    data, md5, sha512 = __prepare(data, password)

    _logger.debug(_gc("ly") + ' * Decrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.decrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data decrypted.')
    return data
