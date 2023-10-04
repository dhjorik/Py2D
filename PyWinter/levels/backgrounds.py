from abc import ABC
from importlib import resources as _resources
import os
import sys
import pygame

from PyWinter.engine.settings import *
from PyWinter.engine.screen import ScreenLayers
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

backgrounds = str(_resources.files(assets)/'backgrounds')

BK_NAME = 'level_{0:02d}.png'
SBK_NAME = '{0}.png'


class Background(ABC):
    LAYERS = 1
    SPECIALS = 0
    _speeds = []
    BACK_LAYERS = [True]

    _files = []
    _layers = []
    _specials = []
    _shifts = []

    player = (0, 0)

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(backgrounds, name)

        self.NUM_BACK_LAYERS = len([x for x in self.BACK_LAYERS if x])
        self.LAYERS = len(self.BACK_LAYERS)
        self.NUM_FRONT_LAYERS = self.LAYERS - self.NUM_BACK_LAYERS

        for i in range(self.LAYERS):
            self._files.append(BK_NAME.format(i))
            self._shifts.append(0)
        self.back_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)
        self.front_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)

        self.player_speed = 0
        self.camera_speed = 0

    def draw(self):
        self.back_layer.fill((0, 0, 0, 0))
        self.front_layer.fill((0, 0, 0, 0))

        frg = 0
        bkg = 0
        for i in range(self.LAYERS):
            x = self._shifts[i]
            bkg_layer = self._layers[i]
            if self.BACK_LAYERS[i]:
                self.game.screen.blit_buffer(bkg_layer, (x % WIDTH - WIDTH, 0, WIDTH, HEIGHT), ScreenLayers.BACK_LAYERS, bkg)
                bkg += 1
                # self.back_layer.blit(bkg, (x % WIDTH, 0))
                # self.back_layer.blit(bkg, (x % WIDTH - WIDTH, 0))
            else:
                self.game.screen.blit_buffer(bkg_layer, (x % WIDTH - WIDTH, 0, WIDTH, HEIGHT), ScreenLayers.FRONT_LAYERS, frg)
                frg += 1
                # self.front_layer.blit(bkg, (x % WIDTH, 0))
                # self.front_layer.blit(bkg, (x % WIDTH - WIDTH, 0))

    def update(self):
        self.shift_world()

    def shift_world(self):
        if len(self._speeds) == 0:
            return
        factor = self.player_speed / PLAYER_SPEED
        for i in range(self.LAYERS):
            self._shifts[i] -= (self.camera_speed * self._speeds[i] * factor)
            if self._shifts[i] < 0:
                self._shifts[i] += WIDTH
            if self._shifts[i] >= WIDTH:
                self._shifts[i] -= WIDTH

    def load_assets(self):
        self._layers = []
        for i in range(self.LAYERS):
            fl = self._files[i]
            filename = os.path.join(self.path, fl)
            level = pygame.image.load(filename).convert_alpha()
            layer = pygame.transform.scale(level, RES).convert_alpha()
            layer_bkg = pygame.Surface((WIDTH*2, HEIGHT), pygame.SRCALPHA, 32)
            layer_bkg.blit(layer, (0, 0))
            layer_bkg.blit(layer, (WIDTH, 0))
            self._layers.append(layer_bkg)


class Winter01(Background):
    BACK_LAYERS = [True, True, True, True, False, False]
    # BACK_LAYERS = [True, True, False]
    SPECIALS = 1

    _specials = ['snowing']

    def __init__(self, game):
        super(Winter01, self).__init__('winter_01', game)
        self.load_assets()
        backs = len([bck for bck in self.BACK_LAYERS if bck])
        for i in range(self.LAYERS):
            speed = round(i * (PLAYER_SPEED/backs))
            self._speeds.append(speed)

        self.player = (0, 11 * MAP_TileY)
