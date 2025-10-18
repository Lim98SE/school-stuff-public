import pygame
from entity import Entity
from level_loader import parse_level
from textures import textures
pygame.init()

window = pygame.display.set_mode((960, 540))
canvas = pygame.Surface((640, 360))

def send_frame():
    window.blit(pygame.transform.scale(canvas, window.get_size()), (0, 0))
    pygame.display.update()

clock = pygame.time.Clock()

player = Entity(pygame.Vector2(0, 0), pygame.Rect((0, 0), (16, 32)))

level = parse_level("level1")

running = True

def get_axis(negative, positive):
    return pygame.key.get_pressed()[positive] - pygame.key.get_pressed()[negative]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.velocity.y = -10

    player.velocity.y = -get_axis(pygame.K_DOWN, pygame.K_UP) * 10
    player.velocity.x *= 0.8
    player.velocity.x += get_axis(pygame.K_LEFT, pygame.K_RIGHT)
    player.update()

    for tile in level:
        cstate = player.check_collision(tile)

        if "W" in cstate:
            player.velocity.x = 0
            player.position.x = tile.position.x - player.hitbox.w
        
        elif "F" in cstate:
            if player.velocity.y > 0:
                player.velocity.y = 0
                player.position.x = tile.position.y - player.hitbox.h
    
    # ONLY draw after here!

    canvas.fill("#326da8")

    player.draw((0, 0, 0), canvas)

    for tile in level:
        tile.render(canvas)

    send_frame()

    clock.tick(60)