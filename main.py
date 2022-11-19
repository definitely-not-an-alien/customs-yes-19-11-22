import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.font.init()
speed_bird = 0.5
jumping = 0
game_over = False
score_text = 0
size = width, height = 500, 440
bird_x = 10
bird_y = height / 2
screen_scrolling = 0
pipe_width = 90
pipe_height = 400
pipe_pos = width
pipe_interval = 200
pipe_gap = 200
pipes = []
for i in range(6):
    pipes.append(random.randint(pipe_gap, height - pipe_gap))

font = pygame.font.SysFont('monospace', 30)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Platformer')
bg_image = pygame.image.load("images/bg.png")
bg_image = pygame.transform.scale(bg_image, size)
bird = pygame.image.load("images/fb.png")
scale_ratio = (bird.get_height() / bird.get_width())
bird_width = 60
bird_height = 60 * scale_ratio
bird = pygame.transform.scale(bird, (bird_width, bird_height))
t_pipe = pygame.image.load("images/top_pipe.png")
t_pipe = pygame.transform.scale(t_pipe, (pipe_width, pipe_height))
b_pipe = pygame.image.load("images/bottom_pipe.png")
b_pipe = pygame.transform.scale(b_pipe, (pipe_width, pipe_height))
score = font.render(str(score_text), False, "white")


def is_colliding():
    return pipe_pos <= (bird_x + bird_width) and (pipe_pos + pipe_width) >= bird_x and (pipes[0] <= (bird_y + bird_height) or pipes[0] - pipe_gap >= bird_y)


while True:
    pygame.time.Clock().tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
#             if event.key == K_SPACE:
            jumping += 25

    for s in range(2):
        screen.blit(bg_image, (screen_scrolling + s * width, 0))
    screen_scrolling -= 2
    if (screen_scrolling < -width):
        screen_scrolling = 0
        
    for p in range(6):
        screen.blit(t_pipe, (pipe_pos + p * (pipe_width + pipe_interval), pipes[p] - pipe_gap - pipe_height))
        screen.blit(b_pipe, (pipe_pos + p * (pipe_width + pipe_interval), pipes[p]))

    pipe_pos -= 1

    if (is_colliding()):
        game_over = True

    if game_over:
        jumping = 100
        speed_bird = 6
        bird_y += speed_bird
        if (bird_y >= height - bird.get_height()):
            bird_y = height - bird.get_height()
            jumping = 0
        screen.blit(bird, (10, bird_y))
        font = pygame.font.SysFont('monospace', 60)
        font.set_bold(True)
        gg = font.render("GAME OVER", False, "white")
        screen.blit(gg, (width / 2 - font.size(str("GAME OVER"))[0] / 2, height / 2 - font.size(str("GAME OVER"))[1] / 2))
    else:
        if (jumping > 0):
            speed_bird = -5
            jumping -= 1
        else:
            speed_bird = 2
        bird_y += speed_bird
        if (bird_y >= height - bird.get_height()):
            bird_y = height - bird.get_height()
            jumping = 0
            game_over = True
            # break
        elif (bird_y <= 0):
            bird_y = bird_height
            jumping = 0
        screen.blit(bird, (10, bird_y))
        if (pipe_pos < -pipe_width):
            pipes.pop(0)
            pipes.append(random.randint(pipe_gap, height - pipe_gap))
            pipe_pos += (pipe_width + pipe_interval)
            score_text += 1
            score = font.render(str(score_text), False, "white")

    screen.blit(score, (width / 2 - font.size(str(score_text))[0] / 2, 20))
    pygame.display.flip()
