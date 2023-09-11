from enum import Enum

TOL = 1e-6

# RES = WIDTH, HEIGHT = 1920, 1080
RES = WIDTH, HEIGHT = 1200, 900
# RES = WIDTH, HEIGHT = 640, 480
FPS = 50
TICKS = 50

MAP_Cols = 20
MAP_Rows = 15

MAP_TileX = WIDTH / MAP_Cols
MAP_TileY = HEIGHT / MAP_Rows

HALF_WIDTH = WIDTH / 2

THRESHOLD_LEFT = WIDTH / 4
THRESHOLD_RIGHT = WIDTH * 3 / 4

LEVEL_PATH = 'e{0:2d}w{0:2d}m{0:2d}'

NUM_EPISODES = 3
NUM_WORLDS = 10
NUM_MAPS = 5

EPISODES = range(NUM_EPISODES)
WORLDS = range(NUM_WORLDS)
MAPS = range(NUM_MAPS)

PLAYER_WALK_TIME = 3    # Number of seconds to go from 0 to WIDTH
PLAYER_SPEED = round(WIDTH/PLAYER_WALK_TIME/TICKS)


class PlayerState(Enum):
    IDLE = 0,
    WALK = 1,
    RUN = 2,
    JUMP = 3,
    FALL = 4,
    HURT = 5,
    DEAD = 6,
    SLIDE = 100
