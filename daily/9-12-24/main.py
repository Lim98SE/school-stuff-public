import pygame
import random
import math

sign = lambda x: math.copysign(1, x)

pygame.init()

img = pygame.image.load("donut.png")
img.set_colorkey("#FF00FF")

window = pygame.display.set_mode((800, 600))

max_x = window.get_size()[0] - img.get_size()[0]
max_y = window.get_size()[1] - img.get_size()[1]

target_x = 0
target_y = 0

x = 0
y = 0

running = True
moved_to = False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill("#000000")

    if abs(x - target_x) < 5 and abs(y - target_y) < 5:
        target_x = random.randint(0, max_x)
        target_y = random.randint(0, max_y)
    
    else:
        x += sign(target_x - x)
        y += sign(target_y - y)

    pygame.draw.line(window, "#FFFFFF", (x, y), (target_x, target_y), 4)

    window.blit(img, (x, y))

    pygame.display.flip()

    clock.tick(200)
        

pygame.quit()