import pygame
pygame.init()
window = pygame.display.set_mode((800, 600))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    window.fill((0, 0, 0))
    
    index = 0

    for x in range(20):
        index += 1
        for y in range(20):
            index += 1
            r = pygame.Rect((x * 32, y * 32), (32, 32))
            colors = [
                (200, 0, 0),
                (200, 200, 0),
                (0, 0, 200),
                (0, 200, 200),
            ]

            if (index % 2 == 0):
                pygame.draw.rect(window, colors[index % 4], r)
                pygame.draw.rect(window, colors[(index + 1) % 4], r, 4)

    pygame.display.update()