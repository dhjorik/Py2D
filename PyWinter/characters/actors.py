from abc import ABC
from importlib import resources as _resources
import os
import sys
import pygame

from PyWinter.settings import *
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

sprites = (_resources.files(assets)/'sprites')

SPRITE_NAME = '{}_{1:02d}.png'


class Actor:
    ANIMATIONS = {
        'Idle': 10,
        'Walk': 10,
        'Run': 8,
        'Jump': 8,
        'Fall': 8,
        'Slide': 10,
        'Hurt': 10,
        'Dead': 10,
    }

    _files = {}
    _sprites = {}

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(sprites, name)
        for action in self.ANIMATIONS:
            num_frames = self.ANIMATIONS[action]
            frames = []
            for frame in range(num_frames):
                filename = SPRITE_NAME.format(action, frame)
                frames.append(filename)
            self._files.update({action:frames})
        self.player_layer = pygame.Surface(RES, pygame.SRCALPHA, 32)

    def draw(self):
        self.player_layer.fill('black')

    def update(self):
        keys = pygame.key.get_pressed()

    def load_assets(self):
        for action in self.ANIMATIONS:
            num_frames = self.ANIMATIONS[action]
            frames = []
            for frame in range(num_frames):
                fl = self._files[action][frame]
                filename = os.path.join(self.path, fl)
                level = pygame.image.load(filename)
                sprite = pygame.transform.scale(level, RES).convert_alpha()
                frames.append(sprite)
            self._sprites.update({action: frames})

        for i in range(self.LAYERS):
            fl = self._files[i]
            filename = os.path.join(self.path, fl)
            level = pygame.image.load(filename)
            devel = pygame.transform.scale(level, RES).convert_alpha()
            self._sprites.append(devel)
