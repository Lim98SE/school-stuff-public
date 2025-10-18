import colorsys
import numpy as np
import pyvirtualcam
import cv2
from PIL import Image, ImageOps
import pygame
import string
import random
pygame.init()

c = cv2.VideoCapture(0)

# window = pygame.display.set_mode((480, 270), pygame.NOFRAME)
surface = pygame.Surface((1920, 1080))

downscale = 2
color_depth = 12

img_res = (128 // downscale , 67 // downscale)

chars = " "

# for i in range(11):
    # chars += random.choice(string.ascii_letters + string.digits)

chars = " .,-~*:=&%$#"
chars = list(chars)
chars.reverse()
chars = "".join(chars)

def ascii_ize(tiny):
    out_string = ""

    for y in range(tiny.height):
        for x in range(tiny.width):
            out_string += chars[tiny.getpixel((x, y))]
        
        out_string += "\n"
    
    return out_string

font = pygame.Font("font.ttf", 32)
tick = 20

with pyvirtualcam.Camera(width=1920, height=1080, fps=60) as cam:
    print(f'Using virtual camera: {cam.device}')
    output = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
    while True:
        ret, cap = c.read()
        surface.fill("#000000")
        ret, cap = c.read()
        image = Image.fromarray(cv2.cvtColor(cap, cv2.COLOR_BGR2RGB))
        image = ImageOps.autocontrast(image)
        image = image.crop((0, 0, 640, 360))
        image = image.resize(img_res, Image.Resampling.NEAREST)
        image = ImageOps.grayscale(image)
        image = image.quantize(color_depth)
        # image = image.convert("RGB")
        # image = ImageOps.autocontrast(image)

        text = ascii_ize(image)

        out_text = font.render(text, False, "#00FF00")
        surface.blit(out_text, (0, 0))
        # img = pygame.image.frombytes(image.tobytes(), img_res, "RGB")
        # surface.blit(pygame.transform.scale(img, surface.get_size()), (0, 0))
        frame = pygame.image.tobytes(surface, "RGB")
        frame = Image.frombytes("RGB", surface.get_size(), frame)
        output = np.array(frame)
        # pygame.event.get()
        # window.blit(pygame.transform.scale(surface, window.get_size()), (0, 0))
        # pygame.display.update()
        cam.send(output)
        tick += 1
        cam.sleep_until_next_frame()