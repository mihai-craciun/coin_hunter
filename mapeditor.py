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

TEXT_CRT = FONT.render("Current   block:", False, WHITE)
TEXT_HELP_TOGGLE = FONT.render("help : H", False, WHITE)

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

    # Update
    all_sprites.update()
    # Update texts
    TEXT_Y = FONT.render("Y:{}".format(CRT_BLOCK_Y), False, WHITE)
    TEXT_X = FONT.render("X:{}".format(CRT_BLOCK_X), False, WHITE)
    # Get input
    keys = pygame.key.get_pressed()
    if MOVE_TICKER == 0:
        MOVE_TICKER = 3
        if keys[pygame.K_RIGHT]:
            CRT_BLOCK_X += 1
        if keys[pygame.K_LEFT]:
            CRT_BLOCK_X -= 1
        if keys[pygame.K_DOWN]:
            CRT_BLOCK_Y += 1
        if keys[pygame.K_UP]:
            CRT_BLOCK_Y -= 1
    if MOVE_TICKER > 0:
        MOVE_TICKER -= 1
    # Draw / Render
    screen.fill(BLACK)
    # Draw map
    game_map.draw(screen)
    # Draw blink
    screen.blit(CRT_BLOCK, (CRT_BLOCK_X*B_SIZE, CRT_BLOCK_Y*B_SIZE))
    # Draw stats
    screen.blit(TEXT_HELP_TOGGLE, (WIDTH - TEXT_HELP_TOGGLE.get_width(),
                                   HEIGHT - TEXT_HELP_TOGGLE.get_height()))
    screen.blit(TEXT_X, (10, HEIGHT - TEXT_X.get_height()*2))
    screen.blit(TEXT_Y, (10, HEIGHT - TEXT_X.get_height()))
    screen.blit(TEXT_CRT, (WIDTH - TEXT_CRT.get_width(), 0))
    all_sprites.draw(screen)
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
