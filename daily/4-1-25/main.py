import pygame
import random
import math

window = pygame.display.set_mode((800, 600))

running = True

pal = []
rainbow_seq = [5, 4, 6, 3, 2, 1]

sun_size = 60
sun_pos = (680, 120)
sl_length = 40
sl_distance = 80
sl_inital_distance = 80
sun_lines = 8
sl_angle_offset = 0

pal_img = pygame.image.load("colors.png")

for x in range(pal_img.get_width()):
    pal.append(pal_img.get_at((x, 0)))

print(pal)

background = pygame.Surface((1, 2))

background.set_at((0, 0), pal[0])
background.set_at((0, 1), pal[2])

grass = pygame.Surface((800, 4), pygame.SRCALPHA)

def clamp(mn, a, mx):
    if a > mx: return mx
    if a < mn: return mn
    return a

for y in range(grass.get_height()):
    for x in range(grass.get_width()):
        bottom = y == 0
        
        if not bottom:
            for p in range(-1, 2):
                # print(x + p, y - 1)
                if grass.get_at((clamp(0, x + p, 799), y - 1)) == pal[3]:
                    bottom = random.randint(0, 10) > ((3 - y) * 3)
        
        else:
            bottom = random.randint(0, 10) > ((3 - y) * 3)
        
        if bottom:
            grass.set_at((x, y), pal[3])

background = pygame.transform.smoothscale(background, window.get_size())

def rainbow(colors, center, inital, width):
    for i in range(len(colors)):
        pygame.draw.circle(window, pal[colors[i]], center, inital - (i * width), width + 1)

def flower(colors, origin, height):
    origin = pygame.Vector2(origin)
    top_origin = origin - pygame.Vector2(0, height)
    pygame.draw.line(window, pal[colors[0]], origin, top_origin, 4)

    angle = 0
    petals = 6

    for i in range(petals):
        angle += (360 / petals)

        petal_origin = top_origin + pygame.Vector2(2, 0) + pygame.Vector2(0, 20).rotate(angle)
        pygame.draw.circle(window, pal[colors[1]], petal_origin, 11)
    
    pygame.draw.circle(window, pal[colors[2]], top_origin + pygame.Vector2(2, 0), 15)

def bee(colors, origin):
    origin = pygame.Vector2(origin)
    size = pygame.Vector2(30, 10)

    pygame.draw.circle(window, pal[colors[2]], origin + pygame.Vector2(-10 + (size.x - 10), 0), 10)
    pygame.draw.circle(window, pal[colors[2]], origin + pygame.Vector2(10 + (size.x - 10), 0), 10)

    pygame.draw.rect(window, pal[colors[0]], pygame.Rect(origin, size))
    pygame.draw.circle(window, pal[colors[0]], (origin + pygame.Vector2(0, size.y // 2)), size.y // 2)
    pygame.draw.circle(window, pal[colors[0]], (origin + pygame.Vector2(size.x, size.y // 2)), size.y // 2)

    pygame.draw.line(window, pal[colors[1]], origin + pygame.Vector2(4, 0), origin + pygame.Vector2(4, size.y), 2)
    pygame.draw.line(window, pal[colors[1]], origin + pygame.Vector2(size.x - 4, 0), origin + pygame.Vector2(size.x - 4, size.y), 2)

bee_colors = [6, 0, 7]

class Bee:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.speed = random.randint(1, 10)
        if random.randint(0, 3) == 0: self.speed *= -1
    
    def draw(self):
        bee(bee_colors, self.position)
    
    def update(self):
        self.position.x += self.speed

        if (self.position.x > 900) or (self.position.x < -100):
            self.__init__(pygame.Vector2(-899 if random.randint(0, 1) == 0 else 899, random.randint(0, 500)))

clock = pygame.time.Clock()
ticks = 0

bees = [
]

for i in range(100):
    bees.append(
        Bee((random.randint(0, 800), random.randint(0, 500)))
    )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
    
    window.fill("#FFFFFF")

    window.blit(background)

    rainbow(rainbow_seq, (400, 400), 200, 10)

    pygame.draw.rect(window, pal[3], (0, 400, 800, 600))
    window.blit(grass, (0, 400 - grass.get_height()))

    pygame.draw.circle(window, pal[6], sun_pos, sun_size)
    pygame.draw.circle(window, pal[4], sun_pos, sun_size // 1.5)

    sl_angle = 0

    for i in bees:
        i.draw()
        i.update()

    for i in range(sun_lines):
        sl_angle += 360 / sun_lines

        offset = pygame.Vector2(0, sl_length).rotate(sl_angle + sl_angle_offset)
        distance = pygame.Vector2(0, sl_distance).rotate(sl_angle + sl_angle_offset)

        pygame.draw.line(window, pal[6], pygame.Vector2(sun_pos) + distance, pygame.Vector2(sun_pos) + distance + offset, 4)

    flower([3, 1, 6], (60, 400), 50)

    pygame.display.update()

    sl_angle_offset += 0.25
    sl_distance = sl_inital_distance + (math.sin(ticks / 20) * 16)

    clock.tick(60)
    ticks += 1

pygame.quit()