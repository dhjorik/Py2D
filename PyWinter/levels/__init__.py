from abc import ABC
from importlib import resources as _resources
import os
import sys
import pygame

from PyWinter.settings import *
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

LEVEL_PATH = 'e{0:2d}w{0:2d}m{0:2d}'
BK_NAME = 'level_{0:2d}.png'
SBK_NAME = '{0}.png'

NUM_EPISODES = 3
NUM_WORLDS = 10
NUM_MAPS = 5

EPISODES = range(NUM_EPISODES)
WORLDS = range(NUM_WORLDS)
MAPS = range(NUM_MAPS)

backgrounds = (_resources.files(assets)/'backgrounds')


class Background(ABC):
    LEVELS = 1
    SPECIALS = []
    SPEEDS = [1]

    _files = []
    _levels = []

    def __init__(self, name, screen):
        self.name = name
        self.path = os.path.join(backgrounds, name)
        for i in range(self.LEVELS):
            self._files.append(BK_NAME.format(i))

    def draw(self):
        pass

    def update(self):
        pass

    def load_assets(self):
        self._levels = []
        for i in range(self.LEVELS):
            fl = self._files[i]
            filename = os.path.join(self.path, fl)
            level = pygame.image.load(filename)
            pygame.transform.scale(level, RES)
            self._levels.append(level)


class Winter01(Background):
    LEVELS = 6
    SPECIALS = ['snowing']
    SPEEDS = [12, 10, 7, 4, 2, 0]

    def __init__(self):
        super(Winter01, self).__init__('winter_01')
        self.load_assets()
