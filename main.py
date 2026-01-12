import pygame #type: ignore
import random
import time

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

target_pos = [random.randrange(1, (720//10)) * 10, random.randrange(1, (720//10)* 10)]     # why ? : one block width = 10

target_spawn = True



direction = 'UP'
change_to = direction 

is_on = True
while is_on:
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
    pygame.draw.rect(game_window, pygame.Color(255, 255, 255), pygame.Rect(10, 10, 700, 700), 5)

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

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == target_pos[0] and snake_position[1] == target_pos[1]:
        score += 10
        target_spawn =False
    else: 
        snake_body.pop()

    if not target_spawn:
        target_pos = [random.randrange(1, (720//10)) * 10, random.randrange(1, (720//10)* 10)]
    
    target_spawn = True
    
    game_window.fill('black')

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
    clock.tick(15)

