import numpy as np
import random
import math
import matplotlib.pyplot as mpl

def clamp(a, mn, mx):
    if a < mn: return mn
    if a > mx: return mx
    return a

points = []

def random_coord(min, max):
    coord = random.randint(min, max)
    return coord

for i in range(2000):
    points.append((i, i + random.randint(0, i)))

x_points = np.array([])
y_points = np.array([])

for i in points:
    x_points = np.append(x_points, [i[0]])
    y_points = np.append(y_points, [i[1]])

x_size = math.ceil(x_points.max())

# ok now for the regression

def get_b(x_positions, y_positions):
    iterations = len(x_positions)
    sum_x = sum(x_positions)
    sum_y = sum(y_positions)

    sum_xy = 0
    sum_x2 = 0

    for i in range(iterations):
        sum_xy += x_positions[i] * y_positions[i]
        sum_x2 += pow(x_positions[i], 2)
    
    b = (iterations * sum_xy - sum_x * sum_y) / (iterations * sum_x2 - sum_x * sum_x)

    return b

def get_line_eq(x, y):
    iterations = len(x)
    b = get_b(x, y)
    mean_x = round(sum(x) / iterations)
    mean_y = round(sum(y) / iterations)

    a = mean_y - b * mean_x

    return [a, b]

def render_line(equation_inputs, iterations, step):
    x = 0
    rendered_line = []
    for i in range(iterations):
        y = equation_inputs[0] + (equation_inputs[1] * x)
        rendered_line.append(y)
        x += step
    
    return rendered_line

line_eq = get_line_eq(x_points, y_points)
line_points = render_line(line_eq, x_size, 1)

mpl.scatter(x_points, y_points, c="#000000")
mpl.plot(line_points, linewidth="3")
mpl.show()