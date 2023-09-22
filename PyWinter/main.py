from PyWinter.engine.screen import Screen
from PyWinter.engine.viewports import Viewport
from PyWinter.engine.gui import Gui
from PyWinter.levels import *
from PyWinter.characters import *


class Game:
    def __init__(self):
        self.screen = Screen(self)

        self.level = GameGround(self, (1, 1, 1))
        self.background = Winter01(self)
        self.gui = Gui(self)
        self.player = Player01(self)
        self.viewport = Viewport(self)

        self.timer = pygame.time.Clock()
        self.delta_time = 0
        self.delta_time = 0

        self.running = False

    def draw(self):
        self.viewport.draw()

        msg1 = f'FPS - {self.timer.get_fps():.01f}'
        tnr_font = pygame.font.SysFont('timesnewroman', 22)
        letters = tnr_font.render(msg1, False, 'black', (255, 255, 255, 0))
        self.screen.blit_buffer(letters, (0, 800), ScreenLayers.GUI_LAYERS, 0)

        # pygame.display.set_caption(f'FPS: {msg1} - Delta: {self.delta_time}')
        # pygame.display.set_caption(f'PXY {self.level.player_x, self.level.player_y} - VX {self.viewport.scroll_x} - GX {self.viewport.start_x}')

        self.screen.draw()
        self.screen.flip()

    def update(self):
        # self.delta_time = self.timer.tick(FPS)
        self.delta_time = self.timer.tick()

        # Execute physics and state updates
        self.viewport.update()

    def run(self):
        self.running = True
        self.screen.set_layers()
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
