import pygame
import random

pygame.init()

running = True
window = pygame.display.set_mode((960, 540))

clock = pygame.time.Clock()

ticks_until_move = 20
ticks_between_moves = 5
direction = 1
step_size = 32
distance_between = 24
swarm_size_w = 16
swarm_size_h = 4
step_down = False

speed = 2
target_y = 0

origin = pygame.Vector2(16, 16)
boundary_right = 960 - (swarm_size_w * distance_between)
boundary_left = 16

invader_res = pygame.image.load("invaders.png")
player_res = pygame.image.load("player.png")
barrier_res = pygame.image.load("barrier.png")

shoot = pygame.Sound("shoot.wav")
explode = pygame.Sound("die.wav")
kill = pygame.Sound("alien_die.wav")
bHit = pygame.Sound("barrierHit.wav")
alienShoot = pygame.Sound("alienShoot.wav")

bgm = pygame.Sound("bgm.mp3")

def random_color():
    return pygame.Color.from_hsva(random.randint(0, 360), 100, 100, 100)

class Invader:
    def __init__(self, index, position, color, type):
        self.index = index
        self.offset = pygame.Vector2(position)
        self.color = pygame.Color(color)
        self.position = origin + self.offset
        self.fire_timer = random.randint(60 * 2, 60 * 20)
        self.sprite = invader_res.subsurface((type * 16, 0), (16, 16))
        self.rect = pygame.Rect(self.position, (16, 16))
    
    def update(self):
        global origin
        self.position = self.offset.copy() + origin.copy()
        self.fire_timer -= 1

        if (self.fire_timer == 0):
            self.fire_timer = random.randint(10, 1000)
            if random.randint(0, 5) == 0: # double tap
                self.fire_timer = random.randint(10, 50)

            global bullets
            bullets.append(Bullet(True, self.position, [0, 5]))
            alienShoot.play()
    
    def draw(self):
        self.position = self.offset.copy() + origin.copy()
        self.rect = pygame.Rect(self.position, (16, 16))
        window.blit(self.sprite, self.position)

class Bullet:
    def __init__(self, dangerous_to_player, position, velocity):
        self.position = position
        self.dangerous = dangerous_to_player
        self.velocity = pygame.Vector2(velocity)
        self.rect = pygame.Rect(self.position, (2, 2))
    
    def update(self):
        self.position += self.velocity
        self.rect = pygame.Rect(self.position, (2, 2))
    
    def draw(self):
        pygame.draw.circle(window, "#FFFFFF", self.position, 4)
    
    def collide(self, list):
        for i in list:
            # print(i)
            try: r = i.rect
            except AttributeError: r = i
            if self.rect.colliderect(r):
                if not self.dangerous and r != player_rect: return i
                if self.dangerous and not i is Invader: return i

class Barrier:
    def __init__(self, position):
        self.position = position
        self.health_level = 4
        self.hp_remaining = 4
        self.hp_per_level = 4
        self.rect = pygame.Rect(self.position, (96, 32))
    
    def hit(self):
        self.hp_remaining -= 1

        if self.hp_remaining == 0:
            self.hp_remaining = self.hp_per_level
            self.health_level -= 1

            if self.health_level == 0:
                global barriers
                barriers.remove(self)
    
    def draw(self):
        image = barrier_res.subsurface(((self.health_level - 1) * 96, 0), (96, 32))
        window.blit(image, self.position)

respawn_timer = 0
dead = False
lives = 3

barriers = [
]

for i in range(4):
    barrier = Barrier(((i * 256) + 32, 540 - 96))
    barriers.append(barrier)

player_pos = pygame.Vector2(0, 0)
player_rect = pygame.Rect(player_pos, (48, 32))

def p_update():
    player_pos.x += player_vel_x
    player_pos.y = window.get_height() - 32
    global player_rect
    player_rect = pygame.Rect(player_pos, (48, 32))

def p_draw(axis):
    frame = axis
    image = player_res.subsurface((frame * 48, 0), (48, 32))
    window.blit(image, player_pos)

def p_fire():
    global bullets
    b_pos = player_pos.copy()
    b_pos.x += 16 + 8
    return Bullet(False, b_pos, [0, -5])

invaders = []
bullets = []

index = -1

for y in range(swarm_size_h):
    for x in range(swarm_size_w):
        index += 1
        invaders.append(Invader(index, [(x) * (distance_between), (y) * (distance_between)], random_color(), y))

iframes = 0
player_vel_x = 0

stars = []
star_velocities = []
star_brightnesses = []

for i in range(3000):
    x = random.randint(0, 960 + 32)
    y = random.randint(0, 540)
    v = random.randint(1, 64)
    b = pygame.math.remap(1, 64, 25, 100, v)
    stars.append([x, y])
    star_velocities.append(v)
    star_brightnesses.append(b)


pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    if not dead:
        axis = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        player_vel_x += axis * 2
        player_vel_x *= 0.9
        p_update()

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            bullets.append(p_fire())
            shoot.play()
    
    window.fill("#000000")

    for i in range(len(stars)):
        window.set_at(stars[i], pygame.Color.from_hsva(0, 0, star_brightnesses[i], 100))
        stars[i][0] -= star_velocities[i]

        if stars[i][0] < -8:
            stars[i][0] = 960 + random.randint(8, 32)
            stars[i][1] = random.randint(0, 540)
            star_velocities[i] = random.randint(1, 64)
            star_brightnesses[i] = random.randint(25, 100)

    for invader in invaders:
        invader.update()
        invader.draw()
    
    for i in bullets:
        i.update()
        i.draw()
    
    for i in barriers:
        i.draw()
    
    hit_player = False
    hit_enemy = None

    buffer = invaders.copy()

    iframes -= 1
    
    for i in bullets:
        if i.dangerous and i.rect.colliderect(player_rect) and iframes < 0:
            dead = True
            respawn_timer = 60
            iframes = 60 * 3
            explode.play()
        
        hit_barrier = i.collide(barriers)

        if hit_barrier:
            hit_barrier.hit()
            bullets.remove(i)
            bHit.play()

            continue
        
        elif not i.dangerous:
            r = i.collide(invaders)
            if r:
                speed += 0.05
                buffer.remove(r)
                bullets.remove(i)
                kill.play()
                continue
    
    if not dead:
        p_draw(axis + 1)
    
    if respawn_timer == 0:
        dead = False

    pygame.display.update()

    ticks_until_move -= 1
    
    clock.tick(60)

    invaders = buffer.copy()

    if step_down:
        if origin.y >= target_y: step_down = False
        origin.y += speed
    
    else:
        origin.x += speed * direction

        if (origin.x > boundary_right or origin.x < boundary_left):
            direction *= -1
            origin.x += direction * speed
            step_down = True
            target_y += step_size
    
    respawn_timer -= 1
    iframes -= 1

pygame.quit()