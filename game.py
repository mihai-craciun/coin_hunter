# Template for Pygame
import pygame
import random
import sys
import os
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


class Player(pygame.sprite.Sprite):

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    WALK = 0

    HITBOX = B_SIZE//2
    TICKER = FPS//12

    @staticmethod
    def getscaled(img_name):
        path = 'player/'
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
        self.sounds = {
            Player.WALK: pygame.mixer.Sound('footstep.wav')
        }

        self.hitbox = pygame.Surface((Player.HITBOX, Player.HITBOX))
        self.rect = self.hitbox.get_rect()
        self.x, self.y = game_map.get_player()
        self.x *= B_SIZE
        self.y *= B_SIZE
        self.rect.center = WIDTH//2, HEIGHT//2
        self.items = 0
        self.coins = 0
        self.speed = 0.1 * B_SIZE
        self.orient = Player.DOWN
        self.count = 0
        self.count_ticker = Player.TICKER
        self.sounds[Player.WALK].set_volume(0.1)

    def update(self):
        keystate = pygame.key.get_pressed()
        # Verify if switch image
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_LEFT] or keystate[pygame.K_UP] or keystate[pygame.K_DOWN]:
            self.count_ticker -= 1
            if self.count_ticker == 0:
                self.sounds[Player.WALK].play()
                self.count_ticker = Player.TICKER
                self.count = (self.count + 1) % 2
        self.image = self.images[self.orient][self.count]
        if keystate[pygame.K_RIGHT]:
            self.x += self.speed
            self.orient = Player.RIGHT
        if keystate[pygame.K_LEFT]:
            self.x -= self.speed
            self.orient = Player.LEFT
        if keystate[pygame.K_UP]:
            self.y -= self.speed
            self.orient = Player.UP
        if keystate[pygame.K_DOWN]:
            self.y += self.speed
            self.orient = Player.DOWN

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
    # Update
    all_sprites.update()
    # Draw / Render
    screen.fill(BLACK)
    game_map.draw(screen, cam_x=-WIDTH//2+player.x+player.hitbox.get_width() //
                  2, cam_y=-HEIGHT//2+player.y+player.hitbox.get_height()//2)
    all_sprites.draw(screen)
    # Draw stats

    # *after* drawing everything
    pygame.display.flip()

pygame.quit()
