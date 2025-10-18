import pygame
import random

window = pygame.display.set_mode((800, 800))

sequence = [random.randint(0, 3)]

on_colors = [
    "#FF0000",
    "#FFFF00",
    "#00FF00",
    "#0000FF"
]

off_colors = [
    "#880000",
    "#888800",
    "#008800",
    "#000088"
]

pygame.init()

sounds = [
    pygame.Sound("a.wav"),
    pygame.Sound("b.wav"),
    pygame.Sound("c.wav"),
    pygame.Sound("d.wav"),
    pygame.Sound("loss.mp3")
]

playing_step = -1
step = 0

running = True

state = 0
# 0 -> playing sequence
# 1 -> player input
# 2 -> resetting

class Button:
    def __init__(self, id, pos):
        self.rect = pygame.Rect(pos, (300, 300))
        self.id = id
    
    def draw(self):
        if playing_step >= 0:
            c = on_colors[self.id] if (sequence[playing_step] == self.id) else off_colors[self.id]

        else:
            c = on_colors[self.id] if self.get_hover() else off_colors[self.id]

        pygame.draw.rect(window, c, self.rect)
    
    def get_hover(self):
        return self.rect.collidepoint(mouse_pos)
    
    def get_clicked(self):
        return self.get_hover() and pygame.mouse.get_just_pressed()[0]

mouse_pos = (0, 0)

buttons = [
    Button(0, (50, 50)),
    Button(1, (400, 50)),
    Button(2, (50, 400)),
    Button(3, (400, 400))
]

clock = pygame.time.Clock()
frames_until_next = 30

font = pygame.font.SysFont("Comic Sans", 64)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

    window.fill("#FFFFFF")

    score = str(len(sequence))
    render = font.render(score, True, "#808080")

    for i in buttons: i.draw()

    window.blit(render, (4, 4))

    if state == 0:
        frames_until_next -= 1

        if frames_until_next <= 0:
            frames_until_next = 30
            playing_step += 1

            if (playing_step >= len(sequence)):
                state = 1
                playing_step = -1
            
            else:
                sounds[sequence[playing_step]].play()
    
    elif state == 1:
        for i in buttons:
            if i.get_clicked():
                if (i.id == sequence[step]):
                    step += 1
                    sounds[i.id].play()

                    if (step >= len(sequence)):
                        step = 0
                        playing_step = -1
                        sequence.append(random.randint(0, 3))
                        state = 0
                
                else:
                    frames_until_next = 60 * 5
                    sounds[4].play()
                    state = 2
    
    elif state == 2:
        frames_until_next -= 1

        if frames_until_next <= 0:
            frames_until_next = 30
            sequence = []
            step = 0
            playing_step = -1
            sequence.append(random.randint(0, 3))
            state = 0

    pygame.display.update()

    clock.tick(60)

pygame.quit()