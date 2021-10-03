# InvisibleCharm.__init__.py
# CodeWriter21
from InvisibleCharm.lib import Encryption, Prepare
import InvisibleCharm.lib.operations as operations
import InvisibleCharm.lib.Console as Console
import InvisibleCharm.lib.File as File

from log21 import get_colors as _gc
from InvisibleCharm.lib.Console import exit as _exit

__version__ = "2.3.0"
__author__ = "CodeWriter21 (Mehrad Pooryoussof)"
__github__ = "Https://GitHub.com/MPCodeWriter21/InvisibleCharm"


def entry_point():
    from InvisibleCharm.__main__ import main
    try:
        main()
    except KeyboardInterrupt:
        _exit('\r' + _gc("lr") + ' ! Error: Keyboard Interrupt: User canceled operation')
