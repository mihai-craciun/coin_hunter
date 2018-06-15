import pygame
import os
from threading import Timer

# Window and engine
FPS = 60
CAMERA_X = 0
CAMERA_Y = 0
SCALE = 3
BLOCKS_X = 10
BLOCKS_Y = 10
B_SIZE = 16
# define styles
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEPGREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Item strings
ITEM_NAMES = [
    # Terrains
    "BLANK",
    "WATER",
    "DIRT",
    "GRASS",
    # Collectibles
    "TREE",
    "DRY_TREE",
    "DRY_TREE_BURN",
    "COIN",
    "BLUE_CRYSTAL",
    "RED_CRYSTAL",
]
v = 1
for it in ITEM_NAMES:
    exec("{0}={1}".format(it, v))
    v <<= 1

PLAYER = v

# PNG map
PNGS = {
    WATER: "water.png",
    DIRT: "terrain.png",
    GRASS: "grass.png",
    TREE: "tree.png",
    DRY_TREE: "dry_tree.png",
    DRY_TREE_BURN: "dry_tree_burn.png",
    COIN: "coin.png",
    BLUE_CRYSTAL: "blue_crystal.png",
    RED_CRYSTAL: "red_crystal.png",
}
# Load PNG
images_path = 'images/'
for k in PNGS:
    PNGS[k] = pygame.transform.scale(pygame.image.load(
        os.path.join(images_path+PNGS[k])), (B_SIZE*SCALE, B_SIZE*SCALE))
# Group
TERRAINS = [
    WATER,
    DIRT,
    GRASS,
]
COLLECTIBLES = [
    TREE,
    DRY_TREE,
    DRY_TREE_BURN,
    COIN,
    BLUE_CRYSTAL,
    RED_CRYSTAL,
]
# Special terrain
NONSTARTABLE = [
    WATER
]
ITEMS = TERRAINS + COLLECTIBLES

filters = {
    "TERRAINS": (v-1) ^ (2**(len(TERRAINS)+1)-1),
    "COLLECTIBLES": 2**(len(TERRAINS)+1)-1,
}

# initialize pygame and create window
B_SIZE = B_SIZE * SCALE
WIDTH = BLOCKS_X * B_SIZE
HEIGHT = BLOCKS_Y * B_SIZE
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("pixelated.ttf", 10*SCALE)


# Map
BLANK_SURFACE = pygame.Surface((B_SIZE, B_SIZE))
BLANK_SURFACE.fill(DEEPGREY)


class Map:
    def __init__(self, m=None, rows=8, cols=4):
        if m is not None:
            self.map = m
        else:
            self.map = [[BLANK for i in range(rows)]
                        for j in range(cols)]

    def draw(self, screen, cam_x=0, cam_y=0, scale=1):
        for i, line in enumerate(self.map):
            for j, item in enumerate(line):
                # Position
                pos = (i*B_SIZE*scale - cam_x, j*B_SIZE*scale - cam_y)
                # Check if has terrain to draw
                if item & BLANK > 0:
                    screen.blit(pygame.transform.scale(BLANK_SURFACE, (int(
                        BLANK_SURFACE.get_width()*scale),
                        int(BLANK_SURFACE.get_height()*scale))), pos)
                for t in TERRAINS:
                    if item & t > 0:
                        screen.blit(pygame.transform.scale(
                            PNGS[t], (int(PNGS[t].get_width()*scale), int(PNGS[t].get_height()*scale))), pos)
                        break
                for c in COLLECTIBLES:
                    if item & c > 0:
                        screen.blit(pygame.transform.scale(
                            PNGS[c], (int(PNGS[c].get_width()*scale), int(PNGS[c].get_height()*scale))), pos)

    def setbegin(self, x, y):
        if x >= len(self.map):
            return
        if y >= len(self.map[0]):
            return
        if y < 0:
            for i in range(len(self.map)):
                self.map[i] = [BLANK for _ in range(-y)] + self.map[i]
        if x < 0:
            self.map = [[BLANK for a in self.map[0]]
                        for b in range(-x)] + self.map
        if y > 0:
            for i in range(len(self.map)):
                self.map[i] = self.map[i][y:]
        if x > 0:
            self.map = self.map[x:]

    def setend(self, x, y):
        if x < 0:
            return
        if y < 0:
            return
        if y+1 > len(self.map[0]):
            for i in range(len(self.map)):
                self.map[i] = self.map[i] + \
                    [BLANK for _ in range(y-len(self.map[i])+1)]
        if x+1 > len(self.map):
            self.map = self.map + [[BLANK for a in self.map[0]]
                                   for b in range(x-len(self.map)+1)]
        if y+1 < len(self.map[0]):
            for i in range(len(self.map)):
                self.map[i] = self.map[i][:y+1]
        if x+1 < len(self.map):
            self.map = self.map[:x+1]

    def check(self):
        COINS = 0
        IS_PLAYER = False
        for line in self.map:
            for item in line:
                t = filters["COLLECTIBLES"] & item
                if t not in TERRAINS:
                    return "Missing terrain"
                c = filters["TERRAINS"] & item
                if c == COIN:
                    COINS += 1
                if item & PLAYER == PLAYER:
                    if IS_PLAYER == True:
                        return "Duplicate player"
                    elif c == 0 and t not in NONSTARTABLE:
                        IS_PLAYER = True
                    else:
                        print(c, t)
                        return "Player not in a starting position"
        if COINS == 0:
            return "No coins"
        if IS_PLAYER == False:
            return "No player"
        return None

    def get_player(self):
        for x, line in enumerate(self.map):
            for y, item in enumerate(line):
                if item & PLAYER == PLAYER:
                    return (x, y)

    def get_items(self, item):
        items = []
        for x, line in enumerate(self.map):
            for y, it in enumerate(line):
                if it & item == item:
                    items.append((x, y))
        return items

    def can_move(self, px, py, px2, py2, specials):
        if px2 == -1 or py2 == -1 or px2 >= len(self.map) or py2 >= len(self.map[0]):
            return False
        block = self.map[px2][py2]
        if block & TREE > 0 or block & DRY_TREE > 0 or block & DRY_TREE_BURN > 0:
            return False
        # special cases check specials items
        if specials & BLUE_CRYSTAL == 0 and block & WATER > 0:
            return False
        return True

    def get_collectible(self, x, y):
        item = None
        for c in COLLECTIBLES:
            if c & self.map[x][y]:
                item = c
        return item

    def remove_collectible(self, x, y):
        self.map[x][y] &= filters["COLLECTIBLES"]

    def burn(self, x, y, xdir, ydir, specials):
        BURN_TIMEOUT = 2
        if x+xdir < 0 or x+xdir == len(self.map) or y+ydir < 0 or y+ydir == len(self.map[0]):
            return False
        if specials & RED_CRYSTAL == 0:
            return False
        if self.map[x+xdir][y+ydir] & DRY_TREE == 0:
            return False
        self.map[x+xdir][y+ydir] = self.map[x +
                                            xdir][y+ydir] ^ DRY_TREE | DRY_TREE_BURN
        return True
    # DEBUG

    def printsize(self):
        print([len(self.map[i]) for i in range(len(self.map))])

    def printbock(self, x, y):
        print(self.map[x][y])
