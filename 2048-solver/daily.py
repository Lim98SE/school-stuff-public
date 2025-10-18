import pygame

size = 800
div_size = 10
block_size = size // div_size

window = pygame.display.set_mode((size, size))

c1 = [
    (214, 196, 163),
    (61, 49, 37)
]

c2 = [
    (114, 179, 232),
    (52, 113, 235),
    (43, 81, 207),
    (37, 56, 196),
    (27, 30, 171)
]

c3 = [
    "#c5fcc6",
    "#79b086",
    "#48735d"
]

c4 = [
    "#FFFFFF",
    "#CCCCCC",
    "#999999",
    "#555555",
    "#222222",
    "#000000",
    "#000000",
    "#000000",
    "#000000",
    "#000000",
    "#000000",
    "#000000",
    "#222222",
    "#555555",
    "#999999",
    "#CCCCCC"
]

def rotate(l, n):
    return l[-n:] + l[:-n]

print(block_size)

def draw_blocks(colors, iny, inb):
    index = 0

    for y in range(div_size):
        for x in range(div_size):
            ax = x * block_size
            ay = y * block_size
            index += inb
            color = colors[index % len(colors)]
            rect = pygame.Rect((ax, ay), (block_size, block_size))

            pygame.draw.rect(window, color, rect)
        
        index += iny
        
    pygame.display.update()

running = True
clock = pygame.time.Clock()

mode = 0
modes = [
    [c1, 1, 1, 0, 999999],
    [c2, 1, 0, 1, 8],
    [c3, 2, 2, 1, 12],
    [c4, 1, 0, 1, 12]
]

colors = modes[mode][0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 0
                colors = modes[mode][0]
            
            if event.key == pygame.K_2:
                mode = 1
                colors = modes[mode][0]
            
            if event.key == pygame.K_3:
                mode = 2
                colors = modes[mode][0]
            
            if event.key == pygame.K_4:
                mode = 3
                colors = modes[mode][0]

    colors = rotate(colors, modes[mode][3])
    draw_blocks(colors, modes[mode][1], modes[mode][2])
    clock.tick(modes[mode][4])

pygame.quit()