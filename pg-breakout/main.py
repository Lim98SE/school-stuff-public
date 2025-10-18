import pygame
import math
import random
import json

pygame.init()

# Parse colors from a *.hex file

colors = []
last_positions = []

darker_colors = [(192, 192, 192), (128, 128, 128), (64, 64, 64), (0, 0, 0)]
darker_colors.reverse()

def parse_colors(path):
    colors = []
    with open(path) as file:
        text = file.readlines()
        
        for i in text:
            colors.append("#" + i.strip())
    
    return colors

winFont = pygame.font.Font("font.ttf", 64)
scoreFont = pygame.font.Font("font.ttf", 32)

window_size = pygame.math.Vector2((960, 540))

window = pygame.display.set_mode((window_size.x, window_size.y))

block_size = pygame.Vector2(96, 48)
block_spacing = 5

block_count = pygame.Vector2()

block_count.x = math.floor(window_size.x / (block_size.x + block_spacing))
block_count.y = 4

block_offset = (block_size.x + block_spacing) // 4

class Block:
    def __init__(self, rect, color_id, index):
        self.rect = rect
        self.color = colors[color_id]
        self.index = index
    
    def draw(self, canvas: pygame.Surface):
        pygame.draw.rect(canvas, self.color, self.rect)
        pygame.draw.rect(canvas, (0, 0, 0), self.rect, 4)
        pygame.draw.rect(canvas, (255, 255, 255), self.rect, 2)
    
    def collide(self, pos: pygame.Vector2, size: pygame.Vector2):
        if (pos.y + size.y > self.rect.y) and (pos.y < self.rect.y + self.rect.h): # vertical
            if (pos.x + size.x > self.rect.x) and (pos.x < self.rect.x + self.rect.w): # lateral
                return True
        
        return False

with open("levels.json") as file:
    levels = json.load(file)

def generate_current_level(index):
    blocks = []

    current_color_idx = 0

    if (index >= len(levels)):
        block_count.y = levels[-1]["rows"]
    
    else:
        block_count.y = levels[index]["rows"]
    

    for y in range(int(block_count.y)):
        for x in range(int(block_count.x)):
            block_rect = pygame.Rect((x * (block_size.x + block_spacing) + block_offset, (block_size.y * (y + 1)) + (block_spacing * y)), (block_size.x, block_size.y))
            current_color_idx += random.randint(0, len(colors))
            index = (y * block_count.x) + x
            block = Block(block_rect, current_color_idx % len(colors), index)
            blocks.append(block)
    
    return blocks

stars = []
star_colors = [
    "#73644f",
    "#9c8772",
    "#ccaf9d",
    "#f2d7c7",
    "#ffffff"
]

layer_fades = [
    1,
    2,
    4,
    7,
    12
]

planet_image = pygame.image.load("planet.png")

star_layers = []
star_layer_count = 5

for i in range(star_layer_count):
    star_layers.append(pygame.Surface(window_size, pygame.SRCALPHA, 32))

class Star:
    def __init__(self, position, layer):
        self.position = position
        self.velocity = pygame.Vector2(0, (layer + 1) + (random.randint(-5, 10) / 10))
        self.size = 5 - (layer + 1)
        self.color = star_colors[layer]
        self.layer = layer
        self.boost = 0
    
    def update(self):
        self.position += self.get_velocity()

        if self.position.y + (self.size * 2) > window_size.y:
            self.position.y = -32
        
        self.boost -= 0.1
    
    def draw(self):
        pygame.draw.circle(star_layers[self.layer], self.color, self.position, self.size)
    
    def get_velocity(self):
        new_velocity = pygame.Vector2(self.velocity.x, self.velocity.y)
        
        if (self.boost > 0):
            new_velocity.y += self.boost
        
        else:
            self.boost = 0
        
        return new_velocity

for i in range(200):
    stars.append(Star(pygame.Vector2(random.randint(0, int(window_size.x)), random.randint(0, int(window_size.y))), random.randint(0, star_layer_count - 1)))

bg_surface = pygame.Surface(window_size)

clock = pygame.time.Clock()

paddle_size = pygame.Vector2(256, 16)
paddle = pygame.Rect((0, window_size.y - paddle_size.y - 48), (paddle_size.x, paddle_size.y))

ball_size = pygame.Vector2((32, 32))
init_velocity = pygame.Vector2(0, 3)
ball_velocity = init_velocity

inital_ball_pos = pygame.Vector2(((window_size.x // 2) + (ball_size.x // 2), (window_size.y // 2) + (ball_size.y // 2)))

ball = pygame.Rect((inital_ball_pos.x, inital_ball_pos.y), (ball_size.x, ball_size.y))

running = True

gamestate = 0
level = 0
timer_mode = 0
score = 0
# 0: ball reset
# 1: level advance

planet_showing = False
planet_position = pygame.Vector2(window_size.x // 2 - 256, -512)

colors = parse_colors(levels[level]["colors"])
blocks = generate_current_level(level)
planet_angle = 0

hit_sounds = [
    pygame.mixer.Sound("bounce1.wav"),
    pygame.mixer.Sound("bounce2.wav"),
    pygame.mixer.Sound("bounce3.wav")
]

die_sound = pygame.mixer.Sound("die.wav")

def play_hit_sound(sounds):
    sound = random.choice(sounds)
    sound.play()

while running:
    if not planet_showing and random.randint(0, 0xFFFF) == 0:
        planet_showing = True
        planet_position.y = -512

    for i in star_layers:
        fade = star_layers.index(i)
        i.fill((0, 0, 0, layer_fades[fade]))

    for i in stars:
        i.update()
        i.draw()

    bg_surface.fill((0, 0, 0))

    for i in star_layers:
        bg_surface.blit(i, (0, 0))
    
    if planet_showing:
        bg_surface.blit(pygame.transform.rotate(planet_image, planet_angle), planet_position)
        planet_position.y += 0.5
        planet_angle += 0.1

        if planet_position.y > window_size.y + 512:
            planet_showing = False
            planet_position.y = -512

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                gamestate = 1
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball_velocity.y = 15
        
        if event.type == pygame.USEREVENT:
            match timer_mode:
                case 0:
                    ball_velocity = init_velocity
                    ball_velocity.x = 0
                
                case 1:
                    level += 1
                    gamestate = 0
                    ball_velocity.y = abs(init_velocity.y)
                    ball_velocity.x = 0
                    ball.update((inital_ball_pos.x, inital_ball_pos.y), (ball.w, ball.h))

                    if (level >= len(levels)):
                        colors = parse_colors(levels[-1]["colors"])
                    
                    else:
                        colors = parse_colors(levels[level]["colors"])
                    
                    blocks = generate_current_level(level)
        
    if (gamestate == 0):
        last_positions.append(pygame.Vector2(ball.x, ball.y))

        if (len(last_positions) > 3):
            last_positions.pop(0)

        window.fill((0, 0, 0))

        window.blit(bg_surface, (0, 0))

        score_text = f"Level {level + 1} | Score: {score}"
        score_rendered = scoreFont.render(score_text, False, (255, 255, 255))
        score_rendered_rect = score_rendered.get_rect()
        window.blit(score_rendered, pygame.Vector2(window_size.x // 2 - score_rendered_rect.w // 2, window_size.y - score_rendered_rect.h))

        paddle.update((pygame.mouse.get_pos()[0] - (paddle.w // 2), paddle.y), (paddle.w, paddle.h))
        ball.update((ball.x + ball_velocity.x, ball.y + ball_velocity.y), (ball.w, ball.h))

        if (ball.y + ball.h) > (paddle.y): # vertical
            if (ball.x + ball.w) >= (paddle.x) and (ball.x <= paddle.x + paddle.w): # lateral
                ball_velocity.y = -3
                ball_offset = (paddle.x - ball.x) + (paddle.w / 2)
                ball_velocity.x = -ball_offset // 12
                play_hit_sound(hit_sounds)
        
        if (ball.x <= 0) or (ball.x >= window_size.x - ball.w):
            ball_velocity.x *= -1
            play_hit_sound(hit_sounds)

        if (ball.y <= -ball.h):
            ball_velocity.y *= -1
            play_hit_sound(hit_sounds)
        
        if (ball.y >= window_size.y):
            ball_velocity = pygame.Vector2(0, 0)
            ball.update((inital_ball_pos.x, inital_ball_pos.y), (ball.w, ball.h))
            timer_mode = 0
            timer = pygame.time.set_timer(pygame.USEREVENT, 1500, 1)
            die_sound.play()
        
        for i in last_positions:
            past_ball = pygame.Rect(i.x, i.y, ball.w, ball.h)
            pygame.draw.rect(window, darker_colors[last_positions.index(i)], past_ball)

        pygame.draw.rect(window, (255, 255, 255), paddle)
        pygame.draw.rect(window, (255, 255, 255), ball)

        new_blocks = blocks.copy()

        ball_flipped_yet = False

        for i in blocks:
            if (i.collide(pygame.Vector2(ball.x, ball.y), pygame.Vector2(ball.w, ball.h))):
                new_blocks.remove(i)
                score += 50 * (level + 1)
                play_hit_sound(hit_sounds)

                if (not ball_flipped_yet):
                    ball_velocity.y *= -1
                    ball_flipped_yet = True
                
                for star in stars:
                    star.boost += 3
            
            else:
                i.draw(window)
        
        if len(new_blocks) == 0:
            gamestate = 1
        
        blocks = new_blocks.copy()
    
    if gamestate == 1:
        gamestate = 2
        timer_mode = 1

        pygame.time.set_timer(pygame.USEREVENT, 1000, 1)
    
    if gamestate == 2:
        for star in stars:
            star.boost += 0.5

        text = winFont.render(f"Next level!", False, (255, 255, 255))
        text_rect = text.get_rect()
        window.fill((0, 0, 0))
        window.blit(bg_surface, (0, 0))

        text_pos = pygame.Vector2(window_size.x // 2 - text_rect.w // 2, window_size.y // 2 - text_rect.h // 2 - 32)
        window.blit(text, text_pos)

        text = winFont.render(f"Score: {score}", False, (255, 255, 255))
        text_rect = text.get_rect()
        text_pos = pygame.Vector2(window_size.x // 2 - text_rect.w // 2, window_size.y // 2 - text_rect.h // 2 + 32)
        window.blit(text, text_pos)

        paddle.update((pygame.mouse.get_pos()[0] - (paddle.w // 2), paddle.y), (paddle.w, paddle.h))
        pygame.draw.rect(window, (255, 255, 255), paddle)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()