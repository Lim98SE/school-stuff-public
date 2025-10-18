import pygame
import random

w_width = 40
w_height = 30

map = pygame.Surface((w_width, w_height))

position = pygame.Vector2(w_width // 2, w_height // 2)
window = pygame.display.set_mode((800, 600), pygame.NOFRAME)

ticks_until_change = random.randint(1, 5)

directions = [
    pygame.Vector2(0, 1),
    pygame.Vector2(0, -1),
    pygame.Vector2(1, 0),
    pygame.Vector2(-1, 0),
    # pygame.Vector2(1, 1),
    # pygame.Vector2(1, -1),
    # pygame.Vector2(-1, -1),
    # pygame.Vector2(-1, 1)
]

direction = directions[0]

ticks_in_this_direction = 0
prev_direction = direction

mn = 10
mx = 60

def step():
    global position
    map.set_at((int(position.x), int(position.y)), color)
    position += direction
    
    if position.x < 0: position.x += w_width
    if position.x > w_width: position.x -= w_width

    if position.y < 0: position.y += w_height
    if position.y > w_height: position.y -= w_height

running = True

def generate(steps):
    global ticks_until_change
    global direction

    global mn
    global mx

    mn = 3
    mx = 3

    map.fill("black")
    for i in range(steps):
        step()
        ticks_until_change -= 1

        if ticks_until_change == 0:
            ticks_until_change = random.randint(mn, mx)
            direction = random.choice(directions)

auto_change = 1000
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                color = pygame.Color.from_hsva(random.randint(0, 360), 100, 100)
                position = pygame.Vector2(w_width // 2, w_height // 2)
                generate(random.randint(25, 500))
                auto_change = 1000

    window.blit(pygame.transform.scale(map, window.get_size()))
    pygame.display.flip()
    clock.tick(100)
    auto_change -= 10

    if (auto_change <= 0):
        color = pygame.Color.from_hsva(random.randint(0, 360), 100, 100)
        position = pygame.Vector2(w_width // 2, w_height // 2)
        generate(random.randint(25, 500))
        auto_change = 300

pygame.quit()