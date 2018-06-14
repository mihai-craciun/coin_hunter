# Template for Pygame
import pygame
import random
import datetime
from sys import argv
from commons import *
from copy import deepcopy

# Inits
TITLE = "Map Editor"
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

ERROR = ""
ERROR_TICKER = 0

PLAYER_X = None
PLAYER_Y = None

if len(argv) == 1:
    game_map = Map()
else:
    try:
        with open(argv[1],'r') as loadmap:
            mapstring = loadmap.read()
        exec("lmap = {}".format(mapstring))
        game_map = Map(m=lmap)
        err = game_map.check()
        if err is not None:
            ERROR = "Invalid map, started new one"
            ERROR_TICKER = FPS*5
            game_map = Map()
        else:
            PLAYER_X, PLAYER_Y = game_map.get_player()
    except:
            ERROR = "Invalid map, started new one"
            ERROR_TICKER = FPS*5
            game_map = Map()    
CRT_BLOCK = pygame.Surface((B_SIZE, B_SIZE))
CRT_BLOCK.set_alpha(128)
CRT_BLOCK.fill(WHITE)

CAMERA_X = -WIDTH//2+(len(game_map.map)//2*B_SIZE)
CAMERA_Y = -HEIGHT//2+(len(game_map.map[0])//2*B_SIZE)

PLAYER_POS = pygame.Surface((B_SIZE, B_SIZE))
PLAYER_POS.set_alpha(128)
PLAYER_POS.fill(GREEN)

CRT_BLOCK_X = 0
CRT_BLOCK_Y = 0

SCALE = 1
ZOOM_RATIO = 2

TEXT_CRT = FONT.render("Current block:", False, WHITE)
TEXT_HELP_TOGGLE = FONT.render("Help : H", False, WHITE)

SHOW_HELP = False
TEXT_HELP_ITEMS = [
    "Help: H",
    "Save: S",
    "Quit: Q",
    "Zoom in: 1",
    "Zoom out: 2",
    "Move: Arrows",
    "Set player: P",
    "Set map end: E",
    "Set map begin: B",
    "Delete crt block: D",
    "Change crt item: Tab",
    "Change crt block t/c crt item: SPACE",
    "",
    "Open with argument map file to load previous map!"
]

for i in range(len(TEXT_HELP_ITEMS)):
    TEXT_HELP_ITEMS[i] = FONT.render(TEXT_HELP_ITEMS[i], False, WHITE)

ITEM_CRT = WATER
ITEM_CRT_SURFACE_OFFSET = 10
ITEM_CRT_SURFACE = pygame.Surface(
    (B_SIZE+2*ITEM_CRT_SURFACE_OFFSET, B_SIZE+2*ITEM_CRT_SURFACE_OFFSET))
ITEM_CRT_SURFACE.fill(WHITE)
ITEM_CRT_SURFACE.set_alpha(128)
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
            # Save map
            if event.key == pygame.K_s:
                error = game_map.check()
                if error is None:
                    mapstring = '{}'.format(game_map.map)
                    with open(('map_{}.map'.format(datetime.datetime.now())).replace(' ','_'),'w') as savefile:
                        savefile.write(mapstring)
                    running = False
                else:
                    ERROR = error
                    ERROR_TICKER = FPS*5
            if event.key == pygame.K_p:
                if CRT_BLOCK_X >= 0 and CRT_BLOCK_Y >= 0 and CRT_BLOCK_X < len(game_map.map) and CRT_BLOCK_Y < len(game_map.map[0]):
                    if PLAYER_X is not None and PLAYER_Y is not None and PLAYER_X < len(game_map.map) and PLAYER_Y < len(game_map.map[0]):
                        game_map.map[PLAYER_X][PLAYER_Y] ^= PLAYER
                    PLAYER_X = CRT_BLOCK_X
                    PLAYER_Y = CRT_BLOCK_Y
                    game_map.map[PLAYER_X][PLAYER_Y] |= PLAYER
            # Debug
            if event.key == pygame.K_9:
                game_map.printsize()
            if event.key == pygame.K_0:
                game_map.printbock(CRT_BLOCK_X, CRT_BLOCK_Y)
            if event.key == pygame.K_1:
                SCALE *= ZOOM_RATIO
            if event.key == pygame.K_2:
                SCALE /= ZOOM_RATIO
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_TAB:
                # Change current item
                ITEM_CRT = ITEMS[(ITEMS.index(ITEM_CRT)+1) % len(ITEMS)]
            if event.key == pygame.K_b:
                game_map.setbegin(CRT_BLOCK_X, CRT_BLOCK_Y)
                if CRT_BLOCK_X < 0:
                    CAMERA_X -= B_SIZE * CRT_BLOCK_X
                    CRT_BLOCK_X = 0
                if CRT_BLOCK_Y < 0:
                    CAMERA_Y -= B_SIZE * CRT_BLOCK_Y
                    CRT_BLOCK_Y = 0
                if CRT_BLOCK_X >= len(game_map.map):
                    CAMERA_X -= B_SIZE * (CRT_BLOCK_X - len(game_map.map))
                    CRT_BLOCK_X = len(game_map.map)-1
                if CRT_BLOCK_Y >= len(game_map.map[0]):
                    CAMERA_Y -= B_SIZE * (CRT_BLOCK_Y - len(game_map.map[0]))
                    CRT_BLOCK_Y = len(game_map.map[0])-1
            if event.key == pygame.K_e:
                game_map.setend(CRT_BLOCK_X, CRT_BLOCK_Y)
                if CRT_BLOCK_X >= len(game_map.map):
                    CRT_BLOCK_X = len(game_map.map)-1
                if CRT_BLOCK_X < 0:
                    CRT_BLOCK_X = 0
                if CRT_BLOCK_Y >= len(game_map.map):
                    CRT_BLOCK_Y = len(game_map.map[0])-1
                if CRT_BLOCK_Y < 0:
                    CRT_BLOCK_Y = 0

    # Update
    all_sprites.update()
    # Update texts
    TEXT_Y = FONT.render("Y:{}".format(CRT_BLOCK_Y), False, WHITE)
    TEXT_X = FONT.render("X:{}".format(CRT_BLOCK_X), False, WHITE)
    TEXT_SIZE = FONT.render("Size:{0}x{1}".format(
        len(game_map.map), len(game_map.map[0])), False, WHITE)
    # Get input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]:
        SHOW_HELP = True
    if CRT_BLOCK_Y > -1 and CRT_BLOCK_Y < len(game_map.map[0]) and CRT_BLOCK_X > -1 and CRT_BLOCK_X < len(game_map.map):
        # Only on map
        if keys[pygame.K_SPACE]:
            # Changing item type with existing
            if ITEM_CRT in TERRAINS:
                f = filters["TERRAINS"]
            else:
                f = filters["COLLECTIBLES"]
            game_map.map[CRT_BLOCK_X][CRT_BLOCK_Y] = (game_map.map[CRT_BLOCK_X][CRT_BLOCK_Y] & f) | ITEM_CRT
        if keys[pygame.K_d]:
            game_map.map[CRT_BLOCK_X][CRT_BLOCK_Y] = BLANK
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
    if ERROR_TICKER > 0:
        ERROR_TICKER -= 1
    SCALED_CAMERA_X = CAMERA_X * SCALE
    SCALED_CAMERA_Y = CAMERA_Y * SCALE
    # Draw / Render
    screen.fill(BLACK)
    # Draw map
    game_map.draw(screen, cam_x=SCALED_CAMERA_X, cam_y=SCALED_CAMERA_Y, scale=SCALE)
    # Draw player block
    if PLAYER_X is not None and PLAYER_Y is not None and PLAYER_X < len(game_map.map) and PLAYER_Y < len(game_map.map[0]):
        screen.blit(pygame.transform.scale(PLAYER_POS,
                                       (int(CRT_BLOCK.get_width()*SCALE), int(CRT_BLOCK.get_height()*SCALE))), (PLAYER_X*B_SIZE*SCALE -
                                                                                                                SCALED_CAMERA_X, PLAYER_Y*B_SIZE*SCALE - SCALED_CAMERA_Y))
    # Draw Current block
    screen.blit(pygame.transform.scale(CRT_BLOCK,
                                       (int(CRT_BLOCK.get_width()*SCALE), int(CRT_BLOCK.get_height()*SCALE))), (CRT_BLOCK_X*B_SIZE*SCALE -
                                                                                                                SCALED_CAMERA_X, CRT_BLOCK_Y*B_SIZE*SCALE - SCALED_CAMERA_Y))
    # Draw stats
    screen.blit(TEXT_HELP_TOGGLE, (WIDTH - TEXT_HELP_TOGGLE.get_width(),
                                   HEIGHT - TEXT_HELP_TOGGLE.get_height()))
    screen.blit(TEXT_X, (10, HEIGHT - TEXT_X.get_height()*3))
    screen.blit(TEXT_Y, (10, HEIGHT - TEXT_X.get_height()*2))
    screen.blit(TEXT_SIZE, (10, HEIGHT - TEXT_X.get_height()))
    screen.blit(TEXT_CRT, (WIDTH - TEXT_CRT.get_width(), 0))
    screen.blit(ITEM_CRT_SURFACE, (WIDTH -
                                   ITEM_CRT_SURFACE.get_width() - 10,
                                   TEXT_CRT.get_height()))
    screen.blit(PNGS[ITEM_CRT], (WIDTH - ITEM_CRT_SURFACE.get_width() -
                                 10 + 10, TEXT_CRT.get_height()+10))

    if SHOW_HELP:
        for i, s in enumerate(TEXT_HELP_ITEMS):
            screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT //
                            2 - (len(TEXT_HELP_ITEMS)-i)*s.get_height()))
        SHOW_HELP = False
    if ERROR_TICKER > 0:
        er = FONT.render(ERROR, False, RED)
        screen.blit(er, (WIDTH//2-er.get_width()//2, HEIGHT-er.get_height()*2))
    all_sprites.draw(screen)
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
