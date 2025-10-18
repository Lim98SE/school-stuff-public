import math

def distance(ax, ay, az, bx, by, bz):
    x = pow(bx - ax, 2)
    y = pow(by - ay, 2)
    z = pow(bz - az, 2)
    return math.sqrt(x + y + z)

key_color = [0, 0, 0]
bg_color = [255, 255, 255]

def key(color, tolerance):
    cr = color[0]
    cg = color[1]
    cb = color[2]
    kr = key_color[0]
    kg = key_color[1]
    kb = key_color[2]
    if distance(cr, cg, cb, kr, kg, kb) <= tolerance:
        return bg_color
    return color

test_cases = int(input())
tolerance = 0

for i in range(test_cases):
    line = input().strip().split(" ")
    key_color[0] = int(line[0])
    key_color[1] = int(line[1])
    key_color[2] = int(line[2])
    tolerance = int(line[3])
    fg_color = [0, 0, 0]
    fg_color[0] = int(line[4])
    fg_color[1] = int(line[5])
    fg_color[2] = int(line[6])
    bg_color[0] = int(line[7])
    bg_color[1] = int(line[8])
    bg_color[2] = int(line[9])
    output = key(fg_color, tolerance)

    for i in output:
        print(i, end=" ")
    
    print()