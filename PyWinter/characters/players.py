import pygame
from PyWinter.characters.actors import Actor
from PyWinter.engine.settings import *


class Player01(Actor):
    ANIMATIONS = {
        ActorState.IDLE: ('Idle', 10, 10),
        ActorState.WALK: ('Walk', 10, 10),
        ActorState.RUN:  ('Run', 8, 8),
        ActorState.JUMP: ('Jump', 8, 16),
        ActorState.FALL: ('Fall', 8, 16),
        ActorState.HURT: ('Hurt', 10, 10),
        ActorState.DEAD: ('Dead', 10, 10),
        ActorState.SLIDE: ('Slide', 10, 10),
    }

    SEQUENCERS = {
        ActorState.IDLE: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
        ActorState.WALK: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
        ActorState.RUN:  (0, 1, 2, 3, 4, 5, 6, 7,),
        ActorState.JUMP: (0, 1, 2, 3, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7,),
        ActorState.FALL: (0, 1, 2, 3, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7,),
        ActorState.HURT: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
        ActorState.DEAD: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
        ActorState.SLIDE: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,),
    }

    def __init__(self, game):
        super(Player01, self).__init__('player_01', game)
        self.load_assets()

    def update(self):
        super().update()

        if self.jumping or self.falling:
            return

        self.current_state = ActorState.IDLE
        self.moving = False
        self.running = False

        keys = self.game.key_pressed

        if pygame.K_UP in keys:
            self.current_state = ActorState.JUMP
            self.actor_jump_y = 0
            self.current_frame = 0
            self.jumping = True

        if pygame.K_RIGHT in keys:
            self.mirrored = False
            self.moving = True
            self.current_state = ActorState.WALK

        if pygame.K_LEFT in keys:
            self.mirrored = True
            self.moving = True
            self.current_state = ActorState.WALK

        if pygame.K_LSHIFT in keys:
            self.running = True
            self.current_state = ActorState.RUN
