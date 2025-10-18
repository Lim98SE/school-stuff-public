import base64
import zlib
import pygame

with open("b64d.txt", "rb") as file:
    data = zlib.decompress(base64.b64decode(file.read()))

reading = True

frame = b""
cmp_frames = []
ptr = 0
ptr_offset = 0
lastFinishedPtr = 0

while reading:
    last2 = (frame[-4:])

    if (ptr + ptr_offset) >= len(data) or (lastFinishedPtr == ptr + ptr_offset and ptr_offset != 0):
        print(f"Exceeded data at: {ptr + ptr_offset}")
        break

    if int.from_bytes(last2, "big") == 0 and ptr > 4:
        print(f"Frame finished at {ptr + ptr_offset} (last: {lastFinishedPtr})")
        cmp_frames.append(frame)
        ptr_offset = ptr
        ptr = 0
        lastFinishedPtr = ptr_offset + ptr

    frame += data[ptr + ptr_offset].to_bytes()
    ptr += 1

frames = []

for i in cmp_frames:
    frames.append(zlib.decompress(i))

for i in frames:
    print(i)