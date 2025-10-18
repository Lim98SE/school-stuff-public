import pygame
import random

window = pygame.display.set_mode((1000, 1000))
stats = [
    [500, 500, 500, 500]
]

colors = [
    "#FF0000",
    "#FFFF00",
    "#00FF00",
    "#00FFFF"
]

for i in range(30):
    day = []
    for x in range(4):
        current = stats[-1][x]
        current += random.randint(-100, 100)
        current = pygame.math.clamp(current, 0, 999999999999999)
        day.append(current)
    
    stats.append(day)

index = 0
step_size = 1000 // 30

for i in range(10):
    pygame.draw.line(window, "#050505", (0, i * 100), (1000, i * 100), 2)

for day in stats:
    for stock in range(4):
        if (index != 0):
            previous = stats[index - 1][stock]
        
        else:
            previous = stats[0][stock]

        current = day[stock]
        pygame.draw.line(window, colors[stock], ((index - 1) * step_size, 1000 - previous), ((index) * step_size, 1000 - current), 3)
    
    index += 1

pygame.display.update()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
    
    pygame.display.update()

main()
pygame.quit()