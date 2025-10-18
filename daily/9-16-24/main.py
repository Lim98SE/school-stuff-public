import pygame
import random

flower_spacing = -1

flower_positions = []

with open("lookup.txt") as file:
    data = file.read()

for i in data.replace("\r", "").split("\n"):
    flower_positions.append(i.split("|"))

class Flower:
    def __init__(self, position: pygame.Vector2, size, color):
        self.position = position
        self.size = size
        self.max_size = 128
        self.min_size = 32
        self.speed = 1
        self.direction = 1
        self.color = color
        self.radius = 32
    
    def render(self, surface: pygame.Surface):
        root = self.position
        center = root.y - self.size - (self.radius / 2) # 64 is the size of the center, so 64 / 2 = 32

        # stem
        pygame.draw.line(surface, "#FFFFFF", root + pygame.Vector2(flower_spacing, 0), (root.x + flower_spacing, center), 8)

        # petals
        petals = []

        for i in flower_positions:
            petals.append(
                pygame.Vector2(
                    pygame.Vector2(eval(i[0].replace("S", str(self.radius // 2))),
                                   eval(i[1].replace("S", str(self.radius // 2))))
                )
            )
        
        for i in petals:
            pygame.draw.circle(surface, self.color, i + self.position + pygame.Vector2(0, -self.size - (self.radius / 2)), self.radius)

        pygame.draw.circle(surface, "#404000", pygame.Vector2(root.x, center), self.radius)
        pygame.draw.circle(surface, "#FFFF00", pygame.Vector2(root.x, center), self.radius * 0.7)
    
    def animate(self):
        if (self.size >= self.max_size):
            self.direction *= -1
        
        elif (self.size <= self.min_size):
            self.direction *= -1
        
        self.size += self.direction * self.speed

window = pygame.display.set_mode((640, 360))

flowers = []
colors = [
    "#FF0000",
    "#00FF00",
    "#FFFF00",
    "#FF00FF"
]

for i in range(50):
    flower = Flower(pygame.Vector2(96, 256), 128, "#00FF00")
    flower.position.x = random.randint(64, 640 - 64)
    flower.position.y = random.randint(192, 360)
    flower.size = random.randint(flower.min_size, flower.max_size)
    flower.color = random.choice(colors)
    flower.speed = random.randint(1, 4)
    flowers.append(flower)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill("#0066FF")

    for flower in flowers:
        flower.animate()
        flower.render(window)

    pygame.display.update()

    clock.tick(60)

pygame.quit()