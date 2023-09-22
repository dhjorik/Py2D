import pygame
from PyWinter.engine.settings import *


class GameGround:
    LAYERS = 1

    _player_x = 0
    _player_y = 0
    player_sprite = None

    size_x = 48     # Number of tiles in x
    size_y = 15     # Number of tiles in y

    # Sprite bounding box
    sprite_area_min_x = 0
    sprite_area_min_y = 0
    sprite_area_max_x = 0
    sprite_area_max_y = 0

    test_grid = True

    def __init__(self, game, name):
        self.name = name
        self.game = game

        # Level Size in unit
        self.level_width = self.size_x * MAP_TileX
        self.level_height = self.size_y * MAP_TileY

        # Bounding Box
        self.level_min_x = 0
        self.level_min_y = 0
        self.level_max_x = self.level_width-1
        self.level_max_y = self.level_height-1

        self.sprite_area_min_x = 0
        self.sprite_area_min_y = 0
        self.sprite_area_max_x = self.level_width - MAP_TileX
        self.sprite_area_max_y = self.level_height - MAP_TileY

        self.game_layer = pygame.Surface((self.level_width, self.level_height), pygame.SRCALPHA, 32)
        if self.test_grid:
            self.draw_world()

    def draw(self):
        if self.test_grid:
            self.draw_world()
        else:
            self.game_layer.fill((0, 0, 0, 0))
        if self.player_sprite is not None:
            self.game_layer.blit(self.player_sprite, (self.player_x, self.player_y))

    def update(self):
        pass

    def draw_world(self):
        self.game_layer.fill((0, 0, 0, 0))
        tnr_font = pygame.font.SysFont('timesnewroman', 22)
        x = 0
        i = 0
        while x < self.level_width:
            letter = tnr_font.render(str(i), False, 'black', (255, 255, 255, 0))
            pygame.draw.line(self.game_layer, 'black', (x, self.level_min_y), (x, self.level_max_y))
            self.game_layer.blit(letter, (x, 0))
            x += MAP_TileX
            i += 1
        y = 0
        i = 0
        while y < self.level_height:
            letter = tnr_font.render(str(i), False, 'black', (255, 255, 255, 0))
            pygame.draw.line(self.game_layer, 'black', (self.level_min_x, y), (self.level_max_x, y))
            self.game_layer.blit(letter, (0, y))
            y += MAP_TileY
            i += 1
        self.game_layer.convert_alpha()

    def get_player_x(self):
        return self._player_x

    def set_player_x(self, value):
        self._player_x = value
        if value < self.sprite_area_min_x:
            self._player_x = self.sprite_area_min_x
        if value > self.sprite_area_max_x:
            self._player_x = self.sprite_area_max_x

    player_x = property(get_player_x, set_player_x)

    def get_player_y(self):
        return self._player_y

    def set_player_y(self, value):
        self._player_y = value
        if value < self.sprite_area_min_y:
            self._player_y = self.sprite_area_min_y
        if value > self.sprite_area_max_y:
            self._player_y = self.sprite_area_max_y

    player_y = property(get_player_y, set_player_y)
