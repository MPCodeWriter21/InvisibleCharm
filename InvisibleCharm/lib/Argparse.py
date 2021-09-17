# InvisibleCharm.lib.argparse.py
# COdeWriter21

import log21 as _log21
from argparse import ArgumentParser as _ArgumentParser


class ArgumentParser(_ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = _log21.Logger('InvisibleCharm-Argparse')

    def _print_message(self, message, file=None):
        if message:
            self.logger.handlers.clear()
            handler = _log21.ColorizingStreamHandler(stream=file)
            self.logger.addHandler(handler)
            self.logger.info(message)
