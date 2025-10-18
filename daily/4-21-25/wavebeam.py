import math
import pygame

angle = 0

def calculate(a, b, c, d, x):
    x = x + 0.1
    y = a * math.sin(b * ( angle - c )) + d

    return [x, y]

pos = [0, 1]

def move():
    global pos
    x, y = calculate(200, 1, 0, pos[1], pos[0])
    pos[0] = x
    pos[1] = y

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    pygame.draw.circle()