import pygame
import os
import numpy as np

# Window and engine
FPS = 30
CAMERA_X = 0
CAMERA_Y = 0
SCALE = 3
BLOCKS_X = 16
BLOCKS_Y = 16
B_SIZE = 16
# define styles
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEPGREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Terrains
BLANK = 1
WATER = 2
DIRT = 4
DIRT_TREE = 8
DIRT_TREE_BURN = 16
# Collectibles
COIN = 32
BLUE_CRYSTAL = 64
RED_CRYSTAL = 128
# PNG map
PNGS = {
    WATER: "water.png",
    DIRT: "terrain.png",
    DIRT_TREE: "terrain_tree.png",
    DIRT_TREE_BURN: "terrain_tree_burn.png",
    COIN: "coin.png",
    BLUE_CRYSTAL: "blue_crystal.png",
    RED_CRYSTAL: "red_crystal.png",
}
# Load PNG
for k in PNGS:
    PNGS[k] = pygame.transform.scale(pygame.image.load(
        os.path.join(PNGS[k])), (B_SIZE*SCALE, B_SIZE*SCALE))
# Group
TERRAINS = [
    WATER,
    DIRT,
    DIRT_TREE,
    DIRT_TREE_BURN
]
COLLECTIBLES = [
    COIN,
    BLUE_CRYSTAL,
    RED_CRYSTAL
]
ITEMS = TERRAINS + COLLECTIBLES
# initialize pygame and create window
B_SIZE = B_SIZE * SCALE
WIDTH = BLOCKS_X * B_SIZE
HEIGHT = BLOCKS_Y * B_SIZE
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("pixelated.ttf", 8*SCALE)


# Map
BLANK_SURFACE = pygame.Surface((B_SIZE, B_SIZE))
BLANK_SURFACE.fill(DEEPGREY)


class Map:
    def __init__(self, rows=8, cols=4):
        self.map = [[WATER for i in range(rows)]
                    for j in range(cols)]
        self.map[1][0] |= COIN

    def draw(self, screen, cam_x=0, cam_y=0):
        for i, line in enumerate(self.map):
            for j, item in enumerate(line):
                # Position
                pos = (i*B_SIZE - cam_x, j*B_SIZE - cam_y)
                # Check if has terrain to draw
                if item == BLANK:
                    screen.blit(BLANK_SURFACE, pos)
                for t in TERRAINS:
                    if item & t > 0:
                        screen.blit(PNGS[t], pos)
                        break
                for c in COLLECTIBLES:
                    if item & c > 0:
                        screen.blit(PNGS[c], pos)

    def setbegin(self, x, y):
        if x >= len(self.map):
            return
        if y >= len(self.map[0]):
            return
        if y < 0:
            for i in range(len(self.map)):
                self.map[i] = [BLANK for _ in range(-y)] + self.map[i]
        if x < 0:
            self.map =[[BLANK for a in self.map[0]] for b in range(-x)] + self.map
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
                self.map[i] = self.map[i] + [BLANK for _ in range(y-len(self.map[i])+1)]
        if x+1 > len(self.map):
            self.map = self.map + [[BLANK for a in self.map[0]] for b in range(x-len(self.map)+1)]
        if y+1 < len(self.map[0]):
            for i in range(len(self.map)):
                self.map[i] = self.map[i][:y+1]
        if x+1 < len(self.map):
            self.map = self.map[:x+1]
    
    def printsize(self):
        print([len(self.map[i]) for i in range(len(self.map))])
    
    def printbock(self, x, y):
        print(self.map[x][y])