from PIL import Image, ImageOps, ImageGrab
import math
import sys
import os
import pygame
import colorit

color_pallate = [
    "#FFFFFF",
    "#808080",
    "#FF0000",
    "#FFFF00",
    "#00FF00",
    "#00FFFF",
    "#0000FF",
    "#FF00FF"
]

enable_color = False
enable_aa = True
frame_counter = 0
framerate = 99999

for i in os.listdir("frames"):
    os.remove(f"frames/{i}")

import cv2

cap = cv2.VideoCapture("input.mp4")

index = 0

frame_div = 3

while (cap.isOpened()):
    ret, frame = cap.read()

    index += 1

    if (index % frame_div != 0):
        continue

    if ret == True:
        name = f"inp_frames/{index // frame_div}.png"
        cv2.imwrite(name, frame)

        print(f"Frame {index // frame_div} saved")
    
    else:
        break

cap.release()
print("Done!!! :3 :3 :3")

def load(frame: pygame.Surface):
    global frame_counter
    frame_counter += 1
    # image = Image.frombytes("RGB", frame.get_size(), pygame.image.tobytes(frame, "RGB"))
    # image = ImageGrab.grab()
    image = Image.open(f"inp_frames/{frame_counter}.png")
    image = ImageOps.autocontrast(image)
    image = ImageOps.posterize(image, 4)
    scale = 6
    image = image.resize((image.size[0] // scale, image.size[1] // scale), Image.NEAREST)
    grayscale_image = image.convert("L")

    bpp_range = int(255 // math.pow(2, bpp))

    tiny = ImageOps.posterize(grayscale_image, bpp)
    chars = " .-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C\}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

    charset = ""

    for i in range(pow(2, bpp)):
        charset += chars[math.floor(translate(i, 0, 255 // bpp_range, 0, len(chars)))]

    chars = charset

    image_data = []
    color_data = []

    index = 0
    line = 0

    for y in range(tiny.size[1]):
        image_data.append([])
        for x in range(tiny.size[0]):
            image_data[y].append(tiny.getpixel((x, y)) // (255 // bpp_range))
    
    for y in range(tiny.size[1]):
        color_data.append([])
        for x in range(tiny.size[0]):
            color_data[y].append(image.getpixel((x, y)))

    string = ""

    for y in range(len(image_data)):
        x_idx = 0
        for x in color_data[y]:
            try:
                if enable_color: string += colorit.color_front(chars[image_data[y][x_idx]] if enable_aa else "█", x[0], x[1], x[2]) * 2
                else: string += chars[image_data[y][x_idx]] * 2
            
            except IndexError:
                string += " "
            
            x_idx += 1
            pass
        
        string += "\n"
    
    # print(string)
    print(frame_counter)

    with open(f"frames/{str(frame_counter).zfill(6)}.txt", "wb") as file:
        file.write(string.encode("utf-8"))

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

import pygame.camera as camera

camera.init()

main_cam = camera.Camera(camera.list_cameras()[0])

main_cam.start()

pygame.time.delay(1000)

import time

def main():
    while True:
        try:
            start = time.time()
            os.system("cls")
            load(main_cam.get_image())
            # break
            
            while time.time() - start < 1 / framerate:
                pass
        
        except KeyboardInterrupt:
            break

main()