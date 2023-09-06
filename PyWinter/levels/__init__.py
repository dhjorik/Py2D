import os
import sys


_this = sys.modules[__name__]
_path = os.path.dirname(__file__)

LEVEL_PATH = 'e{0:2d}w{0:2d}m{0:2d}'

NUM_EPISODES = 3
NUM_WORLDS = 10
NUM_MAPS = 5

EPISODES = range(NUM_EPISODES)
WORLDS = range(NUM_WORLDS)
MAPS = range(NUM_MAPS)

