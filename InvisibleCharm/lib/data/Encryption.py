# InvisibleCharm.lib.data.Encryption.py
# CodeWriter21

# We use hashlib library to hash passwords
import hashlib
# We use _AES to encrypt and decrypt data
from Crypto.Cipher import AES as _AES
from log21 import get_colors as _gc
from InvisibleCharm.lib.Console import logger as _logger

__all__ = ['encrypt', 'decrypt']


# Encrypts data using AES and costume password
def encrypt(data: bytes, password: str) -> bytes:
    _logger.debug(_gc("ly") + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    _logger.debug(_gc("ly") + ' * Encrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.encrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data encrypted.')
    return data


# Decrypts data using AES and costume password
def decrypt(data: bytes, password: str) -> bytes:
    _logger.debug(_gc("ly") + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    _logger.debug(_gc("ly") + ' * Decrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.decrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data decrypted.')
    return data
