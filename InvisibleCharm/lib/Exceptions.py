# InvisibleCharm.lib.Exceptions.py
# CodeWriter21

from zlib import error as _zlib_error
from magic.magic import MagicException as _MagicException

__all__ = ['CouldNotDecompressError', 'InvalidCoverDataTypeError', 'CoverDataTypeNotFoundError',
           'NoEmbeddedDataFoundError', 'WinEmbeddedFileNotFoundError', 'NoEmbeddedFileFoundError',
           'NoWinEmbeddedFileFoundError']


class CouldNotDecompressError(_zlib_error):
    pass


class InvalidCoverDataTypeError(_MagicException):
    pass


class CoverDataTypeNotFoundError(InvalidCoverDataTypeError):
    pass


class NoEmbeddedDataFoundError:
    pass


class NoEmbeddedFileFoundError(NoEmbeddedDataFoundError, FileNotFoundError):
    pass


class WinEmbeddedFileNotFoundError(FileNotFoundError):
    pass


class NoWinEmbeddedFileFoundError(WinEmbeddedFileNotFoundError, NoEmbeddedFileFoundError):
    pass
