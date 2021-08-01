# Functions

import os
import sys
# We use zlib library to compress and decompress data
import zlib
# We use hashlib library to hash passwords
import hashlib
# We use zipfile library to embed files
import zipfile
# We use magic to check file type
import magic
# We use getoutput function to get the output of a command
from subprocess import getoutput
# We use AnsiToWin32 class to write colorful texts in windows console
from colorama import AnsiToWin32 as AnsiToWin
# We use AES to encrypt and decrypt data
from Crypto.Cipher import AES
# We use Image to convert data into image
from PIL import Image
# `is_windows` is a boolean that is True if the operating system is Windows
# `Colors` is a class that let us access Ansi color codes easily
# `verbose` and `quiet` are boolean variables
from .variables import is_windows, Colors, embed_capable

# All of the methods that can be imported
__all__ = ['print', 'printv', 'input', 'exit', 'win_embed', 'win_extract', 'win_attrib_hide', 'win_attrib_reveal',
           'to_image', 'from_image', 'embed', 'extract', 'quiet', 'verbose']

_verbose = False
_quiet = False

# Sets write_text function depending on operating system
ATW = AnsiToWin(sys.stdout)
if is_windows:
    write_text = ATW.write_and_convert
else:
    write_text = ATW.write

# Backups input function
input_backup = input


# Colorful print
def print(*args, end='\n', reset_color: bool = True) -> None:
    if _quiet:
        return
    text = ' '.join([str(arg) for arg in args] + [str(end)])
    if reset_color:
        text += Colors.Default
    if text.startswith('\r'):
        write_text('\r' + ' ' * (os.get_terminal_size()[0] - 1) + '\r')
    write_text(text)


def printv(*args, end='\n') -> None:
    if _verbose:
        print(*args, end=end)


# Colorful input
def input(*args, end='') -> str:
    print(*args, end=end)
    return input_backup('')


# Exits
def exit(*args) -> None:
    if args:
        print(*args)
    print(end=Colors.Default)
    sys.exit()


# Enables verbose mode
def verbose() -> bool:
    global _verbose
    _verbose = True
    return _verbose


# Enables quiet mode
def quiet() -> bool:
    global _quiet
    _quiet = True
    return _quiet


# Encrypts data using AES and costume password
def encrypt(data: bytes, password: str) -> bytes:
    printv(Colors.Yellow + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    printv(Colors.Yellow + ' * Encrypting data...', end='')
    cipher = AES.new(md5, AES.MODE_EAX, nonce=sha512)
    data = cipher.encrypt(data)
    printv('\r' + Colors.Green + ' = Data encrypted.')
    return data


# Decrypts data using AES and costume password
def decrypt(data: bytes, password: str) -> bytes:
    printv(Colors.Yellow + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    printv(Colors.Yellow + ' * Decrypting data...', end='')
    cipher = AES.new(md5, AES.MODE_EAX, nonce=sha512)
    data = cipher.decrypt(data)
    printv('\r' + Colors.Green + ' = Data decrypted.')
    return data


# Prepares data(compression and encryption)
def prepare_data(data: bytes, hiding: bool = True, compress: bool = False, encrypt_pass: str = None) -> bytes:
    if hiding:
        if compress:
            printv(Colors.Yellow + ' * Compressing data...', end='')
            data = zlib.compress(data)
            printv('\r' + Colors.Green + ' = Data compressed.')
        if encrypt_pass:
            data = encrypt(data, encrypt_pass)
    else:
        if encrypt_pass:
            data = decrypt(data, encrypt_pass)
        if compress:
            printv(Colors.Yellow + ' * Trying to decompress data...', end='')
            try:
                data = zlib.decompress(data)
                printv('\r' + Colors.Green + ' = Data decompressed.')
            except zlib.error:
                exit('\r' + Colors.Red +
                     " ! Error: Couldn't decompress!\n + Data may not be compressed or may be encrypted.")
    return data


# Opens a file and returns prepared content
def open_file(path: str, name: str, hiding: bool = True, compress: bool = False, encrypt_pass: str = None) -> bytes:
    printv(Colors.Yellow + f' * Reading {name.lower()} file...', end='')
    with open(path, 'rb') as file:
        data = file.read()
    printv('\r' + Colors.Green + f' = {name.capitalize()} file opened.')
    return prepare_data(data, hiding, compress, encrypt_pass)


# Writes data in the given path
def save_file(path: str, data: bytes) -> None:
    printv(Colors.Yellow + ' * Writing in destination file...', end='')
    with open(path, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = File saved.')


# Deletes the file in the given path
def delete_source_file(path: str) -> None:
    printv(Colors.Yellow + ' * Deleting source file...', end='')
    os.remove(path)
    printv('\r' + Colors.Yellow + ' = Source file deleted')


# Returns the possible names of the embedded files in a windows path
def get_names(path: str) -> list:
    output = getoutput('dir ' + os.path.split(path)[0] + ' /r /a')
    names = []
    for line in output.split('\n'):
        if line.endswith(':$DATA'):
            if line[39:].startswith(os.path.split(path)[1]):
                names.append(line[39:].split(':')[1])
    return names


# Adds a numeric identifier
def add_num(name: str):
    n = ''
    extension = ''
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
    return name + str(n) + extension


# Hides a file in another windows file
def win_embed(source: str, dest: str, delete_source: bool, compress: bool, cover: str = None,
              encrypt_pass=None) -> None:
    # Gets the list of available embedded names in the destination path
    names = get_names(dest)
    # Generates a default name
    default_name = os.path.split(source)[1]
    # Makes sure that default name is unique
    while default_name in names:
        default_name = add_num(default_name)

    while True:
        # Gets name from user
        name = input(Colors.Yellow + f' * Enter a name for embedded file' + Colors.White +
                     f'({Colors.Pink}Default{Colors.Red}: {Colors.Cyan}{default_name}{Colors.White}){Colors.Red}: '
                     + Colors.Green)
        if name in names:
            # Makes sure that user wants to replace the existing file
            conform = input(Colors.Yellow + f' * `{Colors.Cyan}{default_name}{Colors.Yellow}` already exists!' +
                            '\n * Do you want to replace it?' +
                            f'{Colors.White}({Colors.Red}y{Colors.White}/{Colors.Green}N{Colors.White}) ' +
                            Colors.Green).lower()
            if conform == 'n':
                continue
        break
    # Sets name to default_name value
    if not name:
        name = default_name

    printv(Colors.Yellow + ' * Preparing path...', end='')
    if cover:
        # Writes the cover data in the destination path
        with open(cover, 'rb') as cover_file:
            with open(dest, 'wb') as dest_file:
                dest_file.write(cover_file.read())
    elif not os.path.exists(dest):
        # Creates an empty file in the destination path
        with open(dest, 'w') as dest_file:
            dest_file.write('')
    printv('\r' + Colors.Green + ' = File is ready.')

    # Reads and prepares the source data
    data = open_file(source, 'source', True, compress, encrypt_pass)

    # Saves the prepared data
    save_file(dest + ':' + name, data)

    if delete_source:
        # Removes Source file
        delete_source_file(source)


# Extracts a hidden file from a file in windows
def win_extract(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Gets the list of available embedded names in destination path
    possible_names = get_names(source)
    name = ''
    if len(possible_names) == 0:
        # Exits if no embedded file is available
        exit(Colors.Red + ' ! Error: No embedded file found!')
    elif len(possible_names) == 1:
        # Choose the only embedded file automatically
        name = possible_names[0]
    else:
        # Asks user to choose one of the embedded files
        while name not in possible_names:
            print(Colors.Blue + 'Available names' + Colors.Red + ': ' + Colors.Green +
                  f'{Colors.Red}, {Colors.Green}'.join(possible_names))
            name = input(Colors.Yellow + f'Enter the name of embedded file' + Colors.Red + ': ' + Colors.Green)

    # Reads and prepares data
    data = open_file(source + ':' + name, 'source', False, compress, encrypt_pass)

    # Saves the prepared data in the destination path
    save_file(dest, data)

    if delete_source:
        # Removes Source file
        delete_source_file(source)


# Changes a file windows attributes to not be show in windows explorer
def win_attrib_hide(path: str) -> None:
    print(Colors.Yellow + ' * Running `attrib` command...', end='')
    # Runs Windows attrib command
    # +h : Adds Hidden File attribute
    # -a : Removes Archive File attribute
    # +s : Adds System File attribute
    os.system('attrib +h -a +s "' + path + '"')
    print('\r' + Colors.Green + ' = Done.')


# Changes a file windows attributes to be shown ib=n windows explorer
def win_attrib_reveal(path: str) -> None:
    print(Colors.Yellow + ' * Running `attrib` command...', end='')
    # Runs Windows attrib command
    # -h : Removes Hidden File attribute
    # +a : Adds Archive File attribute
    # -s : Removes System File attribute
    os.system('attrib -h +a -s "' + path + '"')
    print('\r' + Colors.Green + ' = Done.')


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


# Convert a file to an image
def to_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Reads and prepares the source file data
    data = open_file(source, 'source', True, compress, encrypt_pass)

    printv(Colors.Yellow + ' * Calculating image size...', end='')
    # Calculates a suitable width and height for image
    while True:
        length = len(data)
        if length % 4 != 0:
            data += b'\x00'
            continue
        length /= 4
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
    printv('\r' + Colors.Green + ' = Image size calculated.')

    # Creates a new empty image
    image = Image.new('RGBA', (width, height))
    # Loads image pixel map
    pixel_map = image.load()
    x = 0
    printv(Colors.Yellow + ' * Coloring pixels...', end='')
    # Stores 4 bytes of data in each pixel of the image
    for i in range(image.width):
        for j in range(image.height):
            pixel_map[i, j] = (data[x], data[x + 1], data[x + 2], data[x + 3])
            x += 4
    printv('\r' + Colors.Green + ' = Pixels colored.')

    # Saves image in the destination path
    image.save(dest, format='png')
    print(Colors.Green + ' = Image saved.')

    if delete_source:
        # Removes Source file
        delete_source_file(source)


# Extract a file from an image pixels
def from_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Reads the image file
    printv(Colors.Yellow + ' * Opening image...', end='')
    image = Image.open(source)
    printv('\r' + Colors.Green + ' = Image opened.')

    printv(Colors.Yellow + ' * Reading pixels...', end='')
    # Loads image pixel map
    pixel_map = image.load()
    data = b''
    try:
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
            print('\r' + Colors.Yellow + f' * Reading pixels({(i / image.width * 10000) // 1 / 100}%)...', end='')
    except IndexError:
        exit('\r' + Colors.Red +
             " ! Error: Source image doesn't have ALFA!\n + Image may be compressed by a messaging application.")
    print('\r' + Colors.Green + ' = Data loaded.')

    printv(Colors.Yellow + ' * Correcting data...', end='')
    # Removes all empty bytes at the end of the data
    while data.endswith(b'\x00'):
        data = data[:-1]
    printv('\r' + Colors.Green + ' = Data is ready.')

    # Prepares extracted data
    data = prepare_data(data, False, compress, encrypt_pass)

    # Saves the data in the destination path
    save_file(dest, data)

    if delete_source:
        # Removes Source file
        delete_source_file(source)


# Embeds a file in a cover
def embed(source: str, cover: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    # Reads cover file content
    data = open_file(cover, 'cover')

    printv(Colors.Yellow + ' * Checking cover file type...', end='')
    # Checks cover file type
    try:
        cover_type = magic.from_buffer(data)
        valid = False
        for t in embed_capable:
            if t.lower() in cover_type.lower():
                valid = True
    except magic.magic.MagicException:
        valid = True
    if not valid:
        exit('\r' + Colors.Red + " ! Error: Cover File Type(" + cover_type + ") is not supported!")
    printv('\r' + Colors.Green + ' = Cover file is valid.')

    # Reads and prepares source data
    source_data = open_file(source, 'source', True, compress, encrypt_pass)

    printv(Colors.Yellow + ' * Making an archive...', end='')
    # Generates a name for a temporarily zip archive
    archive_tmp_path = 'tmp.zip'
    while os.path.exists(archive_tmp_path):
        archive_tmp_path = add_num(archive_tmp_path)
    # Makes a zip archive
    archive = zipfile.ZipFile(archive_tmp_path, 'w')
    # Writes prepared source data in the zip archive
    archive.writestr(os.path.split(source)[1], source_data)
    # Closes the archive
    archive.close()
    printv('\r' + Colors.Green + ' = Archive made.')

    printv(Colors.Yellow + ' * Reading archive...', end='')
    # Reads the archive data
    with open(archive_tmp_path, 'rb') as archive_file:
        archive_data = archive_file.read()
    printv('\r' + Colors.Green + ' = Archive opened.')
    # Appends the archive data to the cover data
    data += archive_data
    printv(Colors.Yellow + ' * Removing temp archive...', end='')
    # Removes temporarily zip archive file
    os.remove(archive_tmp_path)
    printv('\r' + Colors.Green + ' = Temp file removed.')

    # Saves the prepared data in the destination path
    save_file(dest, data)

    if delete_source:
        # Removes Source file
        delete_source_file(source)


# Extracts a file from an embedded file
def extract(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None) -> None:
    printv(Colors.Yellow + ' * Opening file...', end='')
    # Opens the source file as a zip archive
    archive = zipfile.ZipFile(source)
    # Reads the hidden data from the source file
    with archive.open(archive.filelist[0], 'r') as source_file:
        data = source_file.read()
    # Closes the archive
    archive.close()
    printv('\r' + Colors.Green + ' = Source file opened.')

    # Prepares the data
    data = prepare_data(data, False, compress, encrypt_pass)

    # Saves the extracted data in the destination path
    save_file(dest, data)

    if delete_source:
        # Removes Source file
        delete_source_file(source)
