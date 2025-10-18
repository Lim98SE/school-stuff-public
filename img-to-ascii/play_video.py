import os
import time
framerate = 20

for i in sorted(os.listdir("frames")):
    start = time.time()
    with open(f"frames/{i}", "rb") as file:
        data = file.read()
    
    data = data.decode("utf-8")
    os.system('cls')
    print(data)

    while time.time() - start < 1 / framerate:
        pass