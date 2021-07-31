# Variables

import platform

__all__ = ['is_windows', 'Colors', 'operating_system', 'verbose', 'quiet', 'embed_capable']

operating_system = platform.system()
is_windows = 'windows' in operating_system.lower()
verbose = False
quiet = False

embed_capable = ['PDF document', 'Matroska data', 'Microsoft ASF', 'PNG image', 'MP4 Base Media', 'JPEG image']


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
