import pygame
import sys

from PyWinter.settings import *
from PyWinter.levels import *
# from PyWinter.characters import Player01


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)

        self.background = Winter01(self)
#        self.player = Player01(self)

        self.timer = pygame.time.Clock()
        self.delta_time = 0

        self.camera_x = WIDTH / 2
        self.camera_y = HEIGHT / 2

        self.camera_dir = 0
        self.player_speed = PLAYER_SPEED

        self.running = False

    def draw(self):
        self.background.draw()
#        self.player.draw()

        self.screen.blit(self.background.back_layer, (0, 0))
        # self.screen.blit(self.player.player_layer, (0, 0))
        self.screen.blit(self.background.front_layer, (0, 0))

        pygame.display.flip()

        self.delta_time = self.timer.tick(TICKS)
        msg1 = f'{self.timer.get_fps():.1f}'
        pygame.display.set_caption(f'FPS: {msg1} - Delta: {self.delta_time} - X-Y-V: {self.camera_x},{self.camera_y} -> {self.camera_dir}')

    def update(self):
        # Execute physics and state updates
        self.background.update()
#        self.player.update()

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.player_speed = PLAYER_SPEED * 1.5
        else:
            self.player_speed = PLAYER_SPEED

        if keys[pygame.K_LEFT]:
            self.camera_x -= self.player_speed
            if self.camera_x < THRESHOLD_LEFT:
                self.camera_x = THRESHOLD_LEFT
                self.camera_dir = -1
        if keys[pygame.K_RIGHT]:
            self.camera_x += self.player_speed
            if self.camera_x > THRESHOLD_RIGHT:
                self.camera_x = THRESHOLD_RIGHT
                self.camera_dir = 1


if __name__ == '__main__':
    pPass, pFail = pygame.init()

    game = Game()
    game.run()

    pygame.quit()
    sys.exit(0)
