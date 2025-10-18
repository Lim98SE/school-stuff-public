import pygame

window = pygame.display.set_mode((960, 540))

neighbors = [[-1, 0], [1, 0], [0, -1], [0, 1]]

field = []

for y in range(window.get_height()):
    field.append([])
    for x in range(window.get_width()):
        field[y].append(window.get_at((x, y)))

def flood_fill(x ,y, old, new):
    # we need the x and y of the start position, the old value,
    # and the new value
    # the flood fill has 4 parts
    # firstly, make sure the x and y are inbounds
    if x < 0 or x >= len(field[0]) or y < 0 or y >= len(field):
        return
    # secondly, check if the current position equals the old value
    if field[y][x] != old:
        return

    # thirdly, set the current position to the new value
    field[y][x] = new
    # fourthly, attempt to fill the neighboring positions
    try:
        flood_fill(x+1, y, old, new)
        flood_fill(x-1, y, old, new)
        flood_fill(x, y+1, old, new)
        flood_fill(x, y-1, old, new)
    
    except RecursionError:
        print("RECURSION ERROR LMFAO")
        return
    
    return

pygame.display.update()

flood_fill(0, 0, (0, 0, 0, 255), (255, 255, 255, 255))

X, Y = 0, 0

for y in field:
    for x in y:
        window.set_at((X, Y), x)
        X += 1
    
    Y += 1

while True:
    pygame.event.get()