# InvisibleCharm.lib.data.Encryption.py
# CodeWriter21

# We use hashlib library to hash passwords
import hashlib
from log21 import get_colors as _gc
from typing import Union as _Union, Tuple as _Tuple
# The following modules are used for the encryption
from Crypto.PublicKey import RSA as _RSA
from Crypto.Cipher import AES as _AES, PKCS1_OAEP as _PKCS1_OAEP
from Crypto.Random import get_random_bytes

from InvisibleCharm.lib.Console import logger as _logger

__all__ = ['encrypt_aes', 'decrypt_aes', 'encrypt_rsa', 'decrypt_rsa']


def __prepare_aes(data: _Union[str, bytes], password: _Union[str, bytes]) -> _Tuple[bytes, bytes, bytes]:
    """
    Prepares data for encrypt_aes and decrypt_aes functions.

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


def __prepare_rsa(data: _Union[str, bytes], key: _RSA.RsaKey) -> _Tuple[bytes, _PKCS1_OAEP.PKCS1OAEP_Cipher]:
    """
    Prepares data for encrypt_rsa and decrypt_rsa functions.

    :param data: Union[str, bytes]
    :param key: RSA.RsaKey
    :return:
    """
    # Checks whether the inputs are valid
    if not isinstance(data, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if isinstance(data, str):
        data = data.encode()
    if not isinstance(key, _RSA.RsaKey):
        raise TypeError('`key` must be an instance of Crypto.PublicKey.RSA.RsaKey.')

    # Encrypt the session key with the public RSA key
    cipher_rsa = _PKCS1_OAEP.new(key)

    return data, cipher_rsa


# Encrypts data using AES and costume password
def encrypt_aes(data: _Union[str, bytes], password: _Union[str, bytes]) -> bytes:
    """
    Encrypts data using AES and costume password.

    :param data: Union[str, bytes]: Data to encrypt.
    :param password: Password for encryption.
    :return: bytes: Encrypted data.
    """

    data, md5, sha512 = __prepare_aes(data, password)

    _logger.debug(_gc("ly") + ' * Encrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.encrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data encrypted.')
    return data


# Decrypts data using AES and costume password
def decrypt_aes(data: _Union[str, bytes], password: _Union[str, bytes]) -> bytes:
    """
    Decrypts data using AES and costume password.

    :param data: Union[str, bytes]: Data to decrypt.
    :param password: Password for decryption.
    :return: bytes: Decrypted data.
    """

    data, md5, sha512 = __prepare_aes(data, password)

    _logger.debug(_gc("ly") + ' * Decrypting data...', end='')
    cipher = _AES.new(md5, _AES.MODE_EAX, nonce=sha512)
    data = cipher.decrypt(data)
    _logger.debug('\r' + _gc("lg") + ' = Data decrypted.')
    return data


# Encrypts data using RSA and costume key
def encrypt_rsa(data: _Union[str, bytes], recipient_key: _RSA.RsaKey, use_private_key: bool = False) -> bytes:
    """
    Encrypts data using RSA and costume key.

    :param data: The data to encrypt.
    :param recipient_key: The key to encrypt the data with.
    :param use_private_key: Forces the use of the private key. Will raise an error if the key is private and this
        parameter is set to False.
    :raises TypeError:
        If the `data` is not an instance of str or bytes.
        If the `recipient_key` is not an instance of Crypto.PublicKey.RSA.RsaKey.
        If the `use_private_key` is False and the `recipient_key` is private.
    :return: bytes: The encrypted data.
    """

    if not use_private_key and recipient_key.has_private():
        raise TypeError('The input key is a private key!\n'
                        'Please use a public key for encryption or set `use_private_key` to True!')

    # Generates a random key
    session_key = get_random_bytes(16)

    data, cipher_rsa = __prepare_rsa(data, recipient_key)

    # Encrypts the session key with the public RSA key
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    _logger.debug(_gc("ly") + ' * Encrypting data...', end='')
    # Encrypt the data with the AES session key
    cipher = _AES.new(session_key, _AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    data = encrypted_session_key + cipher.nonce + tag + ciphertext
    _logger.debug('\r' + _gc("lg") + ' = Data encrypted.')

    return data


# Decrypts data using RSA and costume key
def decrypt_rsa(data: _Union[str, bytes], private_key: _RSA.RsaKey) -> bytes:
    """
    Decrypts data using RSA and costume key.

    :param data: The data to decrypt.
    :param private_key: The key to decrypt the data with.
    :raises TypeError:
        If the `data` is not an instance of str or bytes.
        If the `private_key` is not an instance of Crypto.PublicKey.RSA.RsaKey.
        If the `private_key` is not private.
    :return:
    """

    data, cipher_rsa = __prepare_rsa(data, private_key)

    enc_session_key = data[:private_key.size_in_bytes()]
    nonce = data[private_key.size_in_bytes():private_key.size_in_bytes() + _AES.block_size]
    tag = data[private_key.size_in_bytes() + _AES.block_size:private_key.size_in_bytes() + _AES.block_size * 2]
    ciphertext = data[private_key.size_in_bytes() + _AES.block_size * 2:]

    # Decrypts the session key with the private RSA key
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypts the data with the AES session key
    cipher_aes = _AES.new(session_key, _AES.MODE_EAX, nonce)

    return cipher_aes.decrypt_and_verify(ciphertext, tag)
