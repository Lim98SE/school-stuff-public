import pygame
import random

window = pygame.display.set_mode((540, 960))
surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)

running = True
clock = pygame.time.Clock()

class Brick:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.color = pygame.Color(random.choice(colors))
        self.dying = False
    
    def render(self):
        if self.dying:
            self.color = self.color.lerp("#00000000", 0.1)

        pygame.draw.rect(surface, self.color, pygame.Rect(self.position, pygame.Vector2(64 - (8), 16)))
        pygame.draw.rect(surface, "#000000", pygame.Rect(self.position, pygame.Vector2(64 - (8), 16)), 2)
    
    def collide(self):
        global b_buffer
        if self.dying: return False
        if self.color.r + self.color.g + self.color.b == 0: b_buffer.remove(self)
        return pygame.Rect(self.position, pygame.Vector2(64 - (8), 16)).collidepoint(ball_pos)

ball_pos = pygame.Vector2(540 // 2, 960 // 2)
ball_velocity = pygame.Vector2(0, 10)
paddle = pygame.Rect((0, 960 - 32), (128, 24))

background_sky = pygame.Surface(window.get_size())

bricks = []
colors = [
    "#FFFFFF",
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FF00FF",
    "#FFFF00",
    "#00FFFF"
]

for x in range(540//64):
    for y in range(14):
        bricks.append(
            Brick(((x * 64) + 16, (y * 24) + 64))
        )

trail = []
    
# generate sky

color_0 = "#FFFFFF"
color_1 = "#b5fbff"
color_2 = "#6b9fcf"
color_3 = "#384196"

background_sky.fill("#FF0000")

bg_rect = pygame.Surface((1, 2))
bg_rect.set_at((0, 0), color_0)
bg_rect.set_at((0, 1), color_1)
background_sky.blit(pygame.transform.smoothscale(bg_rect, (window.get_width(), 200)), (0, 0))

bg_rect = pygame.Surface((1, 2))
bg_rect.set_at((0, 0), color_1)
bg_rect.set_at((0, 1), color_2)
background_sky.blit(pygame.transform.smoothscale(bg_rect, (window.get_width(), 300)), (0, 200))

bg_rect = pygame.Surface((1, 3))
bg_rect.set_at((0, 0), color_2)
bg_rect.set_at((0, 1), color_3)
background_sky.blit(pygame.transform.smoothscale(bg_rect, (window.get_width(),(960 - 500))), (0, 500))

while running:
    trail.append(pygame.Vector2(ball_pos))
    # for i in trail: print(i.x, i.y, end=", ")
    # print()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False; continue # semicolons in python
    
    # begin game loop

    paddle.x = pygame.mouse.get_pos()[0] - 64

    ball_pos += ball_velocity

    if (ball_pos.y > window.get_height() or ball_pos.y < 0):
        ball_velocity.y *= -1
        ball_pos += ball_velocity
    
    if (ball_pos.x > window.get_width() or ball_pos.x < 0):
        ball_velocity.x *= -1
        ball_pos += ball_velocity

    b_buffer = bricks.copy()

    if paddle.collidepoint(ball_pos):
        ball_velocity.y = -abs(ball_velocity.y)
        ball_velocity.x = -((paddle.x + ((128) / 2)) - ball_pos.x) / 4
        ball_pos.y = paddle.y

    for i in bricks:
        if i.collide():
            ball_velocity.y *= -1
            ball_velocity.x = -((i.position.x + ((64 - 8) / 2)) - ball_pos.x) / 4
            i.dying = True
    
    bricks = b_buffer.copy()

    # finish game loop
    
    surface.fill("#000000")
    surface.blit(background_sky, (0, 0))

    for i in bricks: i.render()
    if len(trail) > 10: trail.pop(0)
    index = 0
    for i in trail: pygame.draw.circle(surface, "#FFFFFF20", i, index); index += 1
    pygame.draw.circle(surface, "#FFFFFF", ball_pos, 8)
    pygame.draw.circle(surface, "#000000", ball_pos, 8, 2)
    pygame.draw.rect(surface, "#FFFFFF", paddle)

    # draw velocity bc cool

    # pygame.draw.line(surface, "#FF0000", ball_pos, ball_pos + (ball_velocity * 4), 4)

    window.blit(surface)

    pygame.display.update()

    clock.tick(60)

pygame.quit()