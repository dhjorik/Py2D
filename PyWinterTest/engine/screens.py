import pygame as pgm
from PyWinter.engine.settings import *


class ScreenLayers:
    BACK_LAYERS = 0
    GAME_LAYERS = 1
    FRONT_LAYERS = 2
    SFX_LAYERS = 3
    GUI_LAYERS = 4


class Screen:
    offsets = [0, 0, 0, 0, 0]

    num_layers = 1
    layers = [None]
    buffer = None

    def __init__(self, game):
        self.game = game

        if SCREEN_FLAGS is None:
            self.screen = pgm.display.set_mode(SCREEN_RES)
        else:
            self.screen = pgm.display.set_mode(SCREEN_RES, SCREEN_FLAGS)

        self.info = pgm.display.Info()

        print(pgm.display.get_driver())
        print(pgm.display.get_surface())

    def set_layers(self):
        self.num_layers = self.game.background.NUM_BACK_LAYERS
        self.offsets[ScreenLayers.GAME_LAYERS] = self.num_layers
        self.num_layers += self.game.tile_map.LAYERS
        self.offsets[ScreenLayers.FRONT_LAYERS] = self.num_layers
        self.num_layers += self.game.background.NUM_FRONT_LAYERS
        self.offsets[ScreenLayers.SFX_LAYERS] = self.num_layers
        self.num_layers += self.game.background.SPECIALS
        self.offsets[ScreenLayers.GUI_LAYERS] = self.num_layers
        self.num_layers += self.game.gui.LAYERS

        self.layers = [None] * self.num_layers
        self.buffer = pgm.Surface(RES, pgm.SRCALPHA, 32)

    def blit(self, source, destination, area=None, special_flags=0):
        return self.buffer.blit(source, destination, area, special_flags)

    def blit_buffer(self, source, destination, layer=ScreenLayers.BACK_LAYERS, index=0):
        to_layer = index + Screen.offsets[layer]
        self.layers[to_layer] = (source, destination)
        return True

    def flip(self):
        pgm.display.flip()

    def draw(self):
        if len(self.layers) > 0:
            self.buffer.blits([lay for lay in self.layers if lay is not None])
        else:
            self.buffer.fill((0, 0, 0, 0))
        self.screen.blit(self.buffer, (0, 0))

    def update(self):
        self.layers = [None] * self.num_layers

    def _setup_fonts(self):
        self.default_font12 = pgm.font.Font(None, 12)
        self.default_font24 = pgm.font.Font(None, 24)
