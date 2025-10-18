import pygame
pygame.init()

Vector2 = pygame.Vector2

win_size = Vector2(960, 540)

window = pygame.display.set_mode((win_size.x, win_size.y))
framerate = 60
clock = pygame.time.Clock()

class Button:
    def __init__(self, bbox):
        self.bbox = bbox
        self.clicked = False
        self.currently_clicked = False
    
    def render(self, color):
        pygame.draw.rect(window, color, self.bbox)
    
    def check_collision(self, position: Vector2):
        if position.x > self.bbox.x and position.x < self.bbox.x + self.bbox.w:
            if position.y > self.bbox.y and position.y < self.bbox.y + self.bbox.h:
                return True
        
        return False
    
    def hover(self):
        mpos = pygame.mouse.get_pos()
        actual_mpos = Vector2(mpos)
        if self.check_collision(actual_mpos):
            return True
        
        else:
            return False

running = True

btn = Button(pygame.Rect((0, 0), (128, 64)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((255, 255, 255))

    # draw

    btn.render("#00FF00")

    if btn.hover():
        print("Hovered!")

    # finalize

    pygame.display.update()
    clock.tick(framerate)

pygame.quit()