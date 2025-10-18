import random
import math
import pygame

array = list(range(0, 2000))
random.shuffle(array)

sorted_array = []

surface_width = len(array)

surface = pygame.Surface((surface_width, surface_width))

pygame.init()

tone = pygame.Sound("tone.wav")

print(array)

window = pygame.display.set_mode((800, 600))

def max_both_arrays(ar1, ar2):
    if len(ar1) == 0: return max(ar2)
    if len(ar2) == 0: return max(ar1)
    ar1_m = max(ar1)
    ar2_m = max(ar2)

    if ar1_m > ar2_m:
        return ar1_m
    
    return ar2_m

def min_both_arrays(ar1, ar2):
    if len(ar1) == 0: return min(ar2)
    if len(ar2) == 0: return min(ar1)
    ar1_m = min(ar1)
    ar2_m = min(ar2)

    if ar1_m > ar2_m:
        return ar1_m
    
    return ar2_m

def draw_rods():
    surface.fill("#000000")
    pygame.event.get()
    global array
    global sorted_array

    arr_max = max_both_arrays(array, sorted_array)

    index = 0

    for i in array:
        pygame.draw.line(surface, "#FFFFFF" if index != highlight else "#FF0000", (index, arr_max - i), (index, 2000))

        tone.play()

        index += 1
    
    window.blit(pygame.transform.scale(surface, window.get_size()), (0, 0))

    pygame.display.update()

highlight = 0

def step():
    global array
    global sorted_array
    global highlight

    smallest = math.inf
    index = 0
    smallest_index = None

    for item in array:
        highlight = index

        if item in sorted_array: break

        if item < smallest and not item in sorted_array:
            smallest = item
            smallest_index = index
        
        draw_rods()
        
        index += 1
    
    if smallest_index == None:
        return 0
    
    sorted_array.append(array[smallest_index])
    array.append(array.pop(smallest_index))

    return 1

length = len(array)

while length > 0:
    length = step()
    draw_rods()

while True:
    draw_rods()