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
    _shifts = []

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(backgrounds, name)
        for i in range(self.LEVELS):
            self._files.append(BK_NAME.format(i))
            self._shifts.append(0)

    def draw(self):
        for i in range(self.LEVELS):
            x = self._shift[i]
            bkg = self._levels[0]
            self.game.screen.blit(bkg, (x % WIDTH, 0))
            self.game.screen.blit(bkg, (x % WIDTH - WIDTH - 1, 0))

    def update(self):
        self.shift_world()

    def shift_world(self):
        # Scroll when the player sprite moves closer to the right.
        # if self.player.pos.x >= 500:
        #     self.player.pos.x = 500  # Stop at 500.
        #     self.shift_platforms()
        # # Scroll when the player sprite moves closer to the left.
        # if self.player.pos.x <= 120:
        #     self.player.pos.x = 120  # Stop at 120.
        #     self.shift_platforms()
        self.shift_platforms()

    def shift_platforms(self):
        # for plat in self.platforms:  # Iterate over the platform sprites.
        #     plat.pos.x -= self.player.vel.x  # Update the platform's pos vector.
        #     plat.rect.x = plat.pos.x  # Update the rect.
        for i in range(self.LEVELS):
            self._shift[i] += (self.game.camera_dir * self.SPEEDS[i])

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

    def __init__(self, screen):
        super(Winter01, self).__init__('winter_01', screen)
        self.load_assets()
