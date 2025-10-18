import pygame

class Entity:
    def __init__(self, position, size, sprite):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.sprite = sprite
        self.velocity = pygame.Vector2(0, 0)

        self.rect = pygame.Rect(self.position, self.size)

        self.onfloor = False
        self.camera = pygame.Vector2(0, 0)

        self.type = "ENTITY_GENERIC"
    
    def update_scroll(self, new_scroll):
        diff = self.camera - new_scroll
        self.rect.move_ip(diff)
        self.camera = new_scroll
    
    def draw(self, surface):
        surface.blit(self.sprite, self.rect.topleft)
    
    def draw_debug(self, surface):
        pygame.draw.rect(surface, "#FFFFFF", self.rect)
    
    def collide(self, others):
        for i in others:
            if i == self: continue
            if self.rect.colliderect(i.rect):
                return i
        
        return False
    
    def update(self, others):
        self.rect.move_ip(self.velocity.x, 0)

        if self.collide(others):
            self.rect.move_ip(-self.velocity.x, 0)
            self.velocity.x = 0
        
        self.rect.move_ip(0, self.velocity.y)

        c_result = self.collide(others)

        if c_result != False:
            if self.rect.bottom <= c_result.rect.top:
                self.onfloor = True

            self.rect.move_ip(0, -self.velocity.y)
            self.velocity.y = 0