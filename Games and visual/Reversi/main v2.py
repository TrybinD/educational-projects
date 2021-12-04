from ursina import *
from time import sleep, time

class Reversi():
    ''' Основной класс игры. Сохраняет текущее значение поля и имеет методы работы с ним'''
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]# Само поле
        self.board[3][3] = "B"
        self.board[4][4] = "B"
        self.board[3][4] = "W"
        self.board[4][3] = "W"
        self.score = (0, 0)
        self.curr_tile = "B"
        self.tiles_to_flip = []
        self.tile_to_append = None
        self.timer_1 = 0
        self.timer_0 = 0
        self.is_ended = False



    @staticmethod
    def is_on_board(x, y):
        '''Проверяет находится ли текущая метка на поле'''
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        else:
            return False


    @staticmethod # Используем статичный метод просто чтобы была возможность пользоваться им для ИИ
    def is_valid_move(board, tile, x_start, y_start):
        '''Проверяет допустимость хода.
         Если ход допустимый - возвращает перевернутые фишки'''

        if board[y_start][x_start] != ' ':
            return False

        if tile == 'B':
            other_tile = 'W'
        else:
            other_tile = 'B'

        tile_to_flip = []

        for x_dir, y_dir in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
            x, y = x_start, y_start
            x += x_dir
            y += y_dir

            while Reversi.is_on_board(x, y) and board[y][x] == other_tile:
                x += x_dir
                y += y_dir

            if Reversi.is_on_board(x, y) and board[y][x] == tile:
                while True:
                    x -= x_dir
                    y -= y_dir
                    if x == x_start and y == y_start:
                        break
                    tile_to_flip.append((x, y))
        if not tile_to_flip:
            return False

        return tile_to_flip

    def update_score(self):
        b, w = 0, 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == "B":
                    b += 1
                if self.board[x][y] == "W":
                    w += 1
        self.score = (b, w)

    def make_move(self, x_start, y_start):
        tiles_to_flip = Reversi.is_valid_move(self.board, self.curr_tile, x_start, y_start)

        if tiles_to_flip:
            self.board[y_start][x_start] = self.curr_tile
            for x, y in tiles_to_flip:
                self.board[y][x] = self.curr_tile
            if self.curr_tile == "B":
                self.curr_tile = "W"
            else:
                self.curr_tile = "B"


        self.tiles_to_flip = tiles_to_flip if tiles_to_flip else []
        self.tile_to_append = (x_start, y_start)

    def restart(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]  # Само поле
        self.board[3][3] = "B"
        self.board[4][4] = "B"
        self.board[3][4] = "W"
        self.board[4][3] = "W"
        self.score = (0, 0)
        self.curr_tile = "B"
        self.tiles_to_flip = []
        self.tile_to_append = None
        self.timer_1 = 0
        self.timer_0 = 0
        self.is_ended = False

    def randomAI_make_step(self):
        copy_board = copy(self.board)
        available_steps = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(copy_board, self.curr_tile, x, y):
                    available_steps.append((x, y))


        if available_steps:
            final_x, final_y = random.choice(available_steps)

            tiles_to_flip = Reversi.is_valid_move(self.board, self.curr_tile, final_x, final_y)

            if tiles_to_flip:
                self.board[final_y][final_x] = self.curr_tile
                for x, y in tiles_to_flip:
                    self.board[y][x] = self.curr_tile
                if self.curr_tile == "B":
                    self.curr_tile = "W"
                else:
                    self.curr_tile = "B"

            self.tiles_to_flip = tiles_to_flip if tiles_to_flip else []
            self.tile_to_append = (final_x, final_y)



    def smartAI_make_step(self):
        def on_corner(x, y):
            if (x == 0 and y == 0) or (x == 0 and y == 7) or \
                    (x == 7 and  y == 0) or (x == 7 and y == 7):
                return True
            return False


        copy_board = copy(self.board)
        available_steps = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(copy_board, self.curr_tile, x, y):
                    available_steps += [((x, y, 1000))] if on_corner(x,y) else [(x, y, len(self.is_valid_move(copy_board, self.curr_tile, x, y)))]



        if available_steps:
            final_x, final_y, _ = sorted(available_steps, key=lambda l: l[2])[-1]

            tiles_to_flip = Reversi.is_valid_move(self.board, self.curr_tile, final_x, final_y)

            if tiles_to_flip:
                self.board[final_y][final_x] = self.curr_tile
                for x, y in tiles_to_flip:
                    self.board[y][x] = self.curr_tile
                if self.curr_tile == "B":
                    self.curr_tile = "W"
                else:
                    self.curr_tile = "B"

            self.tiles_to_flip = tiles_to_flip if tiles_to_flip else []
            self.tile_to_append = (final_x, final_y)

    def is_ended_func(self):
        copy_board = copy(self.board)
        available_steps = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(copy_board, self.curr_tile, x, y):
                    available_steps.append((x, y))

        if not available_steps:
            self.is_ended = True


# class Tile(Entity):
#     def __init__(self, x, y, color=color.black):
#         super().__init__()
#         model = Cylinder(height=0.2, direction=(0, 0, 1))
#         position = (x, y, -0.25)
#         color = color


# class RestartButton(Button):
#     def __init__(self):
#         super().__init__(
#             model = 'quad',
#             text = "Рестарт",
#             color = color.dark_gray,
#         )



def create_map():
    for x in range(8):
        for y in range(8):
            Button(parent=scene, model='quad', scale=1, position=(x, y, 0), color=color.gray,
                   on_click=Func(reversi.make_move, x, y), eternal=True)

    Entity(model=Grid(8,8, thickness=3), scale=8, position=(3.5,3.5,-0.01), color=color.black,
           eternal=True)


def update_board():
    for x, y in reversi.tiles_to_flip:
        destroy(board_with_tiles[y][x])
        if reversi.board[y][x] == "W":
            board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25))
        if reversi.board[y][x] == "B":
            board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25),
                                            color=color.black)
    x, y = reversi.tile_to_append
    if reversi.board[y][x] == "W":
        board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25))
    if reversi.board[y][x] == "B":
        board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25),
                                        color=color.black)

def input(key):
    if key == 'left mouse up':
        if reversi.tiles_to_flip:
            update_board()
            reversi.timer_0 = time()
        else:
            t = Text('Недопустимый ход', origin = (mouse.position[0]*-5, mouse.position[1]*-40),
                 color = color.red)
            destroy(t, delay=1)


def update():
    stop_game = False
    if reversi.is_ended:
        reversi.update_score()
        print(reversi.score)
        reversi.is_ended = False
        Text('Конец Игры', origin=(4, -3), background = color.dark_gray, size = 1000,
             color = color.red)
        Text(f'Счет: Б - {reversi.score[1]}, Ч - {reversi.score[0]}', origin=(3, -1), background=color.dark_gray, size=1000,
             color=color.red)
        # RestartButton()
    reversi.timer_1 = time()
    if (reversi.timer_1 - reversi.timer_0 > 1 and reversi.timer_0 != 0):
        reversi.smartAI_make_step()
        update_board()
        reversi.timer_0 = 0
        reversi.is_ended_func()




if __name__ == '__main__':
    game = Ursina()
    reversi = Reversi()
    window.color = color.blue
    create_map()
    camera.position = (3.5, -9.5, -15)
    camera.rotation_x = -40
    board_with_tiles = [[None for _ in range(8)] for _ in range(8)]
    for x in range(8):
        for y in range(8):
            if reversi.board[y][x] == "W":
                board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25))
            if reversi.board[y][x] == "B":
                board_with_tiles[y][x] = Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25),
                                    color=color.black)

    game.run()













