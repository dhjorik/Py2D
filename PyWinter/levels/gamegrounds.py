import os
import pygame
from PyWinter.settings import *


class GameGround:
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
        self.game_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)

    def draw(self):
        self.game_layer.fill((0, 0, 0, 0))

        self.game_layer.convert_alpha()

    def update(self):
        pass

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
