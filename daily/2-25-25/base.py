import pygame
import random
pygame.init()#initializes Pygame
pygame.display.set_caption("random walk")#sets the window title
screen = pygame.display.set_mode((800, 800))#creates game screen
xpos = 400 #start point for x
ypos = 400 #start point for y

directions = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
]

grid = [[0] * 80] * 60

direction = random.choice(directions)

surface = pygame.Surface((80, 60))

#render section---------------------------------------------
    
for i in range(5000): #loop a bunch of times
    roll = random.randrange(1, 50) #change x direction if you generate a 1 

    if roll == 1:
        direction = random.choice(directions)
    
    xpos += direction[0]
    ypos += direction[1]

    #start back in the middle if you go off the screen
    if xpos > 80 or xpos <0:
        xpos = 40
    if ypos > 60 or ypos< 0:
        ypos = 30

    surface.set_at((xpos, ypos), 0xFFFFFF)

screen.blit(pygame.transform.scale(surface, screen.get_size()))
pygame.display.flip()

for x in range(80):
    for y in range(60):
        grid[y][x] = int(surface.get_at((x, y)).r > 0)
        print(grid[y][x], end="")
    
    print()

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT: #close game window
        break

#end game loop##############################################
pygame.quit()
