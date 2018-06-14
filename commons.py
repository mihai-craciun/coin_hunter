import pygame
import os
import numpy as np

# Window and engine
FPS = 30
CAMERA_X = 0
CAMERA_Y = 0
SCALE = 4
BLOCKS_X = 8
BLOCKS_Y = 8
B_SIZE = 16
# define styles
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

# initialize pygame and create window
B_SIZE = B_SIZE * SCALE
WIDTH = BLOCKS_X * B_SIZE
HEIGHT = BLOCKS_Y * B_SIZE
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("pixelated.ttf", 8*SCALE)


# Map
class Map:
    def __init__(self):
        self.map = [[WATER for _ in range(HEIGHT//B_SIZE)]
                    for _ in range(WIDTH//B_SIZE)]

    def draw(self, screen):
        for i, line in enumerate(self.map):
            for j, item in enumerate(line):
                # Position
                pos = (i*B_SIZE - CAMERA_Y, j*B_SIZE - CAMERA_X)
                # Check if has terrain to draw
                for t in TERRAINS:
                    if item & t > 0:
                        screen.blit(PNGS[t], pos)
                        break
                for c in COLLECTIBLES:
                    if item & c > 0:
                        screen.blit(PNGS[c], pos)
        
