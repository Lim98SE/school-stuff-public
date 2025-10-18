from PIL import Image, ImageOps
import math
import sys

image = Image.open("image.png")
image = image.convert("L")
scale = 6
image = image.resize((image.size[0] // scale, image.size[1] // scale), Image.NEAREST)

try:
    bpp = int(sys.argv[1])

except IndexError:
    bpp = 4

def translate(value, leftMin, leftMax, rightMin, rightMax): # https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

bpp_range = int(255 // math.pow(2, bpp))
print(bpp_range)

tiny = ImageOps.posterize(image, bpp)
chars = " .-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C\}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

charset = ""

for i in range(pow(2, bpp)):
    charset += chars[math.floor(translate(i, 0, 255 // bpp_range, 0, len(chars)))]

chars = charset
print(len(chars))

image_data = []

index = 0
line = 0

print(tiny.size)

for y in range(tiny.size[1]):
    image_data.append([])
    for x in range(tiny.size[0]):
        image_data[y].append(tiny.getpixel((x, y)) // (255 // bpp_range))

for y in range(len(image_data)):
    for x in image_data[y]:
        try:
            print(chars[x] * 2, end="")
        
        except IndexError:
            print(x, end=" ")
        pass
    
    print()