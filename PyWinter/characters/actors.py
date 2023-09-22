from importlib import resources as _resources
import os
import sys
import pygame

from PyWinter.engine.settings import *
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

sprites = (_resources.files(assets)/'sprites')

SPRITE_NAME = '{0}_{1:02d}.png'


class Actor:
    ANIMATIONS = {}

    _files = {}
    _sprites = {}

    current_frame = 0

    size_x = MAP_TileX
    size_y = MAP_TileY

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(sprites, name)
        for action, num_frames in self.ANIMATIONS.values():
            # num_frames = self.ANIMATIONS[action]
            frames = []
            for frame in range(num_frames):
                filename = SPRITE_NAME.format(action, frame)
                frames.append(filename)
            self._files.update({action: frames})
        self.player_layer = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)

    def draw(self):
        self.player_layer.fill((0, 0, 0, 0))

    def update(self):
        pass

    def load_assets(self):
        for action, num_frames in self.ANIMATIONS.values():
            frames = []
            for frame in range(num_frames):
                fl = self._files[action][frame]
                filename = os.path.join(self.path, fl)
                level = pygame.image.load(filename)
                sprite = pygame.transform.scale(level, (self.size_x, self.size_y)).convert_alpha()
                frames.append(sprite)
            self._sprites.update({action: frames})
