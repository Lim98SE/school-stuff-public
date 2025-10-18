import pygame
import json

arrow_colors = [
    "#FF0000",
    "#00FF00",
    "#00FFFF",
    "#FF00FF"
]

class Arrow:
    def __init__(self, index, is_guide = False):
        self.sprite = pygame.image.load("assets/arrow.png" if not is_guide else "assets/guide_arrow.png")
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))
        self.color = arrow_colors[index]

        self.sprite.fill(self.color, special_flags=pygame.BLEND_MULT)
        self.sprite = pygame.transform.rotate(self.sprite, index * 90)

class Note:
    def __init__(self, index, y_pos):
        self.arrow = Arrow(index)
        self.pos = y_pos
        self.index = index
    
    def draw(self):
        window.blit(self.arrow.sprite,  ((self.index * 64) + ((self.index + 1) * 16), self.pos))
    
    def update(self, delta):
        self.pos += arrow_speed * delta
    
    def check(self):
        if self.pos < bar_height - 96: return "SKIP"
        if self.pos > bar_height - 64 and self.pos < bar_height + 48:
            return bar_height - self.pos
        
        return "NO HIT"


window = pygame.display.set_mode((1280, 720))

bar_height = window.get_height() - 64 - 16 + 32

running = True
time = 0

arrow_sprites = [
    Arrow(0, True),
    Arrow(1, True),
    Arrow(2, True),
    Arrow(3, True)
]

arrows = []
keybinds = [
    pygame.K_d,
    pygame.K_f,
    pygame.K_j,
    pygame.K_k
]

def parse_note(note):
    keys = note["note"]
    offset = note["time"]
    output = []

    for i in range(4):
        if (keys & (1 << i)) >> i:
            output.append(Note(i, -offset))
    
    return output

with open("charts/cool_chart.json") as file:
    chart = json.load(file)

for i in chart["notes"]:
    keys = parse_note(i)
    arrows.extend(keys)

clock = pygame.time.Clock()
arrow_speed = 0.5

pygame.init()
pygame.mixer_music.load(chart["song"])

pygame.mixer.music.play()
font = pygame.font.SysFont("Comic Sans", 64)

score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.KEYDOWN:
            temp_arrows = arrows.copy()
            for i in arrows:
                chk = i.check()

                if chk == "SKIP":
                    continue

                if chk != "NO HIT":
                    if event.key == keybinds[i.index]:
                        score += 64 - abs(chk)
                        temp_arrows.remove(i)
            
            arrows = temp_arrows.copy()

    score = round(score)

    window.fill("#FFFFFF")

    for i in arrows:
        i.draw()
        i.update(clock.get_time())
    
    for i in range(len(arrow_sprites)):
        window.blit(arrow_sprites[i].sprite, ((i * 64) + ((i + 1) * 16), window.get_height() - 64 - 16))

    score_render = font.render(str(score), True, "#000000")
    window.blit(score_render, (window.get_width() - score_render.get_width() - 8, 8))

    pygame.display.update()
    clock.tick(60)

    time += clock.get_time()

pygame.quit()