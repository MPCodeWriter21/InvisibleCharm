# InvisibleCharm.lib.operations.Image.py
# CodeWriter21


from log21 import get_colors as _gc
# We use Image to convert data into image
from PIL import Image as _Image
from InvisibleCharm.lib.Console import logger as _logger
from InvisibleCharm.lib.File import open_file as _open_file, save_file as _save_file, \
    delete_source_file as _delete_source_file
from InvisibleCharm.lib.data.Prepare import prepare_data as _prepare_data

__all__ = ['to_image', 'from_image']


def vm(n: int) -> int:
    sqrt = n ** 0.5
    if sqrt.is_integer():
        return int(sqrt)
    items = list(range(2, int(sqrt)))
    items.reverse()
    for i in items:
        if n % i == 0:
            return i
    return 0


# Prepares data and calculate suitable width and height for image
def calculate_size(data: bytes, mode: int):
    data += b'\x21'
    while True:
        length = len(data)
        if length % mode != 0:
            data += b'\x00'
            continue
        length /= mode
        if vm(length) == 0:
            data += b'\x00'
            continue
        width = vm(length)
        height = length // width
        tmp1 = min(width, height)
        tmp2 = max(width, height)
        width = int(tmp1)
        height = int(tmp2)
        if height / width > 2:
            data += b'\x00'
            continue
        break
    return data, width, height


# Convert a file to an image
def to_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None, mode: int = 3) -> None:
    # Reads and prepares the source file data
    data = _open_file(source, 'source', True, compress, encrypt_pass)

    _logger.debug(_gc("ly") + ' * Calculating image size...', end='')
    # Calculates a suitable width and height for image
    data, width, height = calculate_size(data, mode)
    _logger.debug('\r' + _gc("lg") + ' = Image size calculated.')

    # Creates a new empty image
    image = _Image.new('RGBA' if mode == 4 else 'RGB', (width, height))
    # Loads image pixel map
    pixel_map = image.load()
    x = 0
    _logger.debug(_gc("ly") + ' * Coloring pixels...', end='')
    if mode == 3:
        # Stores 3 bytes of data in each pixel of the image
        for i in range(image.width):
            for j in range(image.height):
                pixel_map[i, j] = (data[x], data[x + 1], data[x + 2])
                x += 3
    elif mode == 4:
        # Stores 4 bytes of data in each pixel of the image
        for i in range(image.width):
            for j in range(image.height):
                pixel_map[i, j] = (data[x], data[x + 1], data[x + 2], data[x + 3])
                x += 4
    _logger.debug('\r' + _gc("lg") + ' = Pixels colored.')

    # Saves image in the destination path
    image.save(dest, format='png')
    _logger.info(_gc("lg") + ' = Image saved.')

    if delete_source:
        # Removes Source file
        _delete_source_file(source)


# Reads pixels and returns data
def read_pixels(image: _Image):
    # Loads image pixel map
    pixel_map = image.load()

    mode = len(pixel_map[0, 0])

    _logger.debug(_gc("ly") + ' * Reading pixels...', end='')
    data = b''
    if mode == 4:
        for i in range(image.width):
            tmp = b''
            for j in range(image.height):
                # Reads a pixel
                # Appends 4 bytes to the temporarily data
                tmp += pixel_map[i, j][0].to_bytes(1, 'little') + pixel_map[i, j][1].to_bytes(1, 'little') + \
                       pixel_map[i, j][2].to_bytes(1, 'little') + pixel_map[i, j][3].to_bytes(1, 'little')
            # Appends the temporarily data to the data
            data += tmp
            # Shows the reading progress in console
            _logger.info('\r' + _gc("ly") + f' * Reading pixels({(i / image.width * 10000) // 1 / 100}%)...', end='')
    elif mode == 3:
        for i in range(image.width):
            tmp = b''
            for j in range(image.height):
                # Reads a pixel
                # Appends 3 bytes to the temporarily data
                tmp += pixel_map[i, j][0].to_bytes(1, 'little') + pixel_map[i, j][1].to_bytes(1, 'little') + \
                       pixel_map[i, j][2].to_bytes(1, 'little')
            # Appends the temporarily data to the data
            data += tmp
            # Shows the reading progress in console
            _logger.info('\r' + _gc("ly") + f' * Reading pixels({(i / image.width * 10000) // 1 / 100}%)...', end='')
    _logger.info('\r' + _gc("lg") + ' = Data loaded.')

    _logger.debug(_gc("ly") + ' * Correcting data...', end='')
    # Removes all empty bytes at the end of the data
    while data.endswith(b'\x00'):
        data = data[:-1]
    data = data[:-1]
    _logger.debug('\r' + _gc("lg") + ' = Data is ready.')
    return data


# Extract a file from an image pixels
def from_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Reads the image file
    _logger.debug(_gc("ly") + ' * Opening image...', end='')
    image = _Image.open(source)
    _logger.debug('\r' + _gc("lg") + ' = Image opened.')

    # Reads pixels and returns data
    data = read_pixels(image)

    # Prepares extracted data
    data = _prepare_data(data, False, compress, encrypt_pass)

    # Saves the data in the destination path
    _save_file(dest, data)

    if delete_source:
        # Removes Source file
        _delete_source_file(source)
