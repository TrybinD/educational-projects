import pygame
import random


class snake():
    def __init__(self):
        self.head = [100,100]
        self.body = [[67,100],[78,100],[89,100],[100,100]]
        self.step = [11,0]

    def print(self,win):
        for i in self.body:
            pygame.draw.rect(win, (255, 255, 255), pygame.Rect(i[0], i[1], 10, 10))

    def steps(self):
        self.head[0] += self.step[0]
        self.head[1] += self.step[1]
        self.body += [list(self.head)]
        self.body.pop(0)

class food():
    def __init__(self):
        self.pos = [random.randrange(12,474,11),random.randrange(12,474,11)]
    def new(self):
        self.pos = [random.randrange(12, 474, 11), random.randrange(12, 474, 11)]
    def print(self,win):
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.pos[0], self.pos[1], 10, 10))

class walls():
    def __init__(self):
        pass

    def print(self, win):
        for i in range(1, 489, 11):
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(1, i, 10, 10))
        for i in range(1, 489, 11):
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(485, i, 10, 10))
        for i in range(1, 489, 11):
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(i, 1, 10, 10))
        for i in range(1, 489, 11):
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(i, 485, 10, 10))
        pass

class score():
    def __init__(self):
        self.score = 0
        self.font_score = pygame.font.SysFont('Arial', 20, bold=True, )
        self.font_end = pygame.font.SysFont('Arial', 40, bold=True, )
        self.font_start = pygame.font.SysFont('Arial', 40, bold=True, )
    def plus(self):
        self.score += 1

class menu():
    def __init__(self):
        self.start_run = True
        self.end_run = True
        self.color_passive = 'blue'
        self.color_active = 'red'
        self.color = self.color_passive

    def start(self, win, font_start):
        buttons = [(140, 155),(140, 255)]
        while self.start_run:
            mp = pygame.mouse.get_pos()
            if mp[0] > 140 and mp[0] < 300 and mp[1] > 155 and mp[1] < 200:
                render_start = font_start.render('Играть', 1, pygame.Color(self.color_active))
                win.blit(render_start, buttons[0])
            else:
                render_start = font_start.render('Играть', 1, pygame.Color(self.color_passive))
                win.blit(render_start, buttons[0])
            if mp[0] > 140 and mp[0] < 300 and mp[1] > 255 and mp[1] < 300:
                render_start = font_start.render('Выйти', 1, pygame.Color(self.color_active))
                win.blit(render_start, buttons[1])
            else:
                render_start = font_start.render('Выйти', 1, pygame.Color(self.color_passive))
                win.blit(render_start, buttons[1])

            pygame.display.update()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and mp[0] > 140 and mp[0] < 300 and mp[1] > 155 and mp[1] < 200:
                    self.start_run = False
                if ev.type == pygame.MOUSEBUTTONDOWN and mp[0] > 140 and mp[0] < 300 and mp[1] > 255 and mp[1] < 300:
                    exit()

    def end(self, win, font_end, score):
        while self.end_run:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and self.color == self.color_active:
                    self.end_run = False

            render_end = font_end.render('Game over', 1, pygame.Color('orange'))
            win.blit(render_end, (140, 155))
            render_end = font_end.render(f'Ваш счет: {score}', 1, pygame.Color('orange'))
            win.blit(render_end, (140, 205))
            render_end = font_end.render('Начать заново', 1, pygame.Color(self.color))
            win.blit(render_end, (140, 255))

            mp = pygame.mouse.get_pos()
            if mp[0] > 140 and mp[0] < 440 and mp[1] > 255 and mp[1] < 300:
                self.color = self.color_active
            else:
                self.color = self.color_passive

            pygame.display.update()
