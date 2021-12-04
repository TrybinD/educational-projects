import pygame
from settings import *
from map import world_map

# def ray_casting(sc, player_pos, player_angle):
#     cur_angle = player_angle - Half_FOV
#     x0, y0 = player_pos
#     for ray in range(Num_ray):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         for depth in range(1, Max_Depth):
#             x = x0 + depth * cos_a
#             y = y0 + depth * sin_a
#             # pygame.draw.line(sc, pygame.color.Color('white'), player_pos, (x,y),2)
#             if (x // Tile * Tile , y // Tile * Tile) in world_map:
#                 depth *= math.cos(player_angle - cur_angle)
#                 proj_height = Proj_Coeff / depth
#                 c = 225 / (1 + depth * depth * 0.00002)
#                 color = (c,c,c)
#                 pygame.draw.rect(sc, color ,(ray * Scale, Half_height - proj_height // 2, Scale, proj_height))
#                 break
#         cur_angle += Delta_angle

# Находим левый верхний у квадрата, в котором мы
def mapping(a, b):
    return (a // Tile) * Tile, (b // Tile) * Tile

def ray_casting(sc, player_pos, player_angle, texture):
    x0, y0 = player_pos
    xm, ym = mapping(x0, y0)
    cur_angle = player_angle - Half_FOV
    for ray in range(Num_ray):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        cur_angle += Delta_angle

        # Пересечение с вертикалями
        x, dx = (xm + Tile, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, Width, Tile):
            depth_v = (x - x0) / cos_a
            yv = y0 + (depth_v * sin_a)
            if mapping(x + dx, yv) in world_map:
                break
            x += dx * Tile
        # Пересечение с горизонталями
        y, dy = (ym + Tile, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, Height, Tile):
            depth_h = (y - y0) / sin_a
            xh = x0 + depth_h * cos_a
            if mapping(xh, y + dy) in world_map:
                break
            y += dy * Tile


        depth, offset = (depth_v, yv) if depth_v < depth_h else (depth_h, xh)
        offset = int(offset) % Tile
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.0000001)
        proj_height = min(int(Proj_Coeff / depth), 2 * Height)
        c = 225 / (1 + depth * depth * 0.0003)
        color = (c,c,c)
        pygame.draw.rect(sc, color, (ray * Scale, Half_height - proj_height // 2, Scale, proj_height))

        # wall_column = texture.subsurface(offset * Texture_scale, 0, Texture_scale, Texture_height)
        # wall_column = pygame.transform.scale(wall_column, (Scale, proj_height))
        # sc.blit(wall_column, (ray * Scale, Half_height - proj_height // 2))