# tic-tac-toe

import pygame

window = pygame.display.set_mode((800, 600))

colors = ["#000000", "#FF0000", "#0000FF"]

class Square:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.state = 0
        self.rect = rect = pygame.Rect((self.position * 155) + pygame.Vector2(100, 50), (150, 150))
        # 0 -> blank
        # 1 -> X
        # 2 -> O
    
    def draw(self):
        if self.check_hover():
            pygame.draw.rect(window, "#00FF00", self.rect, 4)
        
        else:
            pygame.draw.rect(window, colors[self.state], self.rect, 4)
    
    def check_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

window.fill("#FFFFFF")

running = True

squares = []

def get_square(x, y):
    for i in squares:
        if i.position.x == x and i.position.y == y: return squares.index(i)
    
    return -1

for x in range(3):
    for y in range(3):
        squares.append(Square((x, y)))

lines = [
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    [[0, 0], [1, 1], [2, 2]],
    [[2, 0], [1, 0], [0, 0]],
]

def check_lines():
    ret_lines = []

    for t in lines:
        test = []

        for i in t:
            print(t, squares[get_square(t[0], i[1])].state)
            test.append(squares[get_square(t[0], i[1])].state)
        
        ret_lines.append(test)
    
    return ret_lines

def determine_next_move():
    # step 1: check for anything to complete
    # step 2: check for anything to block
    # step 3: screw over opponent

    # check for completion

    test = check_lines()

    print(test)

    return

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(squares)):
                sq = squares.copy()
                s = squares[i]
                if s.check_hover() and s.state == 0:
                    sq[i].state = 1
                    squares = sq.copy()
                
            
            determine_next_move()
    
    window.fill("#FFFFFF")

    for i in squares:
        i.draw()
    
    pygame.display.update()