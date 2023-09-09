from abc import ABC
from importlib import resources as _resources
import os
import sys
import pygame

from PyWinter.settings import *
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

backgrounds = (_resources.files(assets)/'backgrounds')

BK_NAME = 'level_{0:02d}.png'
SBK_NAME = '{0}.png'


class Background(ABC):
    LAYERS = 1
    SPECIALS = []
    _speeds = []
    BACK_LAYERS = [True]

    _files = []
    _layers = []
    _shifts = []

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(backgrounds, name)
        for i in range(self.LAYERS):
            self._files.append(BK_NAME.format(i))
            self._shifts.append(0)
        self.back_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)
        self.front_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)

    def draw(self):
        self.back_layer.fill((0, 0, 0, 0))
        self.front_layer.fill((0, 0, 0, 0))

        for i in range(self.LAYERS):
            x = self._shifts[i]
            bkg = self._layers[i]
            if self.BACK_LAYERS[i]:
                self.back_layer.blit(bkg, (x % WIDTH, 0))
                self.back_layer.blit(bkg, (x % WIDTH - WIDTH, 0))
            else:
                self.front_layer.blit(bkg, (x % WIDTH, 0))
                self.front_layer.blit(bkg, (x % WIDTH - WIDTH, 0))

        self.back_layer.convert_alpha()
        self.front_layer.convert_alpha()

    def update(self):
        self.shift_world()

    def shift_world(self):
        if len(self._speeds) == 0:
            return
        factor = self.game.player_speed / PLAYER_SPEED
        for i in range(self.LAYERS):
            self._shifts[i] -= (self.game.camera_dir * self._speeds[i] * factor)
            if self._shifts[i] < 0:
                self._shifts[i] += WIDTH
            if self._shifts[i] >= WIDTH:
                self._shifts[i] -= WIDTH

    def load_assets(self):
        self._layers = []
        for i in range(self.LAYERS):
            fl = self._files[i]
            filename = os.path.join(self.path, fl)
            level = pygame.image.load(filename)
            layer = pygame.transform.scale(level, RES).convert_alpha()
            self._layers.append(layer)


class Winter01(Background):
    LAYERS = 6
    SPECIALS = ['snowing']
    BACK_LAYERS = [True, True, True, True, False, False]

    def __init__(self, game):
        super(Winter01, self).__init__('winter_01', game)
        self.load_assets()
        backs = len([bck for bck in self.BACK_LAYERS if bck])
        for i in range(self.LAYERS):
            speed = round(i * (PLAYER_SPEED/backs))
            self._speeds.append(speed)
