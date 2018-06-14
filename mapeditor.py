# Template for Pygame
import pygame
import random
from commons import *

# Inits
TITLE = "Map Editor"
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
game_map = Map()
CRT_BLOCK = pygame.Surface((B_SIZE, B_SIZE))
CRT_BLOCK.set_alpha(128)
CRT_BLOCK.fill(WHITE)

CRT_BLOCK_X = 0
CRT_BLOCK_Y = 0

TEXT_CRT = FONT.render("Current block:", False, WHITE)
TEXT_HELP_TOGGLE = FONT.render("Help : H", False, WHITE)

TEXT_HELP_ITEMS = [
    "Help: H",
    "Set map begin: B",
    "Set map finish: F",
    "Delete crt: D",
    "XOR crt: SPACE",
    "Change item: Tab",
    "Move: Arrows",
]

for i in range(len(TEXT_HELP_ITEMS)):
    TEXT_HELP_ITEMS[i] = FONT.render(TEXT_HELP_ITEMS[i], False, WHITE)

ITEM_CRT = WATER
ITEM_CRT_SURFACE_OFFSET = 10
ITEM_CRT_SURFACE = pygame.Surface(
    (B_SIZE+2*ITEM_CRT_SURFACE_OFFSET, B_SIZE+2*ITEM_CRT_SURFACE_OFFSET))
ITEM_CRT_SURFACE.fill(WHITE)
ITEM_CRT_SURFACE.set_alpha(128)
SHOW_HELP = False
MOVE_TICKER = 3

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_map.printsize()
            if event.key == pygame.K_2:
                game_map.printbock(CRT_BLOCK_X, CRT_BLOCK_Y)
            if event.key == pygame.K_TAB:
                # Change current item
                ITEM_CRT = ITEMS[(ITEMS.index(ITEM_CRT)+1) % len(ITEMS)]
            if CRT_BLOCK_Y > -1 and CRT_BLOCK_Y < len(game_map.map[0]) and CRT_BLOCK_X > -1 and CRT_BLOCK_X < len(game_map.map):
                # Only on map
                if event.key == pygame.K_SPACE:
                    # Changing item type with existing
                    game_map.map[CRT_BLOCK_X][CRT_BLOCK_Y] ^= ITEM_CRT
                if event.key == pygame.K_d:
                    game_map.map[CRT_BLOCK_X][CRT_BLOCK_Y] = BLANK
            if event.key == pygame.K_b:
                game_map.setbegin(CRT_BLOCK_X, CRT_BLOCK_Y)
                if CRT_BLOCK_X < 0:
                    CAMERA_X -= B_SIZE * CRT_BLOCK_X
                    CRT_BLOCK_X = 0
                if CRT_BLOCK_Y < 0:
                    CAMERA_Y -= B_SIZE * CRT_BLOCK_Y
                    CRT_BLOCK_Y = 0
                if CRT_BLOCK_X > 0:
                    CAMERA_X -= B_SIZE * CRT_BLOCK_X
                    CRT_BLOCK_X = 0
                if CRT_BLOCK_Y > 0:
                    CAMERA_Y -= B_SIZE * CRT_BLOCK_Y
                    CRT_BLOCK_Y = 0
            if event.key == pygame.K_e:
                game_map.setend(CRT_BLOCK_X, CRT_BLOCK_Y)
                if CRT_BLOCK_X >= len(game_map.map):
                    CRT_BLOCK_X = len(game_map.map)-1
                if CRT_BLOCK_Y < 0:
                    CRT_BLOCK_Y = 0
                if CRT_BLOCK_X <= len(game_map.map):
                    CRT_BLOCK_X = len(game_map.map)-1
                if CRT_BLOCK_Y > 0:
                    CRT_BLOCK_Y > 0

    # Update
    all_sprites.update()
    # Update texts
    TEXT_Y = FONT.render("Y:{}".format(CRT_BLOCK_Y), False, WHITE)
    TEXT_X = FONT.render("X:{}".format(CRT_BLOCK_X), False, WHITE)
    TEXT_SIZE = FONT.render("Size:{0}x{1}".format(len(game_map.map), len(game_map.map[0])), False, WHITE)
    # Get input
    keys = pygame.key.get_pressed()
    if MOVE_TICKER == 0 and set(keys) != set([0]):
        MOVE_TICKER = 3
        if keys[pygame.K_RIGHT]:
            CRT_BLOCK_X += 1
            if CRT_BLOCK_X*B_SIZE - CAMERA_X >= WIDTH:
                CAMERA_X += B_SIZE
        if keys[pygame.K_LEFT]:
            CRT_BLOCK_X -= 1
            if CRT_BLOCK_X*B_SIZE - CAMERA_X < 0:
                CAMERA_X -= B_SIZE
        if keys[pygame.K_DOWN]:
            CRT_BLOCK_Y += 1
            if CRT_BLOCK_Y*B_SIZE - CAMERA_Y >= HEIGHT:
                CAMERA_Y += B_SIZE
        if keys[pygame.K_UP]:
            CRT_BLOCK_Y -= 1
            if CRT_BLOCK_Y*B_SIZE - CAMERA_Y < 0:
                CAMERA_Y -= B_SIZE
    if MOVE_TICKER > 0:
        MOVE_TICKER -= 1
    # Draw / Render
    screen.fill(BLACK)
    # Draw map
    game_map.draw(screen, cam_x=CAMERA_X, cam_y=CAMERA_Y)
    # Draw blink
    screen.blit(CRT_BLOCK, (CRT_BLOCK_X*B_SIZE -
                            CAMERA_X, CRT_BLOCK_Y*B_SIZE - CAMERA_Y))
    # Draw stats
    screen.blit(TEXT_HELP_TOGGLE, (WIDTH - TEXT_HELP_TOGGLE.get_width(),
                                   HEIGHT - TEXT_HELP_TOGGLE.get_height()))
    screen.blit(TEXT_X, (10, HEIGHT - TEXT_X.get_height()*3))
    screen.blit(TEXT_Y, (10, HEIGHT - TEXT_X.get_height()*2))
    screen.blit(TEXT_SIZE, (10, HEIGHT - TEXT_X.get_height()))
    screen.blit(TEXT_CRT, (WIDTH - TEXT_CRT.get_width(), 0))
    screen.blit(ITEM_CRT_SURFACE, (WIDTH -
                                   ITEM_CRT_SURFACE.get_width() - 10, TEXT_CRT.get_height()))
    screen.blit(PNGS[ITEM_CRT], (WIDTH - ITEM_CRT_SURFACE.get_width() -
                                 10 + 10, TEXT_CRT.get_height()+10))
    all_sprites.draw(screen)
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
