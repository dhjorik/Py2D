import pygame
from OpenGL.GL import *

from PyWinter.engine.settings import *


class ScreenLayers:
    BACK_LAYERS = 0
    GAME_LAYERS = 1
    FRONT_LAYERS = 2
    SFX_LAYERS = 3
    GUI_LAYERS = 4


class Screen:
    offsets = [0, 0, 0, 0, 0]

    num_layers = 1
    layers = [None]
    buffer = None

    def __init__(self, game):
        self.game = game

        flags = SCREEN_FLAGS
        self.screen = pygame.display.set_mode(SCREEN_RES, flags)
        # self.screen = pygame.display.set_mode(SCREEN_RES)

        self.info = pygame.display.Info()
        self._setup_opengl()

        self.texID = glGenTextures(1)

        print(pygame.display.get_driver())
        print(pygame.display.get_surface())

    def set_layers(self):
        self.num_layers = self.game.background.NUM_BACK_LAYERS
        self.offsets[ScreenLayers.GAME_LAYERS] = self.num_layers
        self.num_layers += self.game.level.LAYERS
        self.offsets[ScreenLayers.FRONT_LAYERS] = self.num_layers
        self.num_layers += self.game.background.NUM_FRONT_LAYERS
        self.offsets[ScreenLayers.SFX_LAYERS] = self.num_layers
        self.num_layers += self.game.background.SPECIALS
        self.offsets[ScreenLayers.GUI_LAYERS] = self.num_layers
        self.num_layers += self.game.gui.LAYERS

        self.layers = [None] * self.num_layers
        self.buffer = pygame.Surface(RES, pygame.SRCALPHA, 32)

    def blit(self, source, destination, area=None, special_flags=0):
        return self.buffer.blit(source, destination, area, special_flags)

    def blit_buffer(self, source, destination, layer=ScreenLayers.BACK_LAYERS, index=0):
        to_layer = index + Screen.offsets[layer]
        self.layers[to_layer] = (source, destination)
        return True

    def flip(self):
        pygame.display.flip()
        pass

    def draw(self):
        if len(self.layers) > 0:
            self.buffer.blits([lay for lay in self.layers if lay is not None])
        else:
            self.buffer.fill((0, 0, 0, 0))
        # self.screen.blit(self.buffer, (0, 0))

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glClearColor(0, 0, 0, 1.0)

        # draw texture openGL Texture
        self._surface_to_texture(self.buffer)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-1, 1)
        glTexCoord2f(0, 1)
        glVertex2f(-1, -1)
        glTexCoord2f(1, 1)
        glVertex2f(1, -1)
        glTexCoord2f(1, 0)
        glVertex2f(1, 1)
        glEnd()

    def update(self):
        self.layers = [None] * self.num_layers

    def _setup_opengl(self):
        glViewport(0, 0, self.info.current_w, self.info.current_h)
        glDepthRange(0, 1)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_BLEND)

    def _setup_fonts(self):
        self.default_font12 = pygame.font.Font(None, 12)
        self.default_font24 = pygame.font.Font(None, 24)

    def _surface_to_texture(self,  pygame_surface):
        rgb_surface = pygame.image.tostring(pygame_surface, 'RGB')
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        s_rect = pygame_surface.get_rect()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, s_rect.width, s_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_surface)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
