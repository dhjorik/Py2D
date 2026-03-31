import pygame as pgm
from PyWinter.engine.settings import *
from PyWinter.engine.screens import Screen, ScreenLayers


class Gui:
    LAYERS = 1

    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        # self.layer = pgm.Surface(RES, pgm.SRCALPHA, 32)
        # self.layer.fill((10, 10, 10, 255))

    def draw(self):
        pass
        # self.screen.blit_buffer(self.layer, (0, 0), ScreenLayers.BACK_LAYERS, 0)
