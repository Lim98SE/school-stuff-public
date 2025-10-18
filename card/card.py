import pygame
import random

signs = [-1, 1]

paddle_1_window = pygame.Window("", (64, 300), (0, 0))
paddle_1_window.borderless = True
paddle_1_window.always_on_top = True

paddle_2_window = pygame.Window("", (64, 300), (0, 0))
paddle_2_window.borderless = True
paddle_2_window.always_on_top = True

ball_window = pygame.Window("", (64, 64))
ball_window.borderless = True
ball_window.always_on_top = True

score_window = pygame.Window("", (256, 64))
score_window.borderless = True
score_surface = score_window.get_surface()
score_window.always_on_top = True
score_window.position = [(1920 / 2) - (256 / 2), 1080 - 64]

paddle_1_window.get_surface().fill("#FFFFFF")
paddle_2_window.get_surface().fill("#FFFFFF")
ball_window.get_surface().fill("#FFFFFF")

paddle_1_window.flip()
paddle_2_window.flip()
ball_window.flip()

running = True

paddle_1_y = 16
paddle_2_y = 16

ball_velocity = pygame.Vector2(-5, 0)
ball_pos = pygame.Vector2(960, 540)

clock = pygame.time.Clock()

p1_score = 0
p2_score = 0

cooldown = 120

pygame.font.init()
font = pygame.font.SysFont("Arial", 48, True)

while True:
    pygame.event.get()

    score_surface.fill("#000000")
    sc_blit = font.render(str(p1_score), True, "#FF0000")
    score_surface.blit(sc_blit, (16, 8))

    sc_blit = font.render(str(p2_score), True, "#00FFFF")
    score_surface.blit(sc_blit, (256 - 16 - sc_blit.get_width(), 8))

    paddle_1_window.position = pygame.Vector2(16, paddle_1_y)
    paddle_2_window.position = pygame.Vector2(1920 - 64 - 16, paddle_2_y)

    score_window.flip()

    if cooldown < 0:
        ball_pos += ball_velocity
    
    ball_window.position = ball_pos

    if pygame.key.get_pressed()[pygame.K_w]:
        paddle_1_y -= 4
    
    if pygame.key.get_pressed()[pygame.K_s]:
        paddle_1_y += 4
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        paddle_2_y -= 4
    
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        paddle_2_y += 4

    if ball_pos.y < 0:
        ball_pos.y = 0
        ball_velocity.y *= -1
    
    if ball_pos.y > 1080 - 48:
        ball_pos.y = 1080 - 48
        ball_velocity.y *= -1
    
    if ball_pos.x < 64 and ball_pos.x > 32:
        if ball_pos.y > paddle_1_y and ball_pos.y < paddle_1_y + 300:
            ball_velocity.x *= -1
            ball_velocity.y = -((paddle_1_y - ((ball_pos.y + 32))) + 150) / 5
            ball_pos.x = 64
    
    if ball_pos.x > 1920 - 128 - 16 and ball_pos.x < 1920 - 128 + 16:
        if ball_pos.y > paddle_2_y and ball_pos.y < paddle_2_y + 300:
            ball_velocity.x *= -1
            ball_velocity.y = -((paddle_2_y - ((ball_pos.y + 32))) + 150) / 5
            ball_pos.x = 1920 - 128 - 16
    
    if ball_pos.x > 1920: # p1 wins
        p1_score += 1
        ball_pos = pygame.Vector2(960, 540)
        ball_velocity = pygame.Vector2(5 * random.choice(signs), 0)
        cooldown = 60
    
    if ball_pos.x < -64: # p2 wins
        p2_score += 1
        ball_pos = pygame.Vector2(960, 540)
        ball_velocity = pygame.Vector2(5 * random.choice(signs), 0)
        cooldown = 60
    
    cooldown -= 1
    
    clock.tick(60)