import pygame

window = pygame.display.set_mode((960, 540))

class Shape:
    def __init__(self, type, data, color):
        self.type = type
        self.data = data
        self.color = color
    
    def draw(self):
        if self.type == "rect":
            pygame.draw.rect(window, self.color, self.data)
        
        if self.type == "circ":
            pygame.draw.circle(window, self.color, self.data.xy, self.data.z)

data = []

global_color = "#000000"
size = pygame.Vector2(50, 50)

def create_square():
    rect = pygame.Rect(pygame.mouse.get_pos() - (size / 2), size)
    data.append(Shape("rect", rect, global_color))

def create_circle():
    mpos = pygame.mouse.get_pos()
    circ = pygame.Vector3(mpos[0], mpos[1], size.x / 2)
    data.append(Shape("circ", circ, global_color))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                create_square()
            
            elif pygame.mouse.get_pressed()[2]:
                create_circle()
    
    window.fill("#FFFFFF")

    for i in data:
        i.draw()

    pygame.display.update()

pygame.quit()