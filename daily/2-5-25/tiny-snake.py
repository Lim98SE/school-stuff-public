import pygame
import random

snake = [pygame.Vector2(0, 0)] * 4
direction = pygame.Vector2(1, 0)
lookup = {
    pygame.K_DOWN: pygame.Vector2(0, 1),
    pygame.K_UP: pygame.Vector2(0, -1),
    pygame.K_LEFT: pygame.Vector2(-1, 0),
    pygame.K_RIGHT: pygame.Vector2(1, 0)
}

res = 10

apple_color = 0xFF << (8 * 2)
snake_color = pygame.Color("#00FF00")
apple_pos = (random.randint(0, res - 1), random.randint(0, res - 1))

surface = pygame.Surface((res, res))
window = pygame.display.set_mode((res * 50, res * 50))

score = 0
state = 0

def move_snake():
    global snake
    snake.append(snake[-1] + direction)
    try: surface.get_at(snake[-1]).r
    except: global state; state = 1; return
    if surface.get_at(snake[-1]).r == 0:
        snake.pop(0)
    else:
        global apple_pos
        global score
        score += 1
        apple_pos = (random.randint(0, res - 1), random.randint(0, res - 1))

clock = pygame.time.Clock()
changed = 0

while True:
    surface.fill(0)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if direction * -1 != lookup[event.key] and not changed:
                direction = lookup[event.key];changed = 1

    if state == 0:
        surface.set_at(apple_pos, apple_color)
        move_snake()
        try: surface.get_at(snake[-1])
        except: state = 1; continue
        x = 0
        for i in snake[:-1]: surface.set_at(i, snake_color.lerp("#000F00", x / len(snake))); x += 1
        if surface.get_at(snake[-1]).b != 0: state = 1
        surface.set_at(snake[-1], snake_color)
    
    else:
        print(score)
    
    window.blit(pygame.transform.scale(surface, window.get_size()))
    pygame.display.update()

    changed = 0
    
    clock.tick(9)
