import pygame
from PyWinter.engine.settings import *
from PyWinter.engine.screen import ScreenLayers


class Viewport:
    viewport_x = WIDTH
    player_x = 0
    player_y = 0

    scroll_x = 0
    scroll_min_x = 0
    scroll_max_x = 0

    def __init__(self, game):
        self.game = game

        self.level = self.game.level
        self.background = self.game.background
        self.player = self.game.player

        self.start_x = 0
        self.scroll_min_x = HALF_WIDTH
        self.scroll_max_x = self.level.level_width - HALF_WIDTH

        self.view_min_x = 0
        self.view_max_x = self.level.level_width - WIDTH

        self.scroll_dir = 0

        self.player_x = self.background.player[0]
        self.player_y = self.background.player[1]
        self.player_speed = PLAYER_SPEED

    def draw(self):
        self.player.draw()
        self.level.draw()
        self.background.draw()

        self.start_x = self.player_x - HALF_WIDTH
        if self.start_x < self.view_min_x:
            self.start_x = self.view_min_x
        if self.start_x > self.view_max_x:
            self.start_x = self.view_max_x

        self.game.screen.blit_buffer(self.level.game_layer, (-self.start_x, 0, WIDTH, HEIGHT), ScreenLayers.GAME_LAYERS, 0)

    def update(self):
        direction = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.player_speed = PLAYER_SPEED * 1.5
        else:
            self.player_speed = PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            if self.player_x < self.level.level_max_x:
                self.player_x += self.player_speed
                self.scroll_x += self.player_speed
                direction = 1
            else:
                self.player_x = self.level.level_max_x

        if keys[pygame.K_LEFT]:
            if self.player_x > 0:
                self.player_x -= self.player_speed
                self.scroll_x -= self.player_speed
                direction = -1
            else:
                self.player_x = 0

        if (self.scroll_x > self.scroll_min_x) and (self.scroll_x < self.scroll_max_x):
            self.scroll_dir = direction
        else:
            self.scroll_dir = 0

        self.player.update()

        self.background.player_speed = self.player_speed
        self.background.camera_speed = self.scroll_dir
        self.background.update()

        self.level.player_x = self.player_x
        self.level.player_y = self.player_y + round(self.player.player_delta_y)
        self.level.player_sprite = self.player.player_layer
        self.level.update()
