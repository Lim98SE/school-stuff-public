import numpy as np
import matplotlib.pyplot as plot

matrix = np.random.randint(0, 101, size=(50))
print("Random 5x1 matrix:\n", matrix)

print("Max of matrix:", np.max(matrix))
print("Min of matrix:", np.min(matrix))
print("Mean of matrix:", np.mean(matrix))

expl = [0] * matrix.size
expl[np.where(matrix == np.min(matrix))[0][0]] = 0.1

label = []

for i in matrix:
    label.append(i)

def make_random_color():
    color = np.random.randint(0, 1000, size=(3))
    color = np.divide(color, 1000)
    return list(color)

colors = []

for i in range(matrix.size):
    colors.append(make_random_color())

    if (i % 500 == 0):
        print(i)

plot.pie(matrix, labels=label, colors=colors, explode=expl)
# #0BA115 is "balls" as a hex code lol
plot.title("Pie :3 yummu :333")
plot.show()

# plot.scatter(range(matrix.size), matrix)
# plot.show()