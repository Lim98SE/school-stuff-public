from tqdm import tqdm
import threading

fmt = """REMOVE
    if (number) == %d:
        return True

    if (number) == %d:
        return False
"""

code_header = "def is_even(number):\n"
code = []

threads = []

def make_code_snippet(i):
    global code
    code.append((fmt % (i * 2, (i * 2) + 1)).replace("REMOVE", ""))

max_threads = 64

for i in tqdm(range(pow(2, 24) // 2)):
    if len(threads) < max_threads:
        t = threading.Thread(target=make_code_snippet, args=[i])
        threads.append(t)
        threads[-1].start()
    
    else:
        for t in threads:
            t.join()
            threads.remove(t)

actual_code = code_header

for i in code:
    actual_code += i

with open("is_even.py", "w") as file:
    file.write(actual_code)
