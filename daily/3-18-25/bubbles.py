import pygame
import math
import random

window = pygame.display.set_mode((800, 600))

ticks = 0

gravity = pygame.Vector2(0, 1)

class Particle:
    def __init__(self, position, velocity, color, size):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = pygame.Color(color)
        self.size = float(size)
    
    def tick(self):
        self.position += self.velocity
        self.velocity += gravity
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.position, self.size)

class Snowflake(Particle):
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.color = pygame.Color("#FFFFFF")
        self.size = float(4)
        self.ticks = 0
        self.sway_intensity = 1
        self.sway_freq = 8
    
    def tick(self):
        self.position.x += math.sin(self.ticks / self.sway_freq) * self.sway_intensity
        self.position.y += 1
        self.ticks += 1

class Bubble(Particle):
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.color = pygame.Color("#6666FF")
        self.size = float(16)
    
    def tick(self):
        self.position.y -= 0.25

        if random.randint(0, 1000) == 0:
            temps.remove(self)
    
    def draw(self):
        pygame.draw.circle(window, self.color.lerp("#00000000", 0.1), self.position, self.size)
        pygame.draw.circle(window, self.color, self.position, self.size, 2)

particles = []

for i in range(300):
    x = random.randint(0, 800)
    y = random.randint(0, 200)
    particles.append(Bubble((x, 600 - y)))>
    # particles[-1].ticks += random.randint(-1000, 1000)
    # particles[-1].sway_freq += random.randint(-2, 2)
    # particles[-1].sway_intensity += random.randint(-5, 20) / 10

for i in range(300):
    x = random.randint(0, 800)
    y = random.randint(0, 200)
    particles.append(Snowflake((x, y)))
    particles[-1].ticks += random.randint(-1000, 1000)
    particles[-1].sway_freq += random.randint(-2, 2)
    particles[-1].sway_intensity += random.randint(-5, 20) / 10

running = True
bg_color = "#000000"

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    window.fill(bg_color)

    temps = particles.copy()

    for i in particles:
        i.tick()
        i.draw()
    
    particles = temps.copy()
    
    pygame.display.update()

    clock.tick(60)

    ticks += 1

pygame.quit()