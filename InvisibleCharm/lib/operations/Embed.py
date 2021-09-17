# InvisibleCharm.lib.operations.Image.py
# CodeWriter21

import os as _os
# We use zipfile library to embed files
import zipfile as _zipfile
# We use magic to check file type
import magic as _magic
from log21 import get_colors as _gc
from InvisibleCharm.lib.data.Prepare import add_num as _add_num
from InvisibleCharm.Settings import embed_capable as _embed_capable
from InvisibleCharm.lib.Console import logger as _logger, input, exit
from InvisibleCharm.lib.File import open_file as _open_file, save_file as _save_file, \
    delete_source_file as _delete_source_file
from InvisibleCharm.lib.data.Prepare import prepare_data as _prepare_data

__all__ = ['embed', 'extract']


# Embeds a file in a cover
def embed(source: str, cover: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Reads cover file content
    data = _open_file(cover, 'cover')

    _logger.debug(_gc("ly") + ' * Checking cover file type...', end='')
    # Checks cover file type
    try:
        cover_type = _magic.from_buffer(data)
        valid = False
        for t in _embed_capable:
            if t.lower() in cover_type.lower():
                valid = True
    except _magic.magic.MagicException:
        confirm = input(_gc("lr") + f" ! Error: Couldn't identify file type!\n" + _gc("ly") +
                        ' * Do you still want to use this cover file?' + _gc("lw") + '(' + _gc("ly") +
                        f'Enter {_gc("lm")}Y{_gc("ly")} to confirm{_gc("lw")}){_gc("lr")}: '
                        + _gc("lg")).lower()
        if confirm == 'y':
            valid = True
        else:
            exit()
    if not valid:
        exit('\r' + _gc("lr") + " ! Error: Cover File Type(" + cover_type + ") is not supported!")
    _logger.debug('\r' + _gc("lg") + ' = Cover file is valid.')

    # Reads and prepares source data
    source_data = _open_file(source, 'source', True, compress, encrypt_pass)

    _logger.debug(_gc("ly") + ' * Making an archive...', end='')
    # Generates a name for a temporarily zip archive
    archive_tmp_path = 'tmp.zip'
    while _os.path.exists(archive_tmp_path):
        archive_tmp_path = _add_num(archive_tmp_path)
    # Makes a zip archive
    archive = _zipfile.ZipFile(archive_tmp_path, 'w')
    # Writes prepared source data in the zip archive
    archive.writestr(_os.path.split(source)[1], source_data)
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

    # Saves the prepared data in the destination path
    _save_file(dest, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Extracts a file from an embedded file
def extract(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    _logger.debug(_gc("ly") + ' * Opening file...', end='')
    # Opens the source file as a zip archive
    archive = _zipfile.ZipFile(source)
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
