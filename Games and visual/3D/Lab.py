import random
from settings import *

size_x, size_y = map_settings


lab = [[1 for i in range(size_x)] for j in range(size_y)]
for i in range(size_y):
    lab[i].append(1)
    for j in range(size_x):
        if i % 2 == 1 and j % 2 == 1:
            lab[i][j] = 2
lab.append([1 for i in range(size_x+1)])
x, y = 1, 1
way =[]
while True:
    var = []
    for i in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        if lab[x+i[0]][y+i[1]] == 2:
            var += [(x+i[0], y+i[1])]
    if var == []:
        if way == []:
            break
        else:
            lab[x][y] = 0
            x, y = way.pop()
    else:
        lab[x][y] = 0
        way.append((x,y))
        nx, ny = random.sample(var, 1)[0]
        lab[(x+nx) // 2][(y+ny) // 2] = 0
        x, y = nx, ny

# for i in range(size_y):
#     for j in range(size_x):
#         print('#' if lab[i][j] == 1 else '_', end='')
#     print()

text_map = []
for i in range(size_y):
    text_map += ['#']
    for j in range(1, size_x):
        if lab[i][j] == 1:
            text_map[i] += '#'
        elif lab[i][j] == 0:
            text_map[i] += '_'
