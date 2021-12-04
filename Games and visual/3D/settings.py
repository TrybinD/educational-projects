import pygame
import math

# display set
Width = 1000
Height = 600
Half_width = Width // 2
Half_height = Height // 2
FPS = 60
Tile = 50
FPS_pos = (Width - 50, 5)

#minimap settings
Minimap_scale = 5
Minimap_tile = Tile // Minimap_scale
Minimap_pos = (0, 0) #Height - Height // Minimap_scale
map_settings = (31, 21)

#texture settings (1000 x 1000)
Texture_wight = 1000
Texture_height = 1000
Texture_scale = Texture_wight // Tile

# ray casting set
FOV = math.pi / 3
Half_FOV = FOV / 2
Num_ray = 250
Max_Depth = 300
Delta_angle = FOV / Num_ray
Dist = Num_ray / (2 * math.tan(Half_FOV))
Proj_Coeff = 3 * Dist * Tile
Scale = Width // Num_ray

# player set
player_pos = (70, 70) #(70, Height - 70)
player_angle = 0
player_speed = 2
