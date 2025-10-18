from PIL import Image
import zlib

frame = 1

def open_frame(frame, lf_data):
    image = Image.open(f"frames/{frame}.png").convert("L")
    data = []
    
    for y in range(image.size[1]):
        data.append([])
        for x in range(image.size[0]):
            data[y].append(image.getpixel((x, y)))

    actual_data = b""

    bytedata = []
    bit = 0
    byte = 0
    index = 0

    for y in data:
        for x in y:
            if bit >= 7:
                bytedata.append(byte)

                byte = 0
                bit = 0
                index += 1
            
            byte += x == 255
            byte <<= 1
            bit += 1

    for b in bytedata:
        actual_data += b.to_bytes()

    return actual_data

data = b""
frame = None

for i in range(3):
    frame = open_frame(i + 1, frame)
    actframe = zlib.compress(frame, 9)
    print(f"Frame {i} done! Length: {len(actframe)}")
    data += actframe
    data += int(0).to_bytes(4, "big")

print(len(data))
with open("data.bin", "wb") as file:
    file.write(data)