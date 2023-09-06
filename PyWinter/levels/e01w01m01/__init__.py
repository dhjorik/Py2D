# Level description

import os
import sys


_this = sys.modules(__name__)
_path = os.path.dirname(__file__)

BK_NAME = 'level_{0:2d}.png'


class Background:
    LEVELS = range(6)

    _files = []

    def __init__(self):
        for i in self.LEVELS:
            self._files.append(BK_NAME.format(i))
