import pygame
import sys

from PyWinter.settings import *
from PyWinter.engine.viewports import Viewport
from PyWinter.levels import *
from PyWinter.characters import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)

        self.level = GameGround(self, (1, 1, 1))
        self.background = Winter01(self)
        self.player = Player01(self)
        self.viewport = Viewport(self)

        self.timer = pygame.time.Clock()
        self.delta_time = 0
        self.delta_time = 0

        self.running = False

    def draw(self):
        self.viewport.draw()

        pygame.display.flip()

        msg1 = f'{self.timer.get_fps():.1f}'
        # pygame.display.set_caption(f'FPS: {msg1} - Delta: {self.delta_time}')
        pygame.display.set_caption(f'PXY {self.level.player_x, self.level.player_y} - VX {self.viewport.scroll_x} - GX {self.viewport.start_x}')

    def update(self):
        # Execute physics and state updates
        self.viewport.update()
        self.delta_time = self.timer.tick(FPS)

    def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False


if __name__ == '__main__':
    pPass, pFail = pygame.init()

    print(pygame.display.Info())
    game = Game()
    game.run()

    pygame.quit()
    sys.exit(0)
