import pygame

pygame.init()
window = pygame.display.set_mode((960, 540))

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
    
    window.fill("#FFFFFF")

    pygame.display.update()

    clock.tick(60)

pygame.quit()



