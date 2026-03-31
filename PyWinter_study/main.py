import os

from PyWinter.engine.settings import *
from PyWinter.engine.screens import Screen, ScreenLayers
from PyWinter.engine.backgrounds import *
from PyWinter.engine.guis import *
from PyWinter.engine.tilemaps import *


class Game:
    def __init__(self):
        self.screen = Screen(self)
        self.background = Background('black', self)
        self.tile_map = TileMap(self, 100, MAP_Rows)
        self.gui = Gui(self)

        self.px = 0
        self.py = 0

        self.timer = pygame.time.Clock()
        self.delta_time = 0

        self.running = 0

    def draw(self):
        msg1 = f'FPS - {self.timer.get_fps():.01f} - {self.tile_map.p_tile_x} - {self.tile_map.p_module_x}'
        tnr_font = pygame.font.SysFont('timesnewroman', 22)
        letters = tnr_font.render(msg1, False, 'black', (255, 255, 255, 0))
        position = HEIGHT * 8 / 10
        self.screen.blit_buffer(letters, (0, position), ScreenLayers.GUI_LAYERS, 0)

        self.background.draw()
        self.tile_map.draw()

        self.screen.draw()
        self.screen.flip()

    def update(self):
        self.delta_time = self.timer.tick(FPS)
        self.tile_map.update()
        self.screen.update()

    def run(self):
        self.running = 1
        self.screen.set_layers()
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = 0
        keys = pygame.key.get_pressed()

        step = 1
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            step = 3

        if keys[pygame.K_RIGHT]:
            rs = self.px + step
            valid = self.tile_map.slide(rs, self.py)
            if valid:
                self.px = rs

        if keys[pygame.K_LEFT]:
            rs = self.px - step
            valid = self.tile_map.slide(rs, self.py)
            if valid:
                self.px = rs


if __name__ == '__main__':
    pPass, pFail = pygame.init()

    game = Game()
    game.run()

    pygame.quit()
