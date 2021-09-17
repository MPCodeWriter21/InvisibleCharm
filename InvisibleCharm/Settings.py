# InvisibleCharm.Settings
# CodeWriter21

from log21 import get_colors as _gc
import platform as _platform

__all__ = ['is_windows', 'operating_system', 'embed_capable', 'banner']

operating_system = _platform.system()
is_windows = 'windows' in operating_system.lower()

embed_capable = ['PDF document', 'Matroska data', 'Microsoft ASF', 'PNG image', 'ISO Media', 'JPEG image',
                 'Audio file with ID3']

banner = rf''' 
{_gc('blm', 'lw')}                         ____ _                          {_gc('rst')}
{_gc('blm', 'lw')}                        / ___| |__   __ _ _ __ _ __ ___  {_gc('rst')}
{_gc('blm', 'lm')}   I   V   S   B   E   {_gc('blm', 'lw')}| |   | '_ \ / _` | '__| '_ ` _ \ {_gc('rst')}
{_gc('blm', 'lm')}     N   I   I   L     {_gc('blm', 'lw')}| |___| | | | (_| | |  | | | | | |{_gc('rst')}
{_gc('blm', 'lw')}                        \____|_| |_|\__,_|_|  |_| |_| |_|{_gc('rst')}
{_gc('rst')}
{_gc('lw')}Blog    {_gc('lr')} :{_gc('lc')} https://www.CodeWriter21.blog.ir
{_gc('lw')}Github  {_gc('lr')} :{_gc('lc')} https://www.GitHub.com/MPCodeWriter21
{_gc('lw')}Telegram{_gc('lr')} :{_gc('lc')} https://www.Telegram.me/CodeWriter21
'''
