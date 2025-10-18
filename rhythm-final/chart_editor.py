import pygame
import pygame_gui

window = pygame.display.set_mode((1280, 720))

running = True
clock = pygame.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
    
    window.fill("#222222")

    pygame.display.update()
    clock.tick(60)