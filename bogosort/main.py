import random
import time

list = list(range(100))
random.shuffle(list)
sorted_list = sorted(list)

start_time = time.time_ns()

tests = 0

while list != sorted_list:
    random.shuffle(list)
    tests += 1

    if tests % 100000 == 0:
        print(f"{tests} tests completed")

print(time.time_ns() - start_time, f"{tests} tests")


