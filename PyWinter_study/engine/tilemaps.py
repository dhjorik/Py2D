import pygame as pgm
from PyWinter.engine.settings import *
from PyWinter.engine.screens import Screen, ScreenLayers


class TileMapData:
    _tile_x = 0
    _tile_y = 0

    _size_x = 0
    _size_y = 0

    def __init__(self, def_tile_x, def_tile_y):
        self._tile_x = def_tile_x
        self._tile_y = def_tile_y
        self._recalc()

    def _recalc(self):
        self._size_x = self._tile_x * MAP_TileX
        self._size_y = self._tile_y * MAP_TileY

    @property
    def size_x(self):
        return self._size_x

    @property
    def size_y(self):
        return self._size_y

    def _get_tile_x(self):
        return self._tile_x

    def _set_tile_x(self, value):
        self._tile_x = value
        self._recalc()

    tile_x = property(_get_tile_x, _set_tile_x)

    def _get_tile_y(self):
        return self._tile_y

    def _set_tile_y(self, value):
        self._tile_y = value
        self._recalc()

    tile_y = property(_get_tile_y, _set_tile_y)

    def contains(self, x, y):
        if x < 0:
            return False
        if y < 0:
            return False
        contained = (x < self._size_x) and (y < self._size_y)
        return contained


class TileMap:
    LAYERS = 1

    _tile_x = 0
    _tile_y = 0

    _view_x = 0
    _view_y = 0

    virtual = TileMapData(0, 0)
    sliding = TileMapData(MAP_Cols + 2, MAP_Rows)

    def __init__(self, game, def_tile_x, def_tile_y):
        self.game = game
        self.screen = game.screen

        self._tile_x = def_tile_x
        self._tile_y = def_tile_y
        self._recalc()

        self.p_tile_x = 0
        self.p_module_x = 0
        self.o_tile_x = 0

        self.layer = pgm.Surface((self.sliding.size_x, self.sliding.size_y), pgm.SRCALPHA, 32)
        self.draw_grid()

    def _recalc(self):
        self.virtual.tile_x = self._tile_x
        self.virtual.tile_y = self._tile_y

    def slide(self, dx, dy):
        if self.virtual.contains(dx, dy):
            self._view_x = dx
            self._view_y = dy
            self.calc_tile()
            return True
        else:
            return False

    def calc_tile(self):
        # X tile
        c_x = self._view_x // MAP_TileX
        r_x = self._view_x % MAP_TileX
        self.p_tile_x = round(c_x)
        self.p_module_x = round(r_x)
        return c_x, r_x

    def draw(self):
        self.screen.blit_buffer(self.layer, (-self.p_module_x, 0), ScreenLayers.GAME_LAYERS, 0)

    def update(self):
        if self.p_tile_x != self.o_tile_x:
            self.draw_grid()
            self.o_tile_x = self.p_tile_x
    def draw_grid(self):
        self.layer.fill((0, 0, 0, 0))
        tnr_font = pgm.font.SysFont('timesnewroman', 22)
        x = 0
        i = 0
        while x < self.sliding.size_x:
            letter = tnr_font.render(str(i + self.p_tile_x), False, 'black', (255, 255, 255, 0))
            letter_i = tnr_font.render(str(i), False, 'black', (255, 255, 255, 0))
            pgm.draw.line(self.layer, 'black', (x, 0), (x, self.sliding.size_y-1))
            self.layer.blit(letter, (x, 0))
            self.layer.blit(letter_i, (x, MAP_TileY))
            x += MAP_TileX
            i += 1
        y = 0
        j = 0
        while y < self.sliding.size_y:
            letter = tnr_font.render(str(j), False, 'black', (255, 255, 255, 0))
            pgm.draw.line(self.layer, 'black', (0, y), (self.sliding.size_x-1, y))
            self.layer.blit(letter, (0, y))
            y += MAP_TileY
            j += 1
        self.layer.convert_alpha()
