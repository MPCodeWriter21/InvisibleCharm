#!/bin/python3
# InvisibleCharm.__main__.py
# CodeWriter21

import os
from getpass import getpass

import PIL

from Crypto.PublicKey import RSA
from log21 import get_colors as gc, ColorizingArgumentParser

from InvisibleCharm.Settings import banner, is_windows, operating_system
from InvisibleCharm.lib.Console import logger, input, verbose, quiet, exit
from InvisibleCharm.lib.operations import ntfs_embed, win_extract, win_attrib_hide, win_attrib_reveal, to_image_file, \
    from_image_file, embed_file, extract_file
from InvisibleCharm.lib.Exceptions import CoverDataTypeNotFoundError, InvalidCoverDataTypeError, \
    NoEmbeddedFileFoundError
from InvisibleCharm.lib.File import get_names


def generate_destination_path(source_path: str, extension: str = None):
    """
    Generates a destination path based on the source path.
    :param source_path: The source path.
    :param extension: The extension to use.
    :return: The destination path.
    """
    directory = os.path.dirname(source_path)
    name, ext = os.path.splitext(os.path.basename(source_path))
    dest_path = os.path.join(directory, name + '{}' + (extension if extension is not None else ext))
    number = ''
    if os.path.exists(dest_path.format(number)):
        i = 1
        while os.path.exists(dest_path.format(str(i))):
            i += 1
        number = str(i)

    return dest_path.format(number)


# Main function of script
def main():
    # Initializes the argument parser
    parser = ColorizingArgumentParser()

    # Adds commandline arguments to the parser
    parser.add_argument('mode', action='store', type=str, choices=['hide', 'reveal', 'h', 'r'],
                        help=f'{gc("lb")}modes{gc("lr")}:{gc("lg")} hide{gc("lr")},{gc("lg")} reveal' +
                             gc("rst"))
    parser.add_argument('--ntfs-embed', '-we', action='store_true', dest='ntfs_embed',
                        help=f'{gc("lg")}Embed files invisibly{gc("lw")}\
                            ({gc("ly")}Only works on NTFS file system{gc("lw")})' + gc("rst"))
    parser.add_argument('--win-attribute', '-wa', action='store_true', dest='win_attrib',
                        help=gc("lg") + 'Change windows attributes to hide file' + gc("rst"))
    parser.add_argument('--embed', '-e', action='store_true', dest='embed', help='')
    parser.add_argument('--to-image', '-i', action='store_true', dest='to_image',
                        help=gc("lg") + f'Converts a file into a {gc("lm")}png image' + gc("rst"))
    parser.add_argument('--image-mode', '-I', action='store', type=int, choices=[3, 4], dest='image_mode', default=3,
                        help=f'Sets output image mode.\n' + gc("rst") +
                             f'Valid values{gc("lr")}:{gc("lb")} 3{gc("lr")}:{gc("lb")}RGB' + gc("lr") +
                             f',{gc("lb")} 4{gc("lr")}:{gc("lb")}ARGB' + gc("rst"))
    parser.add_argument('--source-file', '-s', action='store', type=str, dest='source',
                        help=f'Sets the path of {gc("lg")}SOURCE{gc("rst")} file', required=True)
    parser.add_argument('--cover-file', '-c', action='store', type=str, dest='cover',
                        help=f'Sets the path of {gc("lg")}COVER{gc("rst")} file')
    parser.add_argument('--dest-file', '-d', '-o', action='store', type=str, dest='destination',
                        help=f'Sets the path of {gc("lg")}DESTINATION{gc("rst")} file')
    parser.add_argument('--delete-source', '-D', action='store_true', dest='delete',
                        help=gc("lr") + 'Deletes source file' + gc("rst"))
    parser.add_argument('--compress', '-C', action='store_true', dest='compress')
    parser.add_argument('--encrypt-aes', '-aes', action='store_true', dest='aes_encryption',
                        help=f'Enables {gc("lb")}AES encryption{gc("rst")} \
                        - Asks for an {gc("lg")}ENCRYPTION_PASSword' + gc("rst"))
    parser.add_argument('--encrypt-aes-pass', '-aes-pass', action='store', type=str, dest='aes_encryption_pass',
                        help=f'Enables {gc("lb")}AES encryption{gc("rst")} \
                        - Needs an {gc("lg")}ENCRYPTION_PASSword' + gc("rst"))
    parser.add_argument('--encrypt-rsa', '-rsa', action='store', type=str, dest='rsa_encryption_key',
                        help=f'Enables {gc("lb")}RSA encryption{gc("rst")} \
                        - Needs a path to a {gc("lg")}RSA private/public key' + gc("rst"))
    parser.add_argument('--rsa-key-passphrase', '-rsa-pass', action='store', type=str, dest='rsa_key_pass',
                        help=f'A passphrase to decrypt the input RSA private key.' + gc("rst"))
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose',
                        help=gc("lg") + 'Verbose mode' + gc("rst"))
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet', help=gc("lg") + 'Quiet mode' + gc("rst"))
    args = parser.parse_args()

    # Prints banner
    logger.info(banner)

    # Checks for verbose and quiet switches
    if args.verbose:
        verbose()
    if args.quiet:
        quiet()

    # Checks for switches to be suitable
    if not (args.ntfs_embed or args.win_attrib or args.embed or args.to_image):
        exit(gc("lr") + ' ! Error: No operation chosen\n + Please choose an operation like embed!')
    if not is_windows and (args.ntfs_embed or args.win_attrib):
        exit(gc("lr") + f" ! Error: You can't use windows-only options in {operating_system}")
    if args.embed and args.ntfs_embed:
        exit(gc("lr") + " ! Error: You can't use embed and win-embed at the same time!")
    if args.to_image and args.embed:
        exit(gc("lr") + " ! Error: You can't use embed and to-image at the same time!")
    if args.to_image and args.ntfs_embed:
        exit(gc("lr") + " ! Error: You can't use win-embed and to-image at the same time!")
    if not args.source or not os.path.exists(args.source) or not os.path.isfile(args.source):
        exit(gc("lr") + f" ! Error: Couldn't find source file: {os.path.abspath(args.source)}" +
             f"\n + Source file must be an existing file!")
    if args.to_image and args.image_mode not in [3, 4]:
        exit(gc("lr") + f' ! Error: Image Mode: `{gc("lw")}{args.image_mode}{gc("lr")}` not found!\n' +
             f' + Valid values:{gc("lb")} 3{gc("lr")},{gc("lb")} 4')

    if (args.ntfs_embed or args.to_image or args.embed) and not args.destination:
        logger.warning(gc("lr") + " ! Warning: You should set destination path for this operation. use: --dest-file/-d")
        logger.info(gc('ly') + " = Generating a destination path to save the output...")
        if args.mode.lower() in ['hide', 'h']:
            if args.to_image:
                args.destination = generate_destination_path(args.source, '.png')
            else:
                args.destination = generate_destination_path(args.source)
        elif args.mode.lower() in ['reveal', 'r']:
            args.destination = generate_destination_path(args.source, '')

    if args.destination:
        # Makes sure that destination directory exists
        if os.path.split(args.destination)[0]:
            os.makedirs(os.path.split(args.destination)[0], exist_ok=True)

    # Takes a password from user if encryption is enabled and no password is given
    if args.aes_encryption and not args.aes_encryption_pass:
        args.aes_encryption_pass = getpass(" * Enter a password for AES encryption: ")

    # Reads the RSA key file if given
    rsa_key = None
    if args.rsa_encryption_key:
        if not os.path.exists(args.rsa_encryption_key):
            exit(gc("lr") + f" ! Error: Couldn't find RSA key file: '{args.rsa_encryption_key}'" +
                 f"\n + RSA key file must be an existing file!")
        with open(args.rsa_encryption_key, 'rb') as file:
            key = file.read()
            try:
                rsa_key = RSA.import_key(key, args.rsa_key_pass)
            except ValueError:
                logger.error(gc('lr') + ' ! Error: Input key is unsupported or password protected!')
                password = getpass(" * Enter the password of the encrypted key: ")
                if password:
                    try:
                        rsa_key = RSA.import_key(key, password)
                    except ValueError:
                        logger.error(gc('lr') + ' ! Error: Input key is unsupported or the password is wrong!')
                        exit()
                else:
                    exit()

    if args.mode.lower() in ['hide', 'h'] and rsa_key and rsa_key.has_private():
        logger.warn(gc('lr') + ' ! Warning: The input RSA key is a private key!')
        if input(gc('ly') + f'Are you sure you want to encrypt the data using a private key?'
                            f'({gc("r")}y{gc("lr")}/{gc("lg")}N{gc("ly")}) {gc("lc")}').lower() == 'n':
            exit()

    if args.mode.lower() in ['reveal', 'r'] and rsa_key and not rsa_key.has_private():
        logger.error(gc('lr') + ' ! Error: The input RSA key is a not private key!')
        logger.info(gc('c') + 'You must use a private key for decryption!')
        exit()

    # Checks the chosen mode
    if args.mode.lower() in ['hide', 'h']:
        # Checks the chosen operation and calls the suitable function
        if args.ntfs_embed:
            if not args.cover and not os.path.exists(args.destination):
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            'You could add a cover file using --cover-file/-c switches.' + gc("rst"))
            ntfs_embed(args.source, args.destination, args.delete, args.compress, args.cover, args.aes_encryption_pass,
                       rsa_key)
            if args.win_attrib:
                win_attrib_hide(args.destination)
        elif args.win_attrib:
            if args.cover:
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            "`win attrib` operation doesn't use cover file." + gc("rst"))
            if args.destination:
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            "`win attrib` operation doesn't use destination file path." + gc("rst"))
            win_attrib_hide(args.source)
        elif args.to_image:
            if args.cover:
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            "`to image` operation doesn't use cover file." + gc("rst"))
            to_image_file(args.source, args.destination, args.delete, args.compress, args.aes_encryption_pass, rsa_key,
                          args.image_mode)
        elif args.embed:
            if not args.cover or not os.path.exists(args.cover) or not os.path.isfile(args.cover):
                exit(gc("lr") + ' ! Error: Embed operation needs a cover file' +
                     '\n + Source file must be an existing file!')
            try:
                embed_file(args.source, args.cover, args.destination, args.delete, args.compress,
                           args.aes_encryption_pass, rsa_key)
            except CoverDataTypeNotFoundError:
                confirm = input(gc("lr") + f" ! Error: Couldn't identify cover file type!\n" + gc("ly") +
                                ' * Do you still want to use this cover file?' + gc("lw") + '(' + gc("ly") +
                                f'Enter {gc("lm")}Y{gc("ly")} to confirm{gc("lw")}){gc("lr")}: '
                                + gc("lg")).lower()
                if confirm == 'y':
                    embed_file(args.source, args.cover, args.destination, args.delete, args.compress,
                               args.aes_encryption_pass, rsa_key, True)
                else:
                    exit()
            except InvalidCoverDataTypeError as ex:
                exit('\r' + gc("lr") + " ! Error:", str(ex))
    elif args.mode.lower() in ['reveal', 'r']:
        # Checks the chosen operation and calls the suitable function
        if args.cover:
            logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                        "`reveal` operations don't use cover file." + gc("rst"))
        if args.ntfs_embed:
            if args.delete:
                answer = ''
                while answer != 'y' and answer != 'n':
                    answer = input(
                        gc("ly") + f'Are you sure you want to remove source file({args.source})?(y/N) ' +
                        gc("lg"))
                args.delete = answer == 'y'
            # Gets the list of available embedded names in destination path
            possible_names = get_names(args.source)
            name = ''
            if len(possible_names) == 0:
                # Exits if no embedded file is available
                exit(gc("lr") + f' ! Error: No win-embedded file found!')
            elif len(possible_names) == 1:
                # Choose the only embedded file automatically
                name = possible_names[0]
            else:
                # Asks user to choose one of the embedded files
                while name not in possible_names:
                    logger.print(gc("lb") + 'Available names' + gc("lr") + ': ' + gc("lg") +
                                 f'{gc("lr")}, {gc("lg")}'.join(possible_names))
                    name = input(gc("ly") + f'Enter the name of embedded file' + gc("lr") + ': ' + gc("lg"))
            win_extract(args.source, args.destination, args.delete, args.compress, name, args.aes_encryption_pass,
                        rsa_key)
        elif args.win_attrib:
            if args.destination:
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            "`win attrib` operation doesn't use destination file path." + gc("rst"))
            win_attrib_reveal(args.source)
        elif args.to_image:
            try:
                from_image_file(args.source, args.destination, args.delete, args.compress, args.aes_encryption_pass,
                                rsa_key)
            except PIL.UnidentifiedImageError:
                exit(gc('lr') + "! Error: Couldn't identify image file type!")
        elif args.embed:
            try:
                extract_file(args.source, args.destination, args.delete, args.compress, args.aes_encryption_pass,
                             rsa_key)
            except NoEmbeddedFileFoundError:
                exit(gc("lr") + f' ! Error: No embedded file found!')
    else:
        exit(gc("lr") + f' ! Error: Mode: `{gc("lw")}{args.mode}{gc("lr")}` not found!')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('\r' + gc("lr") + ' ! Error: Keyboard Interrupt: User canceled operation')
