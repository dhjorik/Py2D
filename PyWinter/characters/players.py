import pygame
from PyWinter.characters.actors import Actor
from PyWinter.engine.settings import *


class Player01(Actor):
    ANIMATIONS = {
        PlayerState.IDLE: ('Idle', 10, 10),
        PlayerState.WALK: ('Walk', 10, 10),
        PlayerState.RUN:  ('Run', 8, 8),
        PlayerState.JUMP: ('Jump', 8, 16),
        PlayerState.FALL: ('Fall', 8, 16),
        PlayerState.HURT: ('Hurt', 10, 10),
        PlayerState.DEAD: ('Dead', 10, 10),
        PlayerState.SLIDE: ('Slide', 10, 10),
    }

    SEQUENCERS = {
        PlayerState.IDLE: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ),
        PlayerState.WALK: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ),
        PlayerState.RUN:  (0, 1, 2, 3, 4, 5, 6, 7, ),
        PlayerState.JUMP: (0, 1, 2, 3, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7, ),
        PlayerState.FALL: (0, 1, 2, 3, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7, ),
        PlayerState.HURT: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ),
        PlayerState.DEAD: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ),
        PlayerState.SLIDE: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ),
    }

    player_move = False
    player_mirror = False

    player_jump = False
    player_fall = False

    player_delta_y = 0
    player_jump_y = MAP_TileY * 4
    player_step_y = player_jump_y / 16

    player_state = PlayerState.IDLE

    def __init__(self, game):
        super(Player01, self).__init__('player_01', game)
        self.load_assets()

    def draw(self):
        if self.player_jump:
            self.player_state = PlayerState.JUMP
        if self.player_fall:
            self.player_state = PlayerState.FALL

        sprite_name, num_frames, num_sequences = self.ANIMATIONS[self.player_state]
        sprite_sequences = self.SEQUENCERS[self.player_state]
        sprites = self._sprites[sprite_name]

        self.current_frame += 1
        if self.current_frame >= num_sequences:
            if self.player_fall:
                self.player_jump = False
                self.player_fall = False
                self.player_delta_y = 0
            if self.player_jump:
                self.player_jump = False
                self.player_fall = True
                self.player_delta_y = -self.player_jump_y
            self.current_frame = 0

        self.current_sequence = sprite_sequences[self.current_frame]
        sprite = sprites[self.current_sequence]

        self.player_layer.fill((0, 0, 0, 0))
        r_sprite = sprite
        if self.player_mirror:
            r_sprite = pygame.transform.flip(sprite, True, False)
        self.player_layer.blit(r_sprite, (0, 0))

    def update(self):
        cur_state = self.player_state
        self.player_state = PlayerState.IDLE
        self.player_move = False

        if self.player_jump:
            self.player_delta_y -= self.player_step_y
            return

        if self.player_fall:
            self.player_delta_y += self.player_step_y
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.player_delta_y -= self.player_step_y
            self.player_state = PlayerState.JUMP
            self.player_jump = True

        if keys[pygame.K_RIGHT]:
            self.player_mirror = False
            self.player_move = True
            self.player_state = PlayerState.WALK

        if keys[pygame.K_LEFT]:
            self.player_mirror = True
            self.player_move = True
            self.player_state = PlayerState.WALK

        if keys[pygame.K_LSHIFT]:
            if self.player_move:
                self.player_state = PlayerState.RUN

        if self.player_state != cur_state:
            self.current_frame = 0
