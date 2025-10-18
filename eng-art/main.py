import pygame
import cv2
import math
import os

os.system("ffmpeg -y -i video.mp4 audio.mp3")
pygame.init()

font = pygame.font.Font("comicbd.ttf", 192)

audio = pygame.mixer.Sound("audio.mp3")

cap = cv2.VideoCapture('video.mp4')
success, img = cap.read()
shape = img.shape[1::-1]

window = pygame.display.set_mode((1280, 720), pygame.NOFRAME)

running = True

gay = [
    "#E40303",
    "#FF8C00",
    "#FFED00",
    "#008026",
    "#004CFF",
    "#732982"
]

bi = [
    "#DD2785",
    "#8869A5",
    "#2656B4"
]

nonbinary = [
    "#FCF434",
    "#FFFFFF",
    "#9C59D1",
    "#2C2C2C"
]

trans = [
    "#5BCEFA",
    "#F5A9B8",
    "#FFFFFF",
    "#F5A9B8",
    "#5BCEFA"
]

colors = [
    gay,
    bi,
    trans,
    nonbinary
]

def draw_stripes(colors, size_x, size_y, off_x = 0):
    y = 0

    for c in colors:
        pygame.draw.rect(window, c, pygame.Rect(off_x, y, size_x, size_y))
        y += size_y

clock = pygame.time.Clock()

todraw = 8

audio.play()

frame_counter = 0
flip = 0
drawingText = False
textSize = 1

ss = False

while running:
    frame_counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill("#FFFFFF")

    for i in range(todraw):
        width = int(1280 / todraw)
        color_set = colors[(i + flip) % len(colors)]

        draw_stripes(color_set, width, 720 / len(color_set), i * width)
    
    success, img = cap.read()

    textSize -= 0.05

    if frame_counter == (2 * 30) + 17:
        drawingText = True
        textSize = 1
        flip += 1
        ss = True

    if frame_counter == (3 * 30) + 7:
        flip += 1

    if not success:
        frame_counter = 0
        cap = cv2.VideoCapture('video.mp4')
        audio.play()
        continue
    
    frame = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
    frame = pygame.transform.scale(frame, (1280 // 2, 720 // 2))
    
    window.blit(frame, (0, 0))

    if drawingText:
        if textSize <= 0:
            drawingText = False
        
        else:
            textRender = font.render("GAY PEOPLE", True, (0, 0, 0))
            renderedText = pygame.transform.smoothscale_by(textRender, textSize + 0.1)
            textRect = renderedText.get_rect()

            center_x = (1280 / 2) - (textRect.w / 2)
            center_y = (720 / 2) - (textRect.h / 2)
            window.blit(renderedText, (center_x, center_y))

            textRender = font.render("GAY PEOPLE", True, (255, 255, 255))
            renderedText = pygame.transform.smoothscale_by(textRender, textSize)

            textRect = renderedText.get_rect()
            center_x = (1280 / 2) - (textRect.w / 2)
            center_y = (720 / 2) - (textRect.h / 2)
            window.blit(renderedText, (center_x, center_y))
    
    if ss:
        ss = False
        pygame.image.save(window, "screenshot.png")

    pygame.display.update()
    clock.tick(30)