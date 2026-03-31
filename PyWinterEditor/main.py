import os, os.path

import pygame
import sys
import csv

from pyopencl.characterize import _check_for_pocl_arg_count_bug

# import pickle

import button

from PyWinter.engine.settings import *

this = sys.modules[__name__]
mpath = os.path.dirname(__file__)

path_level = 'level'
path_gui = 'gui'
path_img = 'img'
# path_bkg = 'img/orig/background'
# path_tile = 'img/orig/tile'
path_bkg = 'img/1/background'
path_tile = 'img/1/tiles'


# game window
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# define game variables
ROWS = MAP_Rows
MAX_COLS = 400 # MAP_Cols * 10
TILE_SIZE = MAP_TileX
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 5

# define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

img_list = []

pine1_img = None
pine2_img = None
mountain_img = None
sky_img = None

load_img = None
load_button = None
save_img = None
save_button = None

clock = None
screen = None
font = None
world_data = []
button_list = []


def init_engine():
    pygame.init()

    this.clock = pygame.time.Clock()
    this.screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
    pygame.display.set_caption('Level Editor')

    # define font
    this.font = pygame.font.SysFont('timesnewroman', 16)

    # create empty tile list
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        this.world_data.append(r)

    # create ground
    for tile in range(0, MAX_COLS):
        this.world_data[ROWS - 1][tile] = 0

def load_assets():
    # load images
    sprite1 = pygame.image.load(os.path.join(mpath, path_bkg, 'pine1.png'))
    this.pine1_img = pygame.transform.scale(sprite1, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    sprite2 = pygame.image.load(os.path.join(mpath, path_bkg, 'pine2.png'))
    this.pine2_img = pygame.transform.scale(sprite2, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    sprite3 = pygame.image.load(os.path.join(mpath, path_bkg, 'mountain.png'))
    this.mountain_img = pygame.transform.scale(sprite3, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    sprite4 = pygame.image.load(os.path.join(mpath, path_bkg, 'sky_cloud.png'))
    this.sky_img = pygame.transform.scale(sprite4, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

    # Count tiles in path_tile
    full_dir = os.path.join(mpath, path_tile)
    TILE_TYPES = len([name for name in os.listdir(full_dir) if os.path.isfile(os.path.join(full_dir, name))])
    for x in range(TILE_TYPES):
        img = pygame.image.load(os.path.join(mpath, path_tile, f'{x}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        this.img_list.append(img)

    this.save_img = pygame.image.load(os.path.join(mpath, path_gui, 'save_btn.png')).convert_alpha()
    this.load_img = pygame.image.load(os.path.join(mpath, path_gui, 'load_btn.png')).convert_alpha()

    # create buttons
    this.save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
    this.load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
    # make a button list
    button_col = 0
    button_row = 0
    for i in range(len(img_list)):
        tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
        this.button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        #screen.blit(sky_img, ((x * width) - this.scroll * 0.5, 0))
        #screen.blit(mountain_img, ((x * width) - this.scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        #screen.blit(pine1_img, ((x * width) - this.scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        #screen.blit(pine2_img, ((x * width) - this.scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))
        screen.blit(sky_img, (0, 0))
        screen.blit(mountain_img, (0, 0))
        screen.blit(pine1_img, (0, 0))
        screen.blit(pine2_img, (0, 0))

def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - this.scroll, 0), (c * TILE_SIZE - this.scroll, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - this.scroll, y * TILE_SIZE))


init_engine()
load_assets()

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    text1 = f'Level: {level} - Scroll position: {scroll}'
    draw_text(text1, font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        # save level data
        with open(os.path.join(mpath, f'level{level}_data.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    # alternative pickle method
    # pickle_out = open(f'level{level}_data', 'wb')
    # pickle.dump(world_data, pickle_out)
    # pickle_out.close()
    if load_button.draw(screen):
        # load in level data
        # reset scroll back to the start of the level
        this.scroll = 0
        with open(os.path.join(mpath, f'level{level}_data.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    # alternative pickle method
    # world_data = []
    # pickle_in = open(f'level{level}_data', 'rb')
    # world_data = pickle.load(pickle_in)

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left == True and this.scroll > 0:
        this.scroll -= 5 * this.scroll_speed
    if scroll_right == True and this.scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        this.scroll += 5 * this.scroll_speed

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = round((pos[0] + this.scroll) // TILE_SIZE)
    y = round(pos[1] // TILE_SIZE)

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                this.scroll_left = True
            if event.key == pygame.K_RIGHT:
                this.scroll_right = True
            if event.key == pygame.K_RSHIFT:
                this.scroll_speed = 15

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                this.scroll_left = False
            if event.key == pygame.K_RIGHT:
                this.scroll_right = False
            if event.key == pygame.K_RSHIFT:
                this.scroll_speed = 5

    pygame.display.update()

pygame.quit()
