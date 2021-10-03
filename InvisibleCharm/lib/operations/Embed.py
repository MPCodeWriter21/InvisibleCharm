# InvisibleCharm.lib.operations.Image.py
# CodeWriter21

import os as _os
import uuid as _uuid
# We use magic to check file type
import magic as _magic
# We use zipfile library to embed files
import zipfile as _zipfile
from typing import Union as _Union
from log21 import get_colors as _gc
from InvisibleCharm.lib.data.Prepare import add_num as _add_num
from InvisibleCharm.Settings import embed_capable as _embed_capable
from InvisibleCharm.lib.Console import logger as _logger, input, exit
from InvisibleCharm.lib.File import open_file as _open_file, save_file as _save_file, \
    delete_source_file as _delete_source_file
from InvisibleCharm.lib.data.Prepare import prepare_data as _prepare_data
from InvisibleCharm.lib.Exceptions import InvalidCoverDataTypeError as _InvalidCoverDataTypeError, \
    CoverDataTypeNotFoundError as _CoverDataTypeNotFoundError, NoEmbeddedFileFoundError as _NoEmbeddedFileFoundError, \
    NoEmbeddedDataFoundError as _NoEmbeddedDataFoundError

__all__ = ['embed_file', 'extract_file', 'embed', 'extract']


# Embeds a file in a cover
def embed_file(source: str, cover: str, dest: str, delete_source: bool, compress: bool,
               encrypt_pass: _Union[str, bytes] = '', force_use_cover: bool = False) -> None:
    """
    Embeds a file in a cover

    :param source: str: Source file path.
    :param cover: str: Cover file path.
    :param dest: str: Destination file path.
    :param delete_source: bool: Do you want to delete the source file after embed process?
    :param compress: bool: Do you want to compress the source data?
    :param encrypt_pass: Union[str, bytes] = '': A password for encrypting the file
    :param force_use_cover: bool = False: Use this cover data without raising any exceptions.
    :return: None
    """

    # Checks whether the inputs are valid
    if not isinstance(source, str):
        raise TypeError('`source` must be an instance of str.')
    if not _os.path.exists(source):
        raise FileNotFoundError('`source` must be an existing file path.')
    if not isinstance(cover, str):
        raise TypeError('`cover` must be an instance of str.')
    if not _os.path.exists(cover):
        raise FileNotFoundError('`cover` must be an existing file path.')
    if not isinstance(dest, str):
        raise TypeError('`dest` must be an instance of str.')
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    # Reads and prepares source data
    source_data = _open_file(source, 'source', True, compress, encrypt_pass)

    # Reads cover file content
    cover_data = _open_file(cover, 'cover')

    data = embed(source_data, cover_data, False, force_use_cover=force_use_cover)

    # Saves the prepared data in the destination path
    _save_file(dest, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Embeds data in a cover
def embed(source_data: _Union[str, bytes], cover: _Union[str, bytes], compress: bool,
          encrypt_pass: _Union[str, bytes] = '', force_use_cover: bool = False) -> bytes:
    """
    Embeds data in a cover

    :param source_data: Union[str, bytes]: Data to embed.
    :param cover: bytes: Cover data.
    :param compress: bool: Do you want to compress the source data?
    :param encrypt_pass: Union[str, bytes] = '': A password for encrypting the file
    :param force_use_cover: bool = False: Use this cover data without raising any exceptions.
    :return: bytes: Embedded data
    """

    # Checks whether the inputs are valid
    if not isinstance(source_data, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if isinstance(source_data, str):
        source_data = source_data.encode()
    if not isinstance(cover, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if isinstance(cover, str):
        cover = cover.encode()
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    # Prepares the data
    source_data = _prepare_data(source_data, True, compress, encrypt_pass)

    if not force_use_cover:
        _logger.debug(_gc("ly") + ' * Checking cover file type...', end='')
        # Checks cover file type
        valid = False
        try:
            cover_type = _magic.from_buffer(cover)
            for t in _embed_capable:
                if t.lower() in cover_type.lower():
                    valid = True
        except _magic.magic.MagicException:
            raise _CoverDataTypeNotFoundError("Couldn't identify cover data type!")
        if not valid:
            raise _InvalidCoverDataTypeError(f'Cover Data Type({cover_type}) is not supported!')
        _logger.debug('\r' + _gc("lg") + ' = Cover file is valid.')
    data = cover

    _logger.debug(_gc("ly") + ' * Making an archive...', end='')
    # Generates a name for a temporarily zip archive
    archive_tmp_path = f'tmp.zip'
    while _os.path.exists(archive_tmp_path):
        archive_tmp_path = _add_num(archive_tmp_path)
    # Makes a zip archive
    archive = _zipfile.ZipFile(archive_tmp_path, 'w')
    # Writes prepared source data in the zip archive
    archive.writestr(str(_uuid.uuid4()), source_data)
    # Closes the archive
    archive.close()
    _logger.debug('\r' + _gc("lg") + ' = Archive made.')

    _logger.debug(_gc("ly") + ' * Reading archive...', end='')
    # Reads the archive data
    with open(archive_tmp_path, 'rb') as archive_file:
        archive_data = archive_file.read()
    _logger.debug('\r' + _gc("lg") + ' = Archive opened.')
    # Appends the archive data to the cover data
    data += archive_data
    _logger.debug(_gc("ly") + ' * Removing temp archive...', end='')
    # Removes temporarily zip archive file
    _os.remove(archive_tmp_path)
    _logger.debug('\r' + _gc("lg") + ' = Temp file removed.')

    return data


# Extracts a file from an embedded file
def extract_file(source: str, dest: str, delete_source: bool, compress: bool,
                 encrypt_pass: _Union[str, bytes] = '') -> None:
    """
    Embeds a file in a cover

    :param source: str: Source file path to decrypt.
    :param dest: str: Destination file path.
    :param delete_source: bool: Do you want to delete the source file after embed process?
    :param compress: bool: Do you want to decompress the source data?
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

    _logger.debug(_gc("ly") + ' * Opening file...', end='')
    # Opens the source file as a zip archive
    try:
        archive = _zipfile.ZipFile(source)
    except _zipfile.BadZipfile:
        raise _NoEmbeddedFileFoundError(f'No embedded file found in {source}')
    # Reads the hidden data from the source file
    with archive.open(archive.filelist[0], 'r') as source_file:
        data = source_file.read()
    # Closes the archive
    archive.close()
    _logger.debug('\r' + _gc("lg") + ' = Source file opened.')

    # Prepares the data
    data = _prepare_data(data, False, compress, encrypt_pass)

    # Saves the extracted data in the destination path
    _save_file(dest, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Extracts data from an embedded data
def extract(source_data: _Union[str, bytes], compress: bool, encrypt_pass: _Union[str, bytes] = '') -> bytes:
    """
    Extracts data from an embedded data

    :param source_data: : Union[str, bytes]: Data to extract.
    :param compress: bool: Do you want to decompress the source data?
    :param encrypt_pass: Union[str, bytes] = '': A password for decrypting the file
    :return: bytes: Extracted data
    """

    # Checks whether the inputs are valid
    if not isinstance(source_data, (str, bytes)):
        raise TypeError('`data` must be an instance of str or bytes.')
    if isinstance(source_data, str):
        source_data = source_data.encode()
    if not isinstance(encrypt_pass, (str, bytes)) and encrypt_pass:
        raise TypeError('`encrypt_pass` must be an instance of str or bytes.')

    _logger.debug(_gc("ly") + ' * Opening file...', end='')
    # Generates a name for a temporarily zip archive
    archive_tmp_path = f'tmp'
    while _os.path.exists(archive_tmp_path):
        archive_tmp_path = _add_num(archive_tmp_path)
    with open(archive_tmp_path, 'wb') as file:
        file.write(source_data)
    del source_data
    # Opens the source file as a zip archive
    try:
        archive = _zipfile.ZipFile(archive_tmp_path)
    except _zipfile.BadZipfile:
        raise _NoEmbeddedDataFoundError('No embedded data found in the input data!')
    # Reads the hidden data from the source file
    with archive.open(archive.filelist[0], 'r') as source_file:
        data = source_file.read()
    # Closes the archive
    archive.close()
    _logger.debug('\r' + _gc("lg") + ' = Source file opened.')
    _os.remove(archive_tmp_path)

    # Prepares the data
    data = _prepare_data(data, False, compress, encrypt_pass)

    return data
