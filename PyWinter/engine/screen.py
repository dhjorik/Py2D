import pygame
from OpenGL.GL import *
from PySide6 import QtWidgets, QtGui

from PyWinter.engine.settings import *


class ScreenLayers:
    BACK_LAYERS = 0
    GAME_LAYERS = 1
    FRONT_LAYERS = 2
    SFX_LAYERS = 3
    GUI_LAYERS = 4


class Screen:
    canvas = None
    offsets = [0, 0, 0, 0, 0]

    num_layers = 1
    layers = [None]
    buffer = None

    def __init__(self, game):
        self.game = game

        flags = SCREEN_FLAGS
        self.screen = QtWidgets.QMainWindow()
        self.screen.setWindowTitle('PyWinter Demo')
        self.screen.setGeometry(0, 0, SCREEN_W, SCREEN_H)

        # self.screen = pygame.display.set_mode(SCREEN_RES, flags)
        # self.screen = pygame.display.set_mode(SCREEN_RES)

        self.info = pygame.display.Info()
        self._setup_ui()

        print('Driver:', pygame.display.get_driver())
        print('Surfaces:', pygame.display.get_surface())

    def show(self):
        self.screen.show()

    def set_layers(self):
        self.num_layers = self.game.background.NUM_BACK_LAYERS
        self.offsets[ScreenLayers.GAME_LAYERS] = self.num_layers
        self.num_layers += self.game.level.LAYERS
        self.offsets[ScreenLayers.FRONT_LAYERS] = self.num_layers
        self.num_layers += self.game.background.NUM_FRONT_LAYERS
        self.offsets[ScreenLayers.SFX_LAYERS] = self.num_layers
        self.num_layers += self.game.background.SPECIALS
        self.offsets[ScreenLayers.GUI_LAYERS] = self.num_layers
        self.num_layers += self.game.gui.LAYERS

        self.layers = [None] * self.num_layers
        self.buffer = pygame.Surface(RES, pygame.SRCALPHA, 32)

    def blit(self, source, destination, area=None, special_flags=0):
        return self.buffer.blit(source, destination, area, special_flags)

    def blit_buffer(self, source, destination, layer=ScreenLayers.BACK_LAYERS, index=0):
        to_layer = index + Screen.offsets[layer]
        self.layers[to_layer] = (source, destination)
        return True

    def flip(self):
        pygame.display.flip()
        pass

    def draw(self):
        try:
            if len(self.layers) > 0:
                self.buffer.blits([lay for lay in self.layers if lay is not None])
            else:
                self.buffer.fill((0, 0, 0, 0))
        except:
            pass

        # draw texture openGL Texture
        self._surface_to_texture(self.buffer)

    def update(self):
        self.layers = [None] * self.num_layers

    def _setup_ui(self):
        self.canvas = QtWidgets.QLabel(self.screen)
        self.canvas.setGeometry(0, 0, SCREEN_W, SCREEN_H)

    def _setup_fonts(self):
        self.default_font12 = pygame.font.Font(None, 12)
        self.default_font24 = pygame.font.Font(None, 24)

    def _surface_to_texture(self,  pygame_surface):
        # Convert the Pygame surface to a QImage
        image = QtGui.QImage(pygame_surface.get_buffer(), pygame_surface.get_width(), pygame_surface.get_height(), QtGui.QImage.Format_RGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
