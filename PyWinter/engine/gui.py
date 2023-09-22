import pygame
from PyWinter.engine.settings import *
from OpenGL.GL import *


class Gui:
    LAYERS = 1

    def __init__(self, game):
        self.game = game
