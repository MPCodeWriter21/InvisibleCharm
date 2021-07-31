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
# We use uuid4 function to generate unique IDs
from uuid import uuid4
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
from .variables import is_windows, Colors, embed_capable, verbose as _verbose, quiet as _quiet

# All of the methods that can be imported
__all__ = ['print', 'printv', 'input', 'exit', 'win_embed', 'win_extract', 'win_attrib_hide', 'win_attrib_reveal',
           'to_image', 'from_image', 'embed', 'extract', 'quiet', 'verbose']

# Sets write_text function depending on operating system
ATW = AnsiToWin(sys.stdout)
if is_windows:
    write_text = ATW.write_and_convert
else:
    write_text = ATW.write

# Backups input function
inputbackup = input


# Colorful print
def print(*args, end='\n', reset_color: bool = True):
    if _quiet:
        return
    text = ' '.join([str(arg) for arg in args] + [str(end)])
    if reset_color: text += Colors.Default
    if text.startswith('\r'):
        write_text('\r' + ' ' * (os.get_terminal_size()[0] - 1) + '\r')
    write_text(text)


def printv(*args, end='\n'):
    if _verbose:
        print(*args, end=end)


# Colorful input
def input(*args, end=''):
    print(*args, end=end)
    return inputbackup('')


# Exits
def exit(*args):
    if args:
        print(*args)
    print(end=Colors.Default)
    sys.exit()


# Enables verbose mode
def verbose():
    global _verbose
    _verbose = True


# Enables quiet mode
def quiet():
    global _quiet
    _quiet = True


# Encrypts data using AES and costume password
def encrypt(data: bytes, password: str):
    printv(Colors.Yellow + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    printv(Colors.Yellow + ' * Encrypting data...', end='')
    cipher = AES.new(md5, AES.MODE_EAX, nonce=sha512)
    data = cipher.encrypt(data)
    printv('\r' + Colors.Green + ' = Data encrypted.')
    return data


# Decrypts data using AES and costume password
def decrypt(data: bytes, password: str):
    printv(Colors.Yellow + ' * Hashing password...')
    md5 = hashlib.md5(password.encode()).digest()
    sha512 = hashlib.sha512(password.encode()).digest()
    printv(Colors.Yellow + ' * Decrypting data...', end='')
    cipher = AES.new(md5, AES.MODE_EAX, nonce=sha512)
    data = cipher.decrypt(data)
    printv('\r' + Colors.Green + ' = Data decrypted.')
    return data


def win_embed(name: str, source: str, dest: str, delete_source: bool, compress: bool, cover: str = None,
              encrypt_pass=None):
    printv(Colors.Yellow + ' * Copying cover file...', end='')
    if cover:
        with open(cover, 'rb') as cover_file:
            with open(dest, 'wb') as dest_file:
                dest_file.write(cover_file.read())
    elif not os.path.exists(dest):
        with open(dest, 'w') as dest_file:
            dest_file.write('')
    printv('\r' + Colors.Green + ' = Cover file copied.')
    printv(Colors.Yellow + ' * Reading source file...', end='')
    with open(source, 'rb') as source_file:
        data = source_file.read()
    printv('\r' + Colors.Green + ' = Source file opened.')
    if compress:
        printv(Colors.Yellow + ' * Compressing data...', end='')
        data = zlib.compress(data)
        printv('\r' + Colors.Green + ' = Data compressed.')
    if encrypt_pass:
        data = encrypt(data, encrypt_pass)

    printv(Colors.Yellow + ' * Writing in destination file...', end='')
    with open(dest + ':' + name, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = File embedded.')

    if delete_source:
        printv(Colors.Yellow + ' * Removing source file...')
        os.remove(source)
        printv(Colors.Yellow + ' = Source file removed.')


def get_names(path: str):
    output = getoutput('dir ' + os.path.split(path)[0] + ' /r /a')
    names = []
    for line in output.split('\n'):
        if line.endswith(':$DATA'):
            if line[39:].startswith(os.path.split(path)[1]):
                names.append(line[39:].split(':')[1])
    return names


def win_extract(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None):
    possible_names = get_names(source)
    name = ''
    if len(possible_names) == 0:
        exit(Colors.Red + ' ! Error: No embedded file found!')
    elif len(possible_names) == 1:
        name = possible_names[0]
    else:
        while name not in possible_names:
            print(
                Colors.Blue + 'Available names' + Colors.Red + ': ' + Colors.Green + f'{Colors.Red}, {Colors.Green}'.join(
                    possible_names))
            name = input(Colors.Yellow + f'Enter the name of embedded file' + Colors.Red + ': ' + Colors.Green)
    printv(Colors.Yellow + ' * Reading source file...', end='')
    with open(source + ':' + name, 'rb') as source_file:
        data = source_file.read()
    printv('\r' + Colors.Green + ' = Source file opened.')
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

    printv(Colors.Yellow + ' * Writing in destination file...', end='')
    with open(dest, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = Revealed.')

    if delete_source:
        printv(Colors.Yellow + ' * Removing source file...', end='')
        os.remove(source)
        printv('\r' + Colors.Yellow + ' = Source file removed.')


def win_attrib_hide(path: str):
    print(Colors.Yellow + ' * Running `attrib` command...', end='')
    os.system('attrib +h -a +s "' + path + '"')
    print('\r' + Colors.Green + ' = Done.')


def win_attrib_reveal(path: str):
    print(Colors.Yellow + ' * Running `attrib` command...', end='')
    os.system('attrib -h +a -s "' + path + '"')
    print('\r' + Colors.Green + ' = Done.')


def vmm(n: int):
    ns = []
    for i in range(2, int(n ** 0.5)):
        if n % i == 0:
            ns.append(i)
    if len(ns) == 0:
        return 0
    return ns[-1]


def to_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None):
    printv(Colors.Yellow + ' * Reading source file...', end='')
    with open(source, 'rb') as source_file:
        data = source_file.read()
    printv('\r' + Colors.Green + ' = Source file opened.')
    if compress:
        printv(Colors.Yellow + ' * Compressing data...', end='')
        data = zlib.compress(data)
        printv('\r' + Colors.Green + ' = Data compressed.')
    if encrypt_pass:
        data = encrypt(data, encrypt_pass)
    printv(Colors.Yellow + ' * Calculating image size...', end='')
    while True:
        length = len(data)
        if length % 4 != 0:
            data += b'\x00'
            continue
        length /= 4
        if vmm(length) == 0:
            data += b'\x00'
            continue
        p2 = vmm(length)
        p1 = length // p2
        tmp1 = min(p1, p2)
        tmp2 = max(p1, p2)
        p1 = int(tmp1)
        p2 = int(tmp2)
        if p2 - p1 > 5000:
            data += b'\x00'
            continue
        break
    printv('\r' + Colors.Green + ' = Image size calculated.')

    image = Image.new('RGBA', (p1, p2))
    pixel_map = image.load()
    x = 0
    printv(Colors.Yellow + ' * Coloring pixels...', end='')
    for i in range(image.width):
        for j in range(image.height):
            pixel_map[i, j] = (data[x], data[x + 1], data[x + 2], data[x + 3])
            x += 4
    printv('\r' + Colors.Green + ' = Pixels colored.')

    image.save(dest, format='png')
    print(Colors.Green + ' = Image saved.')

    if delete_source:
        printv(Colors.Yellow + ' * Deleting source file...', end='')
        os.remove(source)
        printv('\r' + Colors.Yellow + ' = Source file deleted')


def from_image(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None):
    printv(Colors.Yellow + ' * Opening image...', end='')
    image = Image.open(source)
    printv('\r' + Colors.Green + ' = Image opened.')
    data = b''
    printv(Colors.Yellow + ' * Reading pixels...', end='')
    pixel_map = image.load()
    try:
        for i in range(image.width):
            tmp = b''
            for j in range(image.height):
                tmp += pixel_map[i, j][0].to_bytes(1, 'little') + pixel_map[i, j][1].to_bytes(1, 'little') + \
                       pixel_map[i, j][2].to_bytes(1, 'little') + pixel_map[i, j][3].to_bytes(1, 'little')
            data += tmp
            printv('\r' + Colors.Yellow + f' * Reading pixels({(i/image.width*10000)//1/100}%)...', end='')
    except IndexError:
        exit('\r' + Colors.Red +
             " ! Error: Source image doesn't have ALFA!\n + Image may be compressed by a messaging application.")

    printv('\r' + Colors.Green + ' = Data loaded.')

    printv(Colors.Yellow + ' * Correcting data...', end='')
    while data.endswith(b'\x00'):
        data = data[:-1]
    printv('\r' + Colors.Green + ' = Data is ready.')

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
    printv(Colors.Yellow + ' * Saving data...', end='')
    with open(dest, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = Data saved.')

    if delete_source:
        printv(Colors.Yellow + ' * Deleting source file...', end='')
        os.remove(source)
        printv('\r' + Colors.Yellow + ' = Source file deleted')


def embed(source: str, cover: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None):
    printv(Colors.Yellow + ' * Reading cover file...', end='')
    with open(cover, 'rb') as cover_file:
        data = cover_file.read()
    printv('\r' + Colors.Green + ' = Cover file opened.')
    printv(Colors.Yellow + ' * Checking cover file type...', end='')
    cover_type = magic.from_buffer(data)
    valid = False
    for t in embed_capable:
        if t.lower() in cover_type.lower():
            valid = True
    if not valid:
        exit('\r' + Colors.Red + " ! Error: Cover File Type(" + cover_type + ") is not supported!")
    printv('\r' + Colors.Green + ' = Cover file is valid.')
    printv(Colors.Yellow + ' * Reading source file...', end='')
    with open(source, 'rb') as source_file:
        source_data = source_file.read()
    printv('\r' + Colors.Green + ' = Source file opened.')

    if compress:
        printv(Colors.Yellow + ' * Compressing data...', end='')
        source_data = zlib.compress(source_data)
        printv('\r' + Colors.Green + ' = Data compressed.')
    if encrypt_pass:
        source_data = encrypt(source_data, encrypt_pass)

    printv(Colors.Yellow + ' * Making an archive...', end='')
    archive_tmp_path = str(uuid4()) + 'tmp.zip'
    while os.path.exists(archive_tmp_path):
        archive_tmp_path = str(uuid4()) + archive_tmp_path
    archive = zipfile.ZipFile(archive_tmp_path, 'w')
    archive.writestr(os.path.split(source)[1], source_data)
    archive.close()
    printv('\r' + Colors.Green + ' = Archive made.')
    printv(Colors.Yellow + ' * Reading archive...', end='')
    with open(archive_tmp_path, 'rb') as archive_file:
        archive_data = archive_file.read()
    printv('\r' + Colors.Green + ' = Archive opened.')
    data += archive_data
    printv(Colors.Yellow + ' * Removing temp archive...', end='')
    os.remove(archive_tmp_path)
    printv('\r' + Colors.Green + ' = Temp file removed.')

    printv(Colors.Yellow + ' * Writing in destination...', end='')
    with open(dest, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = File saved.')

    if delete_source:
        printv(Colors.Yellow + ' * Deleting source file...', end='')
        os.remove(source)
        printv('\r' + Colors.Yellow + ' = Source file deleted')


def extract(source: str, dest: str, delete_source: bool, compress: bool, encrypt_pass=None):
    printv(Colors.Yellow + ' * Opening file...', end='')
    archive = zipfile.ZipFile(source)
    with archive.open(archive.filelist[0], 'r') as source_file:
        data = source_file.read()
    printv('\r' + Colors.Green + ' = Source file opened.')

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

    printv(Colors.Yellow + ' * Writing in destination...', end='')
    with open(dest, 'wb') as dest_file:
        dest_file.write(data)
    print('\r' + Colors.Green + ' = File saved.')

    if delete_source:
        printv(Colors.Yellow + ' * Deleting source file...', end='')
        os.remove(source)
        printv('\r' + Colors.Yellow + ' = Source file deleted')
