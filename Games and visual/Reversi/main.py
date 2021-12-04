from ursina import *
from time import time

class Reversi():
    ''' Основной класс игры. Сохраняет текущее значение поля и имеет методы работы с ним'''
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]# Само поле
        self.board[3][3] = "B"
        self.board[4][4] = "B"
        self.board[3][4] = "W"
        self.board[4][3] = "W"
        # (Возможно стоит доделать до начального положения)
        self.score = (0, 0)
        self.curr_tile = "B"



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

    def make_move(self, x, y):
        tiles_to_flip = Reversi.is_valid_move(self.board, self.curr_tile, x, y)

        if tiles_to_flip:
            self.board[y][x] = self.curr_tile
            for x, y in tiles_to_flip:
                self.board[y][x] = self.curr_tile
            if self.curr_tile == "B":
                self.curr_tile = "W"
            else:
                self.curr_tile = "B"

        return True if tiles_to_flip else False



class ReversiGame(Ursina):
    def __init__(self):
        super().__init__()
        self.reversi = Reversi()
        self.board = self.reversi.board
        self.new_game()
        window.color = color.blue
        camera.position = (3.5, -9.5, -15)
        camera.rotation_x = -40




    def create_map(self):
        for x in range(8):
            for y in range(8):
                Button(parent=scene, model='quad', scale=1, position=(x, y, 0), color=color.gray,
                       on_click=Func(self.reversi.make_move, x, y), eternal=True)

        Entity(model=Grid(8,8, thickness=3), scale=8, position=(3.5,3.5,-0.01), color=color.black,
               eternal=True)

    def new_game(self):
        self.create_map()


    def update(self):
        pass


def input(key):
    if key == 'left mouse up':
        for i in tiles:
            destroy(i)
        for x in range(8):
            for y in range(8):
                if game.board[y][x] == "W":
                    tiles.append(Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25)))
                if game.board[y][x] == "B":
                    tiles.append(Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25),
                                        color=color.black))

if __name__ == '__main__':
    game = ReversiGame()
    update = game.update
    tiles = []
    for x in range(8):
        for y in range(8):
            if game.board[y][x] == "W":
                tiles.append(Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25)))
            if game.board[y][x] == "B":
                tiles.append(Entity(model=Cylinder(height=0.2, direction=(0, 0, 1)), position=(x, y, -0.25),
                       color=color.black))
    game.run()















