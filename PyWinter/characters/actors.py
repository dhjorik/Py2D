from importlib import resources as _resources
import os
import sys

from PyWinter.engine.settings import *
from PyWinter import assets


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

sprites = str(_resources.files(assets)/'sprites')

SPRITE_NAME = '{0}_{1:02d}.png'


class Actor:
    ANIMATIONS = {t: (ActorStateNames[t], 0, 0) for t in ActorState}
    SEQUENCERS = {t: tuple() for t in ActorState}

    _files = {}
    _sprites = {}

    preview_state = ActorState.IDLE
    current_state = ActorState.IDLE
    sprite_name = ActorStateNames[ActorState.IDLE]

    number_frames = 0
    current_frame = 0
    number_sequences = 0
    current_sequence = 0
    current_sequencer = SEQUENCERS[ActorState.IDLE]

    end_sequence = False

    size_x = MAP_TileX
    size_y = MAP_TileY

    position_x = 0
    position_y = 0

    mirrored = False
    moving = False
    running = False
    jumping = False
    falling = False

    actor_jump_y = 0
    actor_top_y = MAP_TileY * 4
    actor_step_y = actor_top_y / 16

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.path = os.path.join(sprites, name)
        for action, num_frames, num_sequences in self.ANIMATIONS.values():
            frames = []
            for frame in range(num_frames):
                filename = SPRITE_NAME.format(action, frame)
                frames.append(filename)
            self._files.update({action: frames})
        self.actor_layer = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)

        self.sprite_name, self.number_frames, self.number_sequences = self.ANIMATIONS[self.current_state]
        self.current_sequencer = self.SEQUENCERS[self.current_state]

    def draw(self):
        self.current_sequence = self.current_sequencer[self.current_frame]

        sprites = self._sprites[self.sprite_name]
        sprite = sprites[self.current_sequence]

        self.actor_layer.fill((0, 0, 0, 0))
        if self.mirrored:
            r_sprite = pygame.transform.flip(sprite, True, False)
            self.actor_layer.blit(r_sprite, (0, 0))
        else:
            self.actor_layer.blit(sprite, (0, 0))

    def update(self):
        if self.jumping:
            self.current_state = ActorState.JUMP
            self.actor_jump_y -= self.actor_step_y

        if self.falling:
            self.current_state = ActorState.FALL
            self.actor_jump_y += self.actor_step_y

        if self.end_sequence:
            if self.falling:
                self.jumping = False
                self.falling = False
                self.actor_jump_y = 0
            if self.jumping:
                self.jumping = False
                self.falling = True
                self.actor_jump_y = -self.actor_top_y

        self.current_frame += 1
        self.end_sequence = False
        if self.current_frame >= self.number_sequences:
            self.end_sequence = True
            self.current_frame = 0

        if self.current_state != self.preview_state:
            self.current_frame = 0
            self.sprite_name, self.number_frames, self.number_sequences = self.ANIMATIONS[self.current_state]
            self.current_sequencer = self.SEQUENCERS[self.current_state]

        self.preview_state = self.current_state

    def load_assets(self):
        for action, num_frames, num_sequences in self.ANIMATIONS.values():
            frames = []
            for frame in range(num_frames):
                fl = self._files[action][frame]
                filename = os.path.join(self.path, fl)
                level = pygame.image.load(filename)
                sprite = pygame.transform.scale(level, (self.size_x, self.size_y))
                frames.append(sprite)
            self._sprites.update({action: frames})

    def move_to(self, x, y):
        self.position_x = x
        self.position_y = y

    def move(self, delta_x, delta_y):
        self.position_x += delta_x
        self.position_y += delta_y
