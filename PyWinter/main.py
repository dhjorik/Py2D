import pygame
import sys

from PyWinter.settings import *
from PyWinter.levels import Winter01


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)

        self.background = Winter01(self)
        self.timer = pygame.time.Clock()
        self.delta_time = 0

        self.camera_x = WIDTH / 2
        self.camera_y = HEIGHT / 2

        self.camera_dir = 0

        self.running = False

    def draw(self):
        # Draw new frame
        self.screen.fill('black')
        self.background.draw()

        pygame.display.flip()
        self.delta_time = self.timer.tick(TICK)
        msg1 = f'{self.timer.get_fps():.1f}'
        pygame.display.set_caption(f'FPS: {msg1}')

    def update(self):
        # Execute physics and state updates
        self.background.update()

    def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def check_events(self):
        self.camera_dir = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.camera_x -= 10
                    if self.camera_x < THRESHOLD_LEFT:
                        self.camera_x = THRESHOLD_LEFT
                        self.camera_dir = -1
                if event.key == pygame.K_RIGHT:
                    self.camera_x += 10
                    if self.camera_x > THRESHOLD_RIGHT:
                        self.camera_x = THRESHOLD_RIGHT
                        self.camera_dir = 1


if __name__ == '__main__':
    pPass, pFail = pygame.init()

    game = Game()
    game.run()

    pygame.quit()
    sys.exit(0)
