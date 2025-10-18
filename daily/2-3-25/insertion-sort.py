import random
data = list(range(20))

random.shuffle(data)

print("Original:", data)

def swap(data: list, x, y):
    idx_a = data.index(x)
    idx_b = data.index(y)
    buffer = data[idx_b]
    data[idx_b] = data[idx_a]
    data[idx_a] = buffer
    return data

swaps = 0

for _ in range(len(data)): # horrible.
    for i in range(1, len(data)):
        a = data[i]
        b = data[i - 1]

        if (b > a):
            data = swap(data, a, b)
            swaps += 1
        
print("Sorted:", data)
print("Swap count:", swaps)