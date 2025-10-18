import pygame
import math
pygame.init()
pygame.display.set_caption("sprite sheet")  # sets the window title
screen = pygame.display.set_mode((800,800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

import random

# CONSTANTS
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
SPACE = 4
keys = [False, False, False, False, False] #this list holds whether each key has been pressed

grid_size = 20

# MAP: 2 is brick
map = []

for x in range(grid_size):
    map.append([])
    for y in range(grid_size):
        map[x].append(0)

directions = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
]

direction = random.choice(directions)

surface = pygame.Surface((grid_size, grid_size))

xpos = grid_size // 2 #start point for x
ypos = grid_size // 2 #start point for y

for i in range(5000): #loop a bunch of times
    roll = random.randrange(1, 50) #change x direction if you generate a 1 

    if roll == 1:
        direction = random.choice(directions)
    
    xpos += direction[0]
    ypos += direction[1]

    #start back in the middle if you go off the screen
    if xpos > grid_size or xpos <0:
        xpos = grid_size // 2
    if ypos > grid_size or ypos< 0:
        ypos = grid_size // 2

    surface.set_at((xpos, ypos), 0xFFFFFF)

screen.blit(pygame.transform.scale(surface, screen.get_size()))
pygame.display.flip()

for x in range(grid_size):
    for y in range(grid_size):
        map[x][y] = int(surface.get_at((x, y)).r == 0) * 2
    
    print()

for x in map:
    print(x)

brick = pygame.image.load('brick.png')  # load your spritesheet
Link = pygame.image.load('link.png')  # load your spritesheet
Link.set_colorkey((255, 0, 255))  # this makes bright pink (255, 0, 255) transparent (sort of)

# player variables
xpos = 400  # xpos of player
ypos = 400  # ypos of player

# animation variables variables
frameWidth = 13
frameHeight = 20
RowNum = 0  # for left animation, this will need to change for other animations
frameNum = 0
ticker = 0
direction = DOWN

while not gameover:
    clock.tick(60)  # FPS

    for event in pygame.event.get():  # quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True

        #keyboard input---------------------------
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                keys[LEFT] = True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT] = False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = False




    #Left/right MOVEMENT-------------------------------------
    if keys[LEFT] == True:
        vx = -3
        RowNum = 0
        direction = LEFT

    elif keys[RIGHT] == True:
        vx = 3
        RowNum = 1
        direction = RIGHT
        
    else:
        vx = 0

    #map collision---------------------
    #left collision
    if map[int((ypos) / 40)][int((xpos - 5) / 40)] == 2 :
        xpos+=3
        print("left collision!")
       
    #right collision
    if map[int((ypos) / 40)][int((xpos + 15) / 40)] == 2:
        xpos-=3   
        print("right collision!") 


    xpos+=vx #update player xpos

    # Animation update
    ticker+=1
    if vx != 0: #only animate when moving
        if ticker % 10 == 0:  # only change frames every 10 ticks (make number smaller for faster running animation)
            frameNum += 1
    if frameNum > 7:
        frameNum = 0

    # Render section--------------------------------------------------------
    screen.fill((0, 0, 0))  # wipe screen so it doesn't smear
    # draw map
    for i in range(grid_size):
        for j in range(grid_size):
            if map[i][j] == 2:
                screen.blit(brick, (j * 40, i * 40), (0, 0, 40, 40))

    # draw player
    screen.blit(Link, (xpos, ypos), (frameWidth * frameNum, RowNum * frameHeight, frameWidth, frameHeight))
    pygame.display.flip()  # this actually puts the pixel on the screen

# end game loop
pygame.quit()

