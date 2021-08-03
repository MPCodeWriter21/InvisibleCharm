# Variables

import platform

__all__ = ['is_windows', 'Colors', 'operating_system', 'embed_capable', 'banner']

operating_system = platform.system()
is_windows = 'windows' in operating_system.lower()

embed_capable = ['PDF document', 'Matroska data', 'Microsoft ASF', 'PNG image', 'ISO Media', 'JPEG image',
                 'Audio file with ID3']


# Colors
class Colors:
    Default = '\033[0m'
    Gray = '\033[90m'
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Pink = '\033[95m'
    Cyan = '\033[96m'
    BCyan = '\033[1;96m'
    White = '\033[1;37m'

    BackGray = '\033[100m'
    BackRed = '\033[101m'
    BackGreen = '\033[102m'
    BackYellow = '\033[103m'
    BackPurple = '\033[104m'
    BackPink = '\033[105m'
    BackCyan = '\033[106m'
    BackWhite = '\033[107m'


banner = rf'''
{Colors.BackPink + Colors.White}                         ____ _                          {Colors.Default}
{Colors.BackPink + Colors.White}                        / ___| |__   __ _ _ __ _ __ ___  {Colors.Default}
{Colors.BackPink + Colors.Pink}   I   V   S   B   E   {Colors.White}| |   | '_ \ / _` | '__| '_ ` _ \ {Colors.Default}
{Colors.BackPink + Colors.Pink}     N   I   I   L     {Colors.White}| |___| | | | (_| | |  | | | | | |{Colors.Default}
{Colors.BackPink + Colors.White}                        \____|_| |_|\__,_|_|  |_| |_| |_|{Colors.Default}
{Colors.Default}
{Colors.White}Blog    {Colors.Red} :{Colors.Cyan} https://www.{Colors.BCyan}CodeWriter21{Colors.Cyan}.blog.ir
{Colors.White}Github  {Colors.Red} :{Colors.Cyan} https://www.GitHub.com/{Colors.BCyan}MPCodeWriter21
{Colors.White}Telegram{Colors.Red} :{Colors.Cyan} https://www.Telegram.me/{Colors.BCyan}CodeWriter21
'''
