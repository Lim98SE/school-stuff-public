import pygame

screen_size = [800, 800]

bg_color = "#000000"
fg_color = "#FFFFFF"
dot_color = "#808080"

class Hitbox:
    def __init__(self, position, size):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.rect = pygame.Rect(self.position, self.size)
    
    def collide(self, other):
        x_collision = (self.position.x >= other.position.x) and (self.position.x + self.size.x <= other.position.x + other.size.x)
        y_collision = (self.position.y >= other.position.y) and (self.position.y + self.size.y <= other.position.y + other.size.y)

        return x_collision and y_collision
    
    def update_rect(self):
        self.rect.update(self.position, self.size)

class Entity:
    def __init__(self, position, size, color):
        self.hitbox = Hitbox(position, size)
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.hitbox.rect)
    
    def update(self):
        self.hitbox.position += self.velocity
        self.hitbox.update_rect()

def get_axis(negative, positive):
    

window = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

running = True

paddle = Entity((0, 0), (16, 128), fg_color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(bg_color)

    paddle.draw(window)

    pygame.display.update()

pygame.quit()