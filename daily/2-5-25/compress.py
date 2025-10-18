import base64
import zlib

with open("tiny-bird.py", "rb") as file:
    data = file.read()

print(len(data))

compressed = base64.b64encode(zlib.compress(data, 9))

print(compressed, len(compressed))