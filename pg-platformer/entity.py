import pygame

class Entity:
    def __init__(self, position, hitbox: pygame.Rect):
        self.position = pygame.Vector2(position[0], position[1])
        self.hitbox = hitbox
        self.velocity = pygame.Vector2(0, 0)
    
    def draw(self, color, surface: pygame.Surface):
        pygame.draw.rect(surface, color, self.hitbox)
    
    def update(self):
        self.position += self.velocity
        self.hitbox.update(self.position, (self.hitbox.w, self.hitbox.h))
    
    def check_collision(self, other):
        # Check for vertical collision first

        if (self.position.x < other.position.x + other.hitbox.w and self.position.x + self.hitbox.w > other.position.x):
            if (self.position.y < other.position.y + other.hitbox.h and self.position.y + self.hitbox.h > other.position.y):
                return "W"
        
        if (self.position.y < other.position.y + other.hitbox.h and self.position.y + self.hitbox.h > other.position.y):
            if (self.position.x < other.position.x + other.hitbox.w and self.position.x + self.hitbox.w > other.position.x):
                return "F"
        
        return ""