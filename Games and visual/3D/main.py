import pygame
from settings import *
from player import Player
from drawing import Drawing
from map import map_size

pygame.init()
player = Player()
sc = pygame.display.set_mode((Width,Height))
map_sc = pygame.Surface(map_size)
Clock = pygame.time.Clock()
drawing = Drawing(sc, map_sc)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit()
    player.movement()
    drawing.background()
    drawing.world(player.pos, player.angle)
    drawing.FPS(Clock)
    drawing.mini_map(player)

    pygame.display.flip()
    Clock.tick(FPS)