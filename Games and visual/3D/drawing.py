import pygame
from settings import *
from ray_casting import ray_casting
from map import world_minimap


class Drawing:
    def __init__(self, sc, map_sc):
        self.sc = sc
        self.map_sc = map_sc
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.texture = pygame.image.load('img/1.jpg').convert()

    def background(self):
        pygame.draw.rect(self.sc, pygame.color.Color('black'), (0, 0, Width, Half_height))
        pygame.draw.rect(self.sc, pygame.color.Color('black'), (0, Half_height, Width, Height))

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle, self.texture)

    def FPS(self, Clock):
        display_FPS = str(int(Clock.get_fps()))
        render = self.font.render(display_FPS, 0, pygame.color.Color('red'))
        self.sc.blit(render, FPS_pos)

    def mini_map(self, player):
        self.map_sc.fill(pygame.color.Color('black'))
        map_x, map_y = player.x // Minimap_scale, player.y // Minimap_scale
        for x,y in world_minimap:
            pygame.draw.rect(self.map_sc, pygame.color.Color('dark gray'),(x,y,Minimap_tile,Minimap_tile))
        pygame.draw.circle(self.map_sc,pygame.color.Color('green'), (map_x, map_y), 4)
        pygame.draw.line(self.map_sc,pygame.color.Color('green'), (map_x, map_y), ((round(map_x + 10*math.cos(player.angle))),
                                                                    round(map_y+ 10*math.sin(player.angle))))
        self.sc.blit(self.map_sc, Minimap_pos)