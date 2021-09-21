#!/bin/python3
# InvisibleCharm.__main__.py
# CodeWriter21

import os
from log21 import get_colors as gc
from log21 import ColorizingArgumentParser
from InvisibleCharm.Settings import banner, is_windows, operating_system
from InvisibleCharm.lib.Console import logger, input, verbose, quiet, exit
from InvisibleCharm.lib.operations import win_embed, win_extract, win_attrib_hide, win_attrib_reveal, to_image_file, \
    from_image_file, embed_file, extract_file


# Main function of script
def main():
    # Initializes the argument parser
    parser = ColorizingArgumentParser()

    # Adds commandline arguments to the parser
    parser.add_argument('mode', action='store', type=str, choices=['hide', 'reveal', 'h', 'r'],
                        help=f'{gc("lb")}modes{gc("lr")}:{gc("lg")} hide{gc("lr")},{gc("lg")} reveal' +
                             gc("rst"))
    parser.add_argument('--win-embed', '-we', action='store_true', dest='win_embed',
                        help=f'{gc("lg")}Embed files invisibly{gc("lw")}\
                            ({gc("ly")}Only works on Windows{gc("lw")})' + gc("rst"))
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
    parser.add_argument('--dest-file', '-d', action='store', type=str, dest='destination',
                        help=f'Sets the path of {gc("lg")}DESTINATION{gc("rst")} file')
    parser.add_argument('--delete-source', '-D', action='store_true', dest='delete',
                        help=gc("lr") + 'Deletes source file' + gc("rst"))
    parser.add_argument('--compress', '-C', action='store_true', dest='compress')
    parser.add_argument('--encrypt', '-E', action='store', type=str, dest='encryption_pass',
                        help=f'Enables {gc("lb")}encryption{gc("rst")} \
                        - needs an {gc("lg")}ENCRYPTION_PASSword' + gc("rst"))
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose')
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet')
    args = parser.parse_args()

    # Prints banner
    logger.info(banner)

    # Checks for verbose and quiet switches
    if args.verbose:
        verbose()
    if args.quiet:
        quiet()

    # Checks for switches to be suitable
    if not (args.win_embed or args.win_attrib or args.embed or args.to_image):
        exit(gc("lr") + ' ! Error: No operation chosen\n + Please choose an operation like embed!')
    if not is_windows and (args.win_embed or args.win_attrib):
        exit(gc("lr") + f" ! Error: You can't use windows-only options in {operating_system}")
    if args.embed and args.win_embed:
        exit(gc("lr") + " ! Error: You can't use embed and win-embed at the same time!")
    if args.to_image and args.embed:
        exit(gc("lr") + " ! Error: You can't use embed and to-image at the same time!")
    if args.to_image and args.win_embed:
        exit(gc("lr") + " ! Error: You can't use win-embed and to-image at the same time!")
    if not args.source or not os.path.exists(args.source) or not os.path.isfile(args.source):
        exit(gc("lr") + f" ! Error: Couldn't find source file: {os.path.abspath(args.source)}" +
             f"\n + Source file must be an existing file!")
    if (args.win_embed or args.to_image or args.embed) and not args.destination:
        exit(gc("lr") + " ! Error: You must set destination path for this operation. use: --dest-file/-d")
    if args.to_image and args.image_mode not in [3, 4]:
        exit(gc("lr") + f' ! Error: Image Mode: `{gc("lw")}{args.image_mode}{gc("lr")}` not found!\n' +
             f' + Valid values:{gc("lb")} 3{gc("lr")},{gc("lb")} 4')

    if args.destination:
        # Makes sure that destination directory exists
        try:
            if os.path.split(args.destination)[0]:
                os.makedirs(os.path.split(args.destination)[0])
        except FileExistsError:
            pass

    # Checks the chosen mode
    if args.mode.lower() in ['hide', 'h']:
        # Checks the chosen operation and calls the suitable function
        if args.win_embed:
            if not args.cover and not os.path.exists(args.destination):
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            'You could add a cover file using --cover-file/-c switches.' + gc("rst"))
            win_embed(args.source, args.destination, args.delete, args.compress, args.cover, args.encryption_pass)
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
            to_image_file(args.source, args.destination, args.delete, args.compress, args.encryption_pass, args.image_mode)
        elif args.embed:
            if not args.cover or not os.path.exists(args.cover) or not os.path.isfile(args.cover):
                exit(gc("lr") + ' ! Error: Embed operation needs a cover file' +
                     '\n + Source file must be an existing file!')
            embed_file(args.source, args.cover, args.destination, args.delete, args.compress, args.encryption_pass)
    elif args.mode.lower() in ['reveal', 'r']:
        # Checks the chosen operation and calls the suitable function
        if args.cover:
            logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                        "`reveal` operations don't use cover file." + gc("rst"))
        if args.win_embed:
            if args.delete:
                answer = ''
                while answer != 'y' and answer != 'n':
                    answer = input(
                        gc("ly") + f'Are you sure you want to remove source file({args.source})?(y/N) ' +
                        gc("lg"))
                args.delete = answer == 'y'
            win_extract(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
        elif args.win_attrib:
            if args.destination:
                logger.warn(gc("lr") + ' ! Warning: ' + gc("blm", "gr") +
                            "`win attrib` operation doesn't use destination file path." + gc("rst"))
            win_attrib_reveal(args.source)
        elif args.to_image:
            from_image_file(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
        elif args.embed:
            extract_file(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
    else:
        exit(gc("lr") + f' ! Error: Mode: `{gc("lw")}{args.mode}{gc("lr")}` not found!')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('\r' + gc("lr") + ' ! Error: Keyboard Interrupt: User canceled operation')
