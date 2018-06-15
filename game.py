# Template for Pygame
import pygame
import random
import sys
import os
import time
from commons import *

# Inits
TITLE = "Find the coins"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

if len(sys.argv) == 1:
    with open('defaultmap.map', 'r') as mapfile:
        ms = mapfile.read()
        exec("gmap={}".format(ms))
        game_map = Map(m=gmap)
else:
    with open(sys.argv[1], 'r') as mapfile:
        try:
            mapstring = mapfile.read()
            exec("gmap={}".format(mapstring))
            game_map = Map(m=gmap)
            if game_map.check() is not None:
                print('Invalid map loaded, exiting.')
                sys.exit(0)
        except:
            print('Invalid map loaded, exiting.')
            sys.exit(0)

TOTAL_COINS = len(game_map.get_items(COIN))
TIME_INITIAL = time.time()

BURNING_TREES = []

SHOW_HELP = False
TEXT_HELP_ITEMS = [
    "The game goal is to collect",
    " all the coins. You can",
    "walk on water if you have", 
    "the blue crystal, and you",
    "can burn dry trees if you",
    "have the white crystal.",
    "",
    "Help : H",
    "Move : Arrows",
    "Burn : SPACE",
    "Quit : Q",
]

for i,t in enumerate(TEXT_HELP_ITEMS):
    TEXT_HELP_ITEMS[i] = FONT.render(TEXT_HELP_ITEMS[i], False, WHITE)

def tomapcoord(coord):
    return int(coord/B_SIZE)

class Player(pygame.sprite.Sprite):

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    WALK = 0
    BURN = 1
    GET_COIN = 2
    GET_CRYSTAL = 3

    HITBOX = B_SIZE//2
    TICKER = FPS//12

    @staticmethod
    def getscaled(img_name):
        path = 'images/player/'
        ext = '.png'
        return pygame.transform.scale(pygame.image.load(os.path.join(path+img_name+ext)), (B_SIZE, B_SIZE))

    def __init__(self):
        super().__init__()
        global CAMERA_X, CAMERA_Y
        self.images = {
            Player.UP: [
                Player.getscaled('link_up_1'),
                Player.getscaled('link_up_2'),
            ],
            Player.DOWN: [
                Player.getscaled('link_down_1'),
                Player.getscaled('link_down_2'),
            ],
            Player.LEFT: [
                Player.getscaled('link_left_1'),
                Player.getscaled('link_left_2'),
            ],
            Player.RIGHT: [
                Player.getscaled('link_right_1'),
                Player.getscaled('link_right_2'),
            ],
        }
        sounds_path = 'sfx/'
        self.sounds = {
            Player.WALK: pygame.mixer.Sound(sounds_path+'footstep.wav'),
            Player.BURN: pygame.mixer.Sound(sounds_path+'burn.wav'),
            Player.GET_COIN: pygame.mixer.Sound(sounds_path+'coin.wav'),
            Player.GET_CRYSTAL: pygame.mixer.Sound(sounds_path+'crystal.wav'),
        }

        self.hitbox = pygame.Surface((Player.HITBOX, Player.HITBOX))
        self.rect = self.hitbox.get_rect()
        self.x, self.y = game_map.get_player()
        self.x *= B_SIZE
        self.y *= B_SIZE
        self.rect.center = WIDTH//2, HEIGHT//2
        self.items = 0
        self.coins = 0
        self.speed = int(0.1 * B_SIZE)
        self.orient = Player.DOWN
        self.count = 0
        self.count_ticker = Player.TICKER
        self.sounds[Player.WALK].set_volume(0.1)
        self.specials = 0 # No special
    
    def collect(self, x, y, item):
        game_map.remove_collectible(x,y)
        if item is None:
            return
        if item == COIN:
            self.sounds[Player.GET_COIN].play()
            self.coins+=1
            return
        self.sounds[Player.GET_CRYSTAL].play()
        self.specials |= item
        return

    def update(self):
        global SHOW_HELP
        keystate = pygame.key.get_pressed()
        # Verify if switch image
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_LEFT] or keystate[pygame.K_UP] or keystate[pygame.K_DOWN]:
            self.count_ticker -= 1
            if self.count_ticker == 0:
                # self.sounds[Player.WALK].play()
                self.count_ticker = Player.TICKER
                self.count = (self.count + 1) % 2
        self.image = self.images[self.orient][self.count]

        HITBOX_OFFSET = 3*B_SIZE//4

        mapx = tomapcoord(player.x + HITBOX_OFFSET)
        mapy = tomapcoord(player.y + HITBOX_OFFSET)

        if keystate[pygame.K_RIGHT]:
            RIGHT_OFFSET = HITBOX_OFFSET
            nextmapy = mapy
            nextmapx = tomapcoord(player.x+self.speed + RIGHT_OFFSET)
            if game_map.can_move(mapx, mapy, nextmapx, nextmapy, self.specials):
                item = game_map.get_collectible(nextmapx, nextmapy)
                player.collect(nextmapx, nextmapy, item)
                self.x += self.speed
            self.orient = Player.RIGHT
        if keystate[pygame.K_LEFT]:
            LEFT_OFFSET = (HITBOX_OFFSET//4 if player.x-self.speed >=0 else -HITBOX_OFFSET)
            nextmapy = mapy
            nextmapx = tomapcoord(player.x-self.speed + LEFT_OFFSET)
            if game_map.can_move(mapx, mapy, nextmapx, nextmapy, self.specials):
                item = game_map.get_collectible(nextmapx, nextmapy)
                player.collect(nextmapx, nextmapy, item)
                self.x -= self.speed
            self.orient = Player.LEFT
        if keystate[pygame.K_UP]:
            UP_OFFSET = (HITBOX_OFFSET if player.y-self.speed >=0 else -HITBOX_OFFSET)
            nextmapy = tomapcoord(player.y-self.speed + UP_OFFSET)
            nextmapx = mapx
            if game_map.can_move(mapx, mapy, nextmapx, nextmapy, self.specials):
                item = game_map.get_collectible(nextmapx, nextmapy)
                player.collect(nextmapx, nextmapy, item)
                self.y -= self.speed
            self.orient = Player.UP
        if keystate[pygame.K_DOWN]:
            DOWN_OFFSET = HITBOX_OFFSET + 10
            nextmapy = tomapcoord(player.y+self.speed + DOWN_OFFSET)
            nextmapx = mapx
            if game_map.can_move(mapx, mapy, nextmapx, nextmapy, self.specials):
                item = game_map.get_collectible(nextmapx, nextmapy)
                player.collect(nextmapx, nextmapy, item)
                self.y += self.speed
            self.orient = Player.DOWN
        if keystate[pygame.K_SPACE]:
            if self.orient == Player.UP:
                nx = 0
                ny = -1
            if self.orient == Player.DOWN:
                nx = 0
                ny = 1
            if self.orient == Player.LEFT:
                nx = -1
                ny = 0
            if self.orient == Player.RIGHT:
                nx = 1
                ny = 0
            if game_map.burn(mapx, mapy, nx, ny, self.specials):
                self.sounds[Player.BURN].play()
                BURNING_TREES.append([2*FPS, mapx+nx, mapy+ny])
        if keystate[pygame.K_h]:
            SHOW_HELP = True

    def draw(self, screen):
        screen.blit(self.image, (WIDTH//2-self.image.get_width() //
                                 2, HEIGHT//2-self.image.get_height()//2))


player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
            if event.key == pygame.K_q:
                running = False
    # Update
    all_sprites.update()
    # Update writables
    TEXT_X = FONT.render('X : {}'.format(tomapcoord(player.x)), False, WHITE)
    TEXT_Y = FONT.render('Y : {}'.format(tomapcoord(player.y)), False, WHITE)
    TEXT_COINS = FONT.render('Coins : {0}/{1}'.format(player.coins, TOTAL_COINS), False, WHITE)
    TEXT_SPECIALS = FONT.render('Specials :', False, WHITE)
    TIME_NOW = int(time.time() - TIME_INITIAL)
    TEXT_TIME = FONT.render('Time : {0:02d}:{1:02d}'.format(TIME_NOW//60, TIME_NOW%60), False, WHITE)
    TEXT_HELP = FONT.render('Help : H', False, WHITE)
    # Update burning trees
    i = 0
    while i < len(BURNING_TREES):
        if BURNING_TREES[i][0] == 0:
            game_map.map[BURNING_TREES[i][1]][BURNING_TREES[i][2]]^=DRY_TREE_BURN
            BURNING_TREES = BURNING_TREES[:i]+BURNING_TREES[i+1:]
            i-=1
        else:
            BURNING_TREES[i][0] = BURNING_TREES[i][0]-1
        i+=1
    # Draw / Render
    screen.fill(BLACK)
    game_map.draw(screen, cam_x=-WIDTH//2+player.x+player.hitbox.get_width() //
                  2, cam_y=-HEIGHT//2+player.y+player.hitbox.get_height()//2)
    all_sprites.draw(screen)
    # Draw stats
    if player.coins == TOTAL_COINS:
        WIN = FONT.render('You won!', False, WHITE)
        screen.blit(WIN, (WIDTH//2 - WIN.get_width()//2, HEIGHT//2 - WIN.get_height()//2))
    MARGIN_OFFSET = 10
    screen.blit(TEXT_X, (MARGIN_OFFSET, -MARGIN_OFFSET + HEIGHT - TEXT_X.get_height()*2))
    screen.blit(TEXT_Y, (MARGIN_OFFSET, -MARGIN_OFFSET + HEIGHT - TEXT_X.get_height()))
    screen.blit(PNGS[COIN], (TEXT_COINS.get_width()+ MARGIN_OFFSET ,0))
    screen.blit(TEXT_COINS, (MARGIN_OFFSET, PNGS[COIN].get_height()//2 - TEXT_COINS.get_height()//2))
    screen.blit(TEXT_SPECIALS, (MARGIN_OFFSET, PNGS[COIN].get_height()))
    screen.blit(TEXT_HELP, (WIDTH - TEXT_HELP.get_width() - MARGIN_OFFSET, HEIGHT - TEXT_HELP.get_height() - MARGIN_OFFSET))
    if SHOW_HELP:
        SHOW_HELP = False
        for i,t in enumerate(TEXT_HELP_ITEMS):
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - (len(TEXT_HELP_ITEMS) - i*2 )*t.get_height()//2))
    SPEC_OFFSET = 0
    for c in COLLECTIBLES:
        if c&player.specials:
            screen.blit(PNGS[c], (MARGIN_OFFSET + TEXT_SPECIALS.get_width() + SPEC_OFFSET*PNGS[c].get_width(), 3*PNGS[COIN].get_width()//4))
            SPEC_OFFSET+=1
    screen.blit(TEXT_TIME, (WIDTH - TEXT_TIME.get_width() - MARGIN_OFFSET, MARGIN_OFFSET))
    # *after* drawing everything
    pygame.display.flip()
    if player.coins == TOTAL_COINS:
        time.sleep(1)
        sys.exit(0)

pygame.quit()
