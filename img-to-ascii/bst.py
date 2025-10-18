data = list(range(1, 20))

def binary_search(target):
    low_end = 0
    high_end = len(data) - 1

    found = False
    steps = 0

    while not found:
        current_index = (high_end + low_end) // 2

        print("step", steps + 1)

        if (data[current_index] == target): return current_index
        if (data[current_index] > target): high_end = current_index + 1
        if (data[current_index] < target): low_end = current_index - 1

        steps += 1

search = binary_search(5)

print(search, data[search])