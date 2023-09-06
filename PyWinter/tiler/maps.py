import os
import pygame
import sys


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)


class Map:
    def __init__(self):
        self._tilemap = []
