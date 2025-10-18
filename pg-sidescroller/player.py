import pygame

from entity import Entity

class Player(Entity):
    def __init__(self, position, size, sprite):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.sprite = sprite
        self.velocity = pygame.Vector2(0, 0)

        self.rect = pygame.Rect(self.position, self.size)

        self.onfloor = False
        self.camera = pygame.Vector2(0, 0)

        self.can_jump = False

        self.type = "ENTITY_PLAYER"

    def update(self, others):
        self.rect.move_ip(self.velocity.x, 0)
        self.position.x += self.velocity.x

        if self.collide(others):
            self.rect.move_ip(-self.velocity.x, 0)
            self.position.x -= self.velocity.x
            self.velocity.x = 0
        
        self.rect.move_ip(0, self.velocity.y)
        self.position.y += self.velocity.y

        c_result = self.collide(others)

        if c_result != False:
            self.rect.move_ip(0, -self.velocity.y)
            self.position.y -= self.velocity.y
            self.velocity.y = 0
            if self.rect.bottom <= c_result.rect.top:
                self.onfloor = True
                self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.velocity.y = -20
            self.can_jump = False