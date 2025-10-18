import pygame
import os
import random

pygame.init()

window = pygame.display.set_mode((1440, 810), pygame.NOFRAME)
scanline_scale = 4
scanlines = pygame.Surface((window.get_width() / scanline_scale, window.get_height() / scanline_scale), pygame.SRCALPHA)

frame = 0

fade_gradient = pygame.image.load("gradient.png")

top_gradient = pygame.transform.scale(fade_gradient, (window.get_width(), fade_gradient.get_height()))
bottom_gradient = pygame.transform.scale(fade_gradient, (window.get_width(), fade_gradient.get_height()))
bottom_gradient = pygame.transform.rotate(bottom_gradient, 180)

def generate_scanlines():
    scanlines.fill("#00000000")

    for i in range(-2, (window.get_height() // 2) + 2):
        y = (i * 2)
        width = 0
        pygame.draw.line(scanlines, colors["highlight"], (width / 2, y), ((scanlines.get_width() - width / 2), y))

font = pygame.font.SysFont("Jetbrains Mono", 64)
small_font = pygame.font.SysFont("Jetbrains Mono", 32, italic=True)

class TextFragment:
    def __init__(self, color, text, position: pygame.Vector2, velocity: pygame.Vector2):
        self.color = color
        self.text = text
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
    
    def update(self):
        self.position += self.velocity

        if self.position.y < -129 or self.position.y > window.get_height() + 128:
            fragments.remove(i)
    
    def draw(self):
        return [font.render(self.text, True, self.color), self.position]

class ImageFragment:
    def __init__(self, image, position: pygame.Vector2, velocity: pygame.Vector2):
        self.image = image
        self.position = position
        self.velocity = velocity
    
    def update(self):
        self.position += self.velocity

        if self.position.y < -self.image.height or self.position.y > window.get_height() + 128:
            fragments.remove(i)
    
    def draw(self):
        return [self.image, self.position]

running = True

colors = {
    "background": "#0c0e13",
    "highlight": "#141720",
    "green": "#638229",
    "blue": "#75c0f9",
    "white": "#FFFFFF",
    "orange": "#f4b763",
    "red": "#e0787b",
    "cyan": "#a7e4cc",
    "purple": "#cba8f9"
}

clock = pygame.time.Clock()

scroll_speed = 3
lines = []

files = []

def search_files(directory):
    try:
        for i in os.listdir(directory):
            if os.path.isdir(i):
                search_files(i)
            
            if i.split(".")[-1] in ["py", "html", "js", "css", "php", "dbl", "c", "cpp", "sh", "bat", "gd", "asm", "go", "h", "hpp", "ps1", "cs", "lds"]:
                print(i)
                files.append([os.path.abspath(f"{directory}\\{i}"), "text"])
            
            elif i.split(".")[-1] in ["png", "jpg", "jpeg", "bmp"]:
                print(i)
                files.append([os.path.abspath(f"{directory}\\{i}"), "image"])
        
    except OSError:
        return

directories = [
    r"C:\Users\Lim\Documents\Projects",
    r"C:\Users\Lim\Documents\Godot",
    r"C:\Users\Lim\Documents\Game Assets"
]
os.chdir(r"C:\Users\Lim\Documents\Projects")
search_files(os.getcwd())

# os.chdir(r"C:\Users\Lim\Documents\Godot")

# search_files(os.getcwd())

images = []

for i in files:
    if i[-1] == "text":
        with open(i[0]) as file:
            lines += file.read().split("\n")
    
    else:
        print(i)
        images.append(pygame.image.load(i[0]))

buffer = []

for i in lines:
    if len(i.strip()) != 0:
        buffer.append(i)

lines = buffer.copy()

def spawn_fragment():
    mode = random.randint(0, 10) == 8 # 0 -> text, 1 -> image
    axis = random.randint(0, 1)

    ref = pygame.Surface((0, 0))
    
    if mode == 0:
        text = random.choice(lines).strip()
        color = colors[random.choice(["blue", "green", "highlight", "white", "orange", "red", "cyan", "purple"])]
        ref =  font.render(text, True, color)
        max_offset = window.get_width() - ref.get_width()
    
    else:
        image = random.choice(images)
        ref = image
        max_offset = window.get_width() - ref.get_width()

    if max_offset < 0:
        max_offset = 0

    offset = random.randint(0, max_offset)
    velocity = pygame.Vector2(0, 0)
    position = pygame.Vector2(offset, axis * window.get_height() + (ref.get_height() if axis else -ref.get_height()))

    if axis == 0:
        velocity.y = random.randint(1, 10) / 10
    
    else:
        velocity.y = random.randint(-10, 1) / 10

    if mode == 0: # Text fragment
        frag = TextFragment(color, text, position, velocity)
        fragments.append(frag)
    
    else:
        frag = ImageFragment(image, position, velocity)
        fragments.append(frag)

fragments = [
]

fragment_frames = random.randint(10, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(colors["background"])
    generate_scanlines()

    window.blit(pygame.transform.scale(scanlines, window.get_size()), (0, (frame / scroll_speed) % 8))

    for i in fragments:
        i.update()
        frag = i.draw()
        window.blit(frag[0], frag[1])
    
    window.blit(top_gradient, (0, 0))
    window.blit(bottom_gradient, (0, window.get_height() - bottom_gradient.get_height()))

    exposition = small_font.render("All the code you see is from this program's source.", True, "#FFFFFF")
    window.blit(exposition, (8, window.get_height() - exposition.get_height() - 8))

    pygame.display.update()

    frame += 1
    fragment_frames -= 1
    clock.tick(60)

    if fragment_frames <= 0:
        fragment_frames = random.randint(10, 200)
        spawn_fragment()

pygame.quit()