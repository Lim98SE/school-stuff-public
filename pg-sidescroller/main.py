import pygame

import entity
from input import *
from player import Player
from level import parse_level

pygame.init()

window = pygame.display.set_mode((960, 544))

pygame.mixer.music.load("music.mp3")

tileset = pygame.image.load("tileset.png")

camera_limit = pygame.Vector2(960, 540)

def load_level(level_name):
    global entities
    global player
    global camera_limit

    global camera
    global camera_target

    entities = []

    level = parse_level(level_name, tileset)

    entities += level[0]

    player = Player(level[1], (32, 64), pygame.image.load("player-temp.png"))
    entities.append(player)

    camera = pygame.Vector2(player.position)
    camera.x -= window.get_width() / 2
    camera.y -= window.get_height() / 2
    camera_target = camera

    load_level("level_0")

running = True

clock = pygame.time.Clock()

stick = 0
gravity = 0

#camera = pygame.Vector2(player.position)
#camera.x -= window.get_width() / 2
#camera.y -= window.get_height() / 2
#camera_target = camera

def vector2_clamp(inp, mn, mx):
    new_vector = inp
    new_vector.x = pygame.math.clamp(inp.x, mn.x, mx.x)
    new_vector.y = pygame.math.clamp(inp.y, mn.y, mx.y)
    
    return new_vector

print(Player)

pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for i in entities:
        i.update_scroll(camera)
    
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player.jump()
    
    if pygame.key.get_just_pressed()[pygame.K_r]:
        load_level("level_1")

    player.velocity.x *= 0.8

    stick = get_axis(pygame.key.get_pressed()[pygame.K_LEFT], pygame.key.get_pressed()[pygame.K_RIGHT])
    player.velocity.x += stick * 2
    player.velocity.y += gravity

    player.update(entities)
    
    window.fll("#008080")

    for i in entities:
        i.draw(window)

    pygame.display.update()

    camera_target = player.position - pygame.Vector2(480, 270)
    camera_target.x = pygame.math.clamp(camera_target.x, 16, camera_limit.x - 480 + 96)
    camera_target.y = pygame.math.clamp(camera_target.y, 0, camera_limit.y - 270 + 80)
    camera = camera.lerp(camera_target, 2)

    clock.tick(60)

pygame.quit()