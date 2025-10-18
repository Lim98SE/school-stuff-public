import base64
import zlib

with open("data.bin", "rb") as file:
    og_data = file.read()

def compress(data):
    new = zlib.compress(data, 9)
    new = base64.b64encode(new)
    return new

b64_data = compress(og_data)

print(len(b64_data))

with open("b64d.txt", "wb") as file:
    file.write(b64_data)