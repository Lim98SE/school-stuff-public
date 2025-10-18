import pygame
import math

window = pygame.display.set_mode((800, 800))
angle = 0

running = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False; continue
    
    if pygame.mouse.get_pressed()[0]:
        mpos = pygame.mouse.get_pos()
        angle = pygame.Vector2(400, 400).angle_to(mpos)
    
    window.fill("#000000")

    pygame.draw.line(window, (255, 0, 0), (400, 400), pygame.Vector2(400, 400).rotate_rad(angle))

    pygame.display.update()

    clock.tick(60)

pygame.quit()