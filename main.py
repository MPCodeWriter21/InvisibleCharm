#!/usr/bin/python3
import os

from extra.imports import *


# Main function of script
def main():
    # Initializes the argument parser
    parser = argparse.ArgumentParser()

    # Adds commandline arguments to the parser
    parser.add_argument('mode', action='store', type=str,
                        help=f'{Colors.Blue}modes{Colors.Red}:{Colors.Green} hide{Colors.Red},{Colors.Green} reveal' +
                             Colors.Default)
    if is_windows:
        parser.add_argument('--win-embed', '-we', action='store_true', dest='win_embed',
                            help=f'{Colors.Green}Embed files invisibly{Colors.White}\
                            ({Colors.Yellow}Only works on Windows{Colors.White})' + Colors.Default)
        parser.add_argument('--win-attribute', '-wa', action='store_true', dest='win_attrib',
                            help=Colors.Green + 'Change windows attributes to hide file' + Colors.Default)
    parser.add_argument('--embed', '-e', action='store_true', dest='embed', help='')
    parser.add_argument('--to-image', '-i', action='store_true', dest='to_image',
                        help=Colors.Green + f'Converts a file into a {Colors.Pink}png image' + Colors.Default)
    parser.add_argument('--image-mode', '-I', action='store', type=int, dest='image_mode', default=3,
                        help=f'Sets output image mode.\n' + Colors.Default +
                             f'Valid values{Colors.Red}:{Colors.Blue} 3{Colors.Red}:{Colors.Blue}RGB' + Colors.Red +
                             f',{Colors.Blue} 4{Colors.Red}:{Colors.Blue}ARGB' + Colors.Default)
    parser.add_argument('--source-file', '-s', action='store', type=str, dest='source',
                        help=f'Sets the path of {Colors.Green}SOURCE{Colors.Default} file', required=True)
    parser.add_argument('--cover-file', '-c', action='store', type=str, dest='cover',
                        help=f'Sets the path of {Colors.Green}COVER{Colors.Default} file')
    parser.add_argument('--dest-file', '-d', action='store', type=str, dest='destination',
                        help=f'Sets the path of {Colors.Green}DESTINATION{Colors.Default} file')
    parser.add_argument('--delete-source', '-D', action='store_true', dest='delete',
                        help=Colors.Red + 'Deletes source file' + Colors.Default)
    parser.add_argument('--compress', '-C', action='store_true', dest='compress')
    parser.add_argument('--encrypt', '-E', action='store', type=str, dest='encryption_pass',
                        help=f'Enables {Colors.Blue}encryption{Colors.Default} \
                        - needs an {Colors.Green}ENCRYPTION_PASSword' + Colors.Default)
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose')
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet')
    args = parser.parse_args()

    # Prints banner
    print(banner)

    # Checks for verbose and quiet switches
    if args.verbose:
        verbose()
    if args.quiet:
        quiet()

    # Checks for switches to be suitable
    if not (args.win_embed or args.win_attrib or args.embed or args.to_image):
        exit(Colors.Red + ' ! Error: No operation chosen\n + Please choose an operation like embed!')
    if not is_windows and (args.win_embed or args.win_attribute):
        exit(Colors.Red + f" ! Error: You can't use windows-only options in {operating_system}")
    if args.embed and args.win_embed:
        exit(Colors.Red + " ! Error: You can't use embed and win-embed at the same time!")
    if args.to_image and args.embed:
        exit(Colors.Red + " ! Error: You can't use embed and to-image at the same time!")
    if args.to_image and args.win_embed:
        exit(Colors.Red + " ! Error: You can't use win-embed and to-image at the same time!")
    if not args.source or not os.path.exists(args.source) or not os.path.isfile(args.source):
        exit(Colors.Red + " ! Error: Couldn't find source file\n + Source file must be an existing file!")
    if (args.win_embed or args.to_image or args.embed) and not args.destination:
        exit(Colors.Red + " ! Error: You must set destination path for this operation. use: --dest-file/-d")
    if args.to_image and args.image_mode not in [3, 4]:
        exit(Colors.Red + f' ! Error: Image Mode: `{Colors.White}{args.image_mode}{Colors.Red}` not found!\n' +
             f' + Valid values:{Colors.Blue} 3{Colors.Red},{Colors.Blue} 4')

    if args.destination:
        # Makes sure that destination directory exists
        try:
            os.makedirs(os.path.split(args.destination)[0])
        except FileExistsError:
            pass

    # Checks the chosen mode
    if args.mode.lower() == 'hide':
        # Checks the chosen operation and calls the suitable function
        if args.win_embed:
            if not args.cover and not os.path.exists(args.destination):
                printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                       'You could add a cover file using --cover-file/-c switches.' + Colors.Default)
            win_embed(args.source, args.destination, args.delete, args.compress, args.cover, args.encryption_pass)
            if args.win_attrib:
                win_attrib_hide(args.destination)
        elif args.win_attrib:
            if args.cover:
                printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                       "`win attrib` operation doesn't use cover file." + Colors.Default)
            if args.destination:
                printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                       "`win attrib` operation doesn't use destination file path." + Colors.Default)
            win_attrib_hide(args.source)
        elif args.to_image:
            if args.cover:
                printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                       "`to image` operation doesn't use cover file." + Colors.Default)
            to_image(args.source, args.destination, args.delete, args.compress, args.encryption_pass, args.image_mode)
        elif args.embed:
            if not args.cover or not os.path.exists(args.cover) or not os.path.isfile(args.cover):
                exit(Colors.Red + ' ! Error: Embed operation needs a cover file' +
                     '\n + Source file must be an existing file!')
            embed(args.source, args.cover, args.destination, args.delete, args.compress, args.encryption_pass)
    elif args.mode.lower() == 'reveal':
        # Checks the chosen operation and calls the suitable function
        if args.cover:
            printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                   "`reveal` operations don't use cover file." + Colors.Default)
        if args.win_embed:
            if args.delete:
                answer = ''
                while answer != 'y' and answer != 'n':
                    answer = input(
                        Colors.Yellow + f'Are you sure you want to remove source file({args.source})?(y/N) ' +
                        Colors.Green)
                args.delete = answer == 'y'
            win_extract(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
        elif args.win_attrib:
            if args.destination:
                printv(Colors.Red + ' ! Warning: ' + Colors.Gray + Colors.BackPink +
                       "`win attrib` operation doesn't use destination file path." + Colors.Default)
            win_attrib_reveal(args.source)
        elif args.to_image:
            from_image(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
        elif args.embed:
            extract(args.source, args.destination, args.delete, args.compress, args.encryption_pass)
    else:
        exit(Colors.Red + f' ! Error: Mode: `{Colors.White}{args.mode}{Colors.Red}` not found!')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('\r' + Colors.Red + ' ! Error: Keyboard Interrupt: User canceled operation')
