import pygame
import os
import random
from Player import Player
from map import *

pygame.init()

# Window size
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("10x10 Tile Map")

# Tile settings
TILE_SIZE = 48
MAP_W, MAP_H = 10, 10

# Load all tiles from folder





main_tile_group = pygame.sprite.Group()
unbreakable_props_group = pygame.sprite.Group()
breakable_props_group = pygame.sprite.Group()

p1 = Player(5,6,screen, unbreakable_props_group, breakable_props_group)
my_player_group = pygame.sprite.Group()
my_player_group.add(p1)


map = Map(screen,4,6,main_tile_group,unbreakable_props_group,breakable_props_group)

all_sprites = YAwareGroup()
for prop in unbreakable_props_group:
    all_sprites.add(prop)
for prop in breakable_props_group:
    all_sprites.add(prop)
all_sprites.add(p1)



clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    

    map.update()
    #Draw tiles
    main_tile_group.draw(screen)     # ΤΑ tiles ΠΑΝΤΑ πρώτα
    all_sprites.update()             # update όλων
    all_sprites.draw(screen)         # depth sorting όλων
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
