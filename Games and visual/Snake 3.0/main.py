import pygame
from items import *

pygame.init()
win = pygame.display.set_mode((496,496))
pygame.display.set_caption('Змейка')
score = score()
start = menu()
start.start(win,score.font_start)
while True:
    from items import *
    sn = snake()
    food = food()
    wall = walls()
    score = score()
    menu = menu()
    run = True
    while run:
        pygame.time.delay(120 - score.score*3)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    menu.start_run = True
                    menu.start(win,score.font_start)
                if ev.key == pygame.K_RIGHT and sn.step != [-11, 0]:
                    sn.step = [11, 0]
                elif ev.key == pygame.K_LEFT and sn.step != [11, 0]:
                    sn.step = [-11, 0]
                elif ev.key == pygame.K_UP and sn.step != [0, 11]:
                    sn.step = [0, -11]
                elif ev.key == pygame.K_DOWN and sn.step != [0, -11]:
                    sn.step = [0, 11]
        sn.print(win)
        sn.steps()
        if sn.head in sn.body[0:-2]:
            run = False

        food.print(win)
        if sn.head == food.pos:
            sn.body += [list(food.pos)]
            food.new()
            score.plus()

        wall.print(win)

        if sn.head[0] == 1 or sn.head[0] == 485 or sn.head[1] == 1 or sn.head[1] == 485:
            run = False

        render_score = score.font_score.render(f'Счет: {score.score}', 1, pygame.Color('orange'))
        win.blit(render_score, (5, 5))

        pygame.display.update()
        win.fill((0, 0, 0))
    pygame.time.delay(500)
    menu.end(win,score.font_end,score.score)

