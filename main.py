import pygame #type: ignore
import random
import heapq
import time


def a_star(start, goal, snake_body):
    def _bounds(position):
        return 0<= position[0] < 720 and 0<= position[1] < 720
    # board = []
    # for x in range(0, 720, 10):
    #     for y in range(0, 720, 10):
    #         board.append([x, y])

    dirs = [[10, 0], [0, 10], [-10, 0], [0, -10]]

    def neighbours(node):
        results = []
        for d in dirs:
            neighbour = [node[0] + d[0], node[1] + d[1]]
            if _bounds(neighbour) and neighbour not in snake_body:
                results.append(neighbour)
        return results
    
    def h(target, n):
        return abs(target[0] - n[0]) + abs(target[1] - n[1])
    

    open_set = []
    heapq.heappush(open_set, (0, tuple(start)))
    came_from = {}
    g = {tuple(start): 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        current = list(current)

        if current == goal:
            path = []
            while tuple(current) in came_from:
                path.append(current)
                current = came_from[tuple(current)]
            path.reverse()
            return path
        
        for neighbour in neighbours(current):
            g_curr = g[tuple(current)] + 10

            if tuple(neighbour) not in g or g_curr < g[tuple(neighbour)]:
                came_from[tuple(neighbour)] = current
                g[tuple(neighbour)] = g_curr
                f  = g_curr + h(neighbour, goal)
                heapq.heappush(open_set, (f, tuple(neighbour)))
    return None

pygame.init()
pygame.display.set_caption("Snake game")
game_window = pygame.display.set_mode((720, 720))

clock = pygame.time.Clock()

score = 0
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (720 / 2, 720 / 4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render("Score : " + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)
snake_position = [300, 250 ]

snake_body = [[100, 50], [90, 50]]

target_pos = [random.randrange(1, (720//10)) * 10, random.randrange(1, 720//10)* 10]     # why ? : one block width = 10

target_spawn = True



direction = 'UP'
change_to = direction 
path = []
AI_PLAY = True
is_on = True
while is_on:

    if AI_PLAY:
        if not path:
            path = a_star(snake_position, target_pos, snake_body)

        if path:
            next_cell = path.pop(0)

            if next_cell[0] > snake_position[0]:
                change_to = 'RIGHT'
            elif next_cell[0] < snake_position[0]:
                change_to = 'LEFT'
            elif next_cell[1] > snake_position[1]:
                change_to = 'DOWN'
            elif next_cell[1] < snake_position[1]:
                change_to = 'UP'
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                change_to = 'UP'
            if event.key == pygame.K_s:
                change_to = 'DOWN'
            if event.key == pygame.K_a:
                change_to = 'LEFT'
            if event.key == pygame.K_d:
                change_to = 'RIGHT'
        if event.type == pygame.QUIT:
            is_on = False

    if change_to=='RIGHT' and direction != 'LEFT':
        direction='RIGHT'
    if change_to=='LEFT' and direction != 'RIGHT':
        direction='LEFT'
    if change_to=='UP' and direction != 'DOWN':
        direction='UP'
    if change_to=='DOWN' and direction != 'UP':
        direction='DOWN'

    if direction == 'UP': snake_position[1] -= 10
    if direction=='DOWN': snake_position[1] += 10
    if direction=='RIGHT': snake_position[0] += 10
    if direction=='LEFT': snake_position[0] -= 10
    game_window.fill('black')
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == target_pos[0] and snake_position[1] == target_pos[1]:
        score += 10
        target_spawn =False
    else: 
        snake_body.pop()

    if not target_spawn:
        target_pos = [random.randrange(1, (720//10)) * 10, random.randrange(1, 720//10)* 10] 
        if target_pos in snake_body:
            target_pos = [random.randrange(1, (720//10)) * 10, random.randrange(1, 720//10)* 10] 
        path = []
        target_spawn = True
    
    target_spawn = True
    
    

    for position in snake_body:
        pygame.draw.rect(game_window, pygame.Color(0, 255, 0), pygame.Rect(position[0], position[1], 10, 10))
    
    pygame.draw.rect(game_window, (255, 0, 0), pygame.Rect(target_pos[0], target_pos[1], 10, 10))


    if snake_position[0] < 0 or snake_position[0] > 720 -10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > 720 - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    

    show_score(1, (255, 255, 255), "times new roman", 20)
    pygame.display.update()
    clock.tick(60)

