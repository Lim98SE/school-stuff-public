import pygame
import tkinter as tk
from tkinter import colorchooser, filedialog
import multiprocessing
import ctypes
import os

killAllThreads = False

def brushMainLoop(currentSize, bsizeVar):
    bsizeVar.value = currentSize

def disable_event(*args):
    pass

def brushSlider(bsizeVar):
    print(bsizeVar)
    brushSize = bsizeVar.value

    thWindow = tk.Tk("Brush Size")
    thWindow.geometry("192x400")

    slider = tk.Scale(thWindow, from_=1, to=16, length=400)
    slider.set(brushSize)
    slider.pack()

    thWindow.resizable(False, False)

    thWindow.protocol("WM_DELETE_WINDOW", disable_event)

    print("Pre-wjile :3")

    while True:
        thWindow.update()
        brushMainLoop(slider.get(), bsizeVar)

if __name__ == "__main__":
    imageSize = [1280, 720]

    statusBarSize = 64
    statusBarPadding = 8
    statusBarSpace = statusBarSize + statusBarPadding

    def getPos(x):
        print((statusBarPadding * x) + (64 * (x - 1)))
        return (statusBarPadding * x) + (64 * (x - 1))
    
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((imageSize[0], imageSize[1] + statusBarSpace))

    class Button:
        def __init__(self, image, pos, size):
            self.image = pygame.image.load(image)
            self.bbox = pygame.Rect(pos, size)
            self.fsc = 0
        
        def pressed(self):
            mousePos = pygame.mouse.get_pos()

            if not pygame.mouse.get_pressed()[0] or self.fsc > 0:
                return False
            
            if self.bbox.collidepoint(mousePos):
                self.fsc = 60
                return True
            
            return False
        
        def render(self):
            window.blit(self.image, self.bbox.topleft)
            self.fsc -= 1
            
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    running = True

    canvas = pygame.Surface(imageSize)
    buffer = pygame.Surface(imageSize, pygame.SRCALPHA, 32)
    bufferBuffer = pygame.Surface(imageSize, pygame.SRCALPHA, 32)

    doneDrawing = False

    mouseState = False
    mousePos = [0, 0]
    color = "#000000FF"
    brushSize = multiprocessing.Value(ctypes.c_int, 4)
    eraserBrushSize = 32

    bgColor = "#FFFFFF"

    canvas.fill(bgColor)
    lastMousePos = [0, 0]

    pencilButton = Button("pencil.png", (getPos(1), statusBarPadding / 2), (64, 64))
    colorButton = Button("color.png", (getPos(2), statusBarPadding / 2), (64, 64))
    saveButton = Button("save.png", (getPos(3), statusBarPadding / 2), (64, 64))
    loadButton = Button("load.png", (getPos(4), statusBarPadding / 2), (64, 64))
    boxButton = Button("box.png", (getPos(5), statusBarPadding / 2), (64, 64))
    filledBoxButton = Button("filled_box.png", (getPos(6), statusBarPadding / 2), (64, 64))

    startedDraw = False
    ogPosition = [0, 0]

    buttons = [
        pencilButton, colorButton, saveButton,
        loadButton, boxButton, filledBoxButton
    ]

    tool = 0
    # 0: brush
    # 1: box
    # 2: filled box
    # 3: fill bucket
    # 4: line
    # 5: eyedropper (or just middle click lol)

    brushThread = multiprocessing.Process(target=brushSlider, args=[brushSize])
    brushThread.start()

    while running:
        window.fill("#666666")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONUP:
                buffer.blit(bufferBuffer, (0, 0))
                startedDraw = False
                doneDrawing = True
        
        # logic!

        bufferBuffer.fill("#00000000")

        mousePos = list(pygame.mouse.get_pos())
        mousePos[1] -= statusBarSpace
        mouseState = pygame.mouse.get_pressed()

        if not mouseState[0]:
            doneDrawing = True
            startedDraw = False

        if mouseState[0]:
            if tool == 0: # brush
                pygame.draw.circle(buffer, color, lastMousePos, brushSize.value / 2)
                pygame.draw.circle(buffer, color, mousePos, brushSize.value / 2)
                pygame.draw.line(buffer, color, lastMousePos, mousePos, brushSize.value)
            
            if tool in [1, 2]:
                if not startedDraw:
                    ogPosition = mousePos
                    startedDraw = True
                
                pygame.draw.polygon(bufferBuffer, color,
                                    [(mousePos[0], mousePos[1]), (mousePos[0], ogPosition[1]), (ogPosition[0], ogPosition[1]), (ogPosition[0], mousePos[1])],
                                    brushSize.value if tool == 1 else 0)
        
        elif mouseState[2]:
            pygame.draw.circle(buffer, bgColor, lastMousePos, brushSize.value / 2)
            pygame.draw.circle(buffer, bgColor, mousePos, brushSize.value / 2)
            pygame.draw.line(buffer, bgColor, lastMousePos, mousePos, eraserBrushSize)
        
        if pencilButton.pressed():
            tool = 0
        
        if boxButton.pressed():
            tool = 1
        
        if filledBoxButton.pressed():
            tool = 2
        
        if colorButton.pressed():
            print("Clicked color button")
            color = colorchooser.askcolor(title="New color")[-1]
        
        if saveButton.pressed():
            filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension="*.png", filetypes=[("PNG File", "*.png")])

            pygame.image.save(canvas, filename)
        
        if loadButton.pressed():
            filename = filedialog.askopenfilename(defaultextension="*.png", filetypes=[("PNG File", "*.png")])

            if not os.path.exists(filename):
                continue

            loaded_file = pygame.image.load(filename)
            print(loaded_file.get_size())

            imageSize = loaded_file.get_size()
            pygame.display.quit()

            window = pygame.display.set_mode((imageSize[0], imageSize[1] + statusBarSpace))
            canvas = pygame.Surface(imageSize)
            buffer = pygame.Surface(imageSize, pygame.SRCALPHA, 32)
            bufferBuffer = pygame.Surface(imageSize, pygame.SRCALPHA, 32)
            canvas.blit(loaded_file, (0,0))

        # draw code!

        for i in buttons: i.render()

        if doneDrawing:
            canvas.blit(buffer, (0, 0))
            buffer.fill("#00000000")
            doneDrawing = False

        window.blit(canvas, (0, 72))

        window.blit(buffer, (0, statusBarSpace))

        window.blit(bufferBuffer, (0, statusBarSpace))

        pygame.display.update()

        lastMousePos = mousePos

        clock.tick(60)

        if not brushThread.is_alive():
            brushThread = multiprocessing.Process(target=brushSlider, args=[brushSize])
            brushThread.start()

    brushThread.kill()
    pygame.quit()