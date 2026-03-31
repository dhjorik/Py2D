import pygame as pgm
from PyWinter.engine.settings import *
from PyWinter.engine.screens import Screen, ScreenLayers


class Background:
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
        self.screen = game.screen

        self.NUM_BACK_LAYERS = len([x for x in self.BACK_LAYERS if x])
        self.LAYERS = len(self.BACK_LAYERS)
        self.NUM_FRONT_LAYERS = self.LAYERS - self.NUM_BACK_LAYERS

        self.layer = pgm.Surface(RES, pgm.SRCALPHA, 32)
        self.layer.fill('white')

    def draw(self):
        self.screen.blit_buffer(self.layer, (0, 0), ScreenLayers.BACK_LAYERS, 0)
