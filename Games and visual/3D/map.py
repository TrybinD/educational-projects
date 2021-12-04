from settings import *
import pygame
from Lab import text_map

# text_map =  [
#     'WWWWWWWWWWWWWWWWWWWW',
#     'W..................W',
#     'W...WW......WWW....W',
#     'W..................W',
#     'W.......WW.........W',
#     'W.......W....WWW...W',
#     'W.WW...............W',
#     'W.......WWWW.......W',
#     'W..................W',
#     'W......WWWWWWWWW...W',
#     'W..WW..............W',
#     'WWWWWWWWWWWWWWWWWWWW',
# ]

world_map = set()
world_minimap = set()
walls_collisions = []
for j,row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == '#':
            world_map.add((i*Tile, j*Tile))
            world_minimap.add((i * Minimap_tile, j * Minimap_tile))
            walls_collisions.append(pygame.Rect(i * Tile, j * Tile, Tile, Tile))

map_size = (len(text_map[0]) * Minimap_tile, len(text_map) * Minimap_tile)