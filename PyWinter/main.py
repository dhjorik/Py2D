from datetime import datetime
import os
import sys

import pygame
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
QKeys = Qt.Key

from PyWinter.engine.screen import Screen
from PyWinter.engine.viewports import Viewport
from PyWinter.engine.gui import Gui
from PyWinter.levels import *
from PyWinter.characters import *


class Game(QtWidgets.QMainWindow):
    key_pressed = []
    key_status = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyWinter Demo')
        self.setGeometry(0, 0, SCREEN_W, SCREEN_H)

        self.screen = Screen(self)

        self.level = GameGround(self, (1, 1, 1))
        self.background = Winter01(self)
        self.gui = Gui(self)
        self.player = Player01(self)
        self.viewport = Viewport(self)

        self.ticker = QtCore.QTimer(self)
        self.ticker.setInterval(TICK_MILLISECOND)
        self.ticker.setSingleShot(False)
        self.ticker.timeout.connect(self.update_gui)

        self.last_time = datetime.now()
        self.delta_time = 0
        self.fps = 0

        self.running = False

    def update_gui(self):
        if self.running:
            self.update_events()
            self.draw()
            self.check_next_events()
        else:
            self.close()

    def draw(self):
        self.viewport.draw()

        msg1 = f'FPS - {self.fps:.01f}'
        tnr_font = pygame.font.SysFont('timesnewroman', 22)
        letters = tnr_font.render(msg1, False, 'black', (255, 255, 255, 0))
        position = HEIGHT*8/10
        self.screen.blit_buffer(letters, (0, position), ScreenLayers.GUI_LAYERS, 0)
        self.screen.draw()

    def update_events(self):
        self.viewport.update()

        self.delta_time += 1
        # if self.delta_time > TICK_MILLISECOND:
        if True:
            self.delta_time = 0
            self.last_time = datetime.now()

            delta_time = datetime.now() - self.last_time

            if delta_time.microseconds == 0:
                time = delta_time.seconds * SECONDS
            else:
                time = delta_time.seconds * SECONDS + delta_time.microseconds / SECONDS
            if time == 0:
                self.fps = FPS
            else:
                self.fps = SECONDS / time
        self.ticker.start()

    def run(self):
        self.running = True
        self.show()
        self.screen.set_layers()
        self.ticker.start()

    def check_next_events(self):
        self.key_pressed = []
        #if QKeys.Key_Left in self.key_status:
        #    print('Key Left')
        #    self.key_pressed.append(pygame.K_LEFT)
        #if QKeys.Key_Right in self.key_status:
        #    print('Key Right')
        #    self.key_pressed.append(pygame.K_RIGHT)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        key_pressed = event.key()
        if key_pressed == QKeys.Key_Left:
            if pygame.K_LEFT not in self.key_pressed:
                self.key_pressed.append(pygame.K_LEFT)
            # if QKeys.Key_Left not in self.key_status:
            #    self.key_status.append(QKeys.Key_Left)
        if key_pressed == QKeys.Key_Right:
            if pygame.K_RIGHT not in self.key_pressed:
                self.key_pressed.append(pygame.K_RIGHT)
            #if QKeys.Key_Right not in self.key_status:
            #    self.key_status.append(QKeys.Key_Right)

        if key_pressed == QtCore.Qt.Key.Key_Q:
            self.running = False

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)

        key_pressed = event.key()
        if key_pressed == QKeys.Key_Right:
            if QKeys.Key_Right in self.key_status:
                self.key_status.remove(QKeys.Key_Right)
        if key_pressed == QKeys.Key_Left:
            if QKeys.Key_Left in self.key_status:
                self.key_status.remove(QKeys.Key_Left)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    pPass, pFail = pygame.init()

    # print(pygame.display.Info())
    game = Game()
    game.run()
    result = app.exec()

    pygame.quit()
    sys.exit(result)
