import pygame
import sys

from settings import *


class Game:
    def __init__(self):
        ppass, pfail = pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.timer = pygame.time.Clock()

        self.delta_time = 0

    def draw(self):
        # Draw new frame
        self.screen.fill('black')
        pygame.display.flip()
        self.delta_time = self.timer.tick(TICK)
        msg1 = f'{self.timer.get_fps():.1f}'
        pygame.display.set_caption(f'FPS: {msg1}')

    def update(self):
        # Execute phisics and state updates
        pass

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)


if __name__ == '__main__':
    game = Game()
    game.run()
