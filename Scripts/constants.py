from enum import Enum
from collections import namedtuple

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MARGIN = 50
OFFSET = 10 # Do not change
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
TILE_RADIUS = 20

Owner = Enum('Owner', 'NONE, BLACK, RED')
Move = Enum('Move', 'PLACE, TAKE, MOVE1, MOVE2')
TileMove = namedtuple("Point", "frm, to")