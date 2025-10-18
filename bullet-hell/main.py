import pygame
import math
import random
from levels import *

pygame.init()

window = pygame.display.set_mode((960, 540))

bg_color = pygame.Color("#53a1e0")
player_position = pygame.Vector2(0, 0)
bullet_diam = 2
player_diam = 4

player_accel = 2
player_decel = 0.9
max_speed = 5

player_velocity = pygame.Vector2(0, 0)

health = 100

running = True
clock = pygame.time.Clock()
target_fps = 60

class Bullet:
    def get_color(self):
        return "#000000"
    
    def __init__(self, position, angle, speed):
        self.position = pygame.Vector2(position)
        self.angle = math.radians(angle)
        self.velocity = pygame.Vector2((0, 0))
        self.speed = speed
        self.color = self.get_color()
    
    def pre_tick(self):
        pass
    
    def post_tick(self):
        pass
    
    def move(self):
        self.position.x += (math.sin(self.angle) * self.speed) + self.velocity.x
        self.position.y += (math.cos(self.angle) * self.speed) + self.velocity.y
    
    def draw(self):
        pygame.draw.circle(window, self.get_color(), self.position, bullet_diam * 2)
        target_pos = self.position.copy()
        target_pos.x += ((math.sin(self.angle) * self.speed) + self.velocity.x) * 8
        target_pos.y += ((math.cos(self.angle) * self.speed) + self.velocity.y) * 8
        # pygame.draw.line(window, "#FF0000", self.position, target_pos, 2)
    
    def cull(self):
        if self.position.x > window.get_width() + 16 or self.position.x < -16:
            return True
        
        if self.position.y > window.get_height() + 16 or self.position.y < -16:
            return True
        
        return False

class GravityBullet(Bullet):
    def pre_tick(self):
        self.velocity.y += 0.3
    
    def get_color(self):
        return "#000020"

class FrictionBullet(Bullet):
    def pre_tick(self):
        self.speed *= 0.95
    
    def get_color(self):
        return "#200020"
    
    def post_tick(self):
        return self.speed < 0.05

bvel_lookup = [100, 150, 200, 250]

class BoomerangBullet(Bullet):
    def __init__(self, position, angle, speed):
        self.position = pygame.Vector2(position)
        self.start_position = pygame.Vector2(position)
        self.angle = math.radians(angle)
        self.start_angle = math.radians(angle)
        self.velocity = pygame.Vector2((0, 0))
        self.speed = speed
        self.bounces = 0
    
    def pre_tick(self):
        if self.position.distance_to(self.start_position) >= bvel_lookup[self.bounces] and self.bounces <= 2:
            self.angle += math.radians(180)
            self.bounces += 1
            # for i in range(5): self.move()
    
    def get_color(self):
        return "#802f0a"

class ClusterBullet(Bullet):
    def __init__(self, position, angle, speed):
        self.position = pygame.Vector2(position)
        self.angle = math.radians(angle)
        self.velocity = pygame.Vector2((0, 0))
        self.speed = speed
        self.ticks_until_explode = 90
    
    def post_tick(self):
        if self.ticks_until_explode == 0:
            spawn_circle((self.position.x, self.position.y), 8, 10)
            return True
        
        self.ticks_until_explode -= 1
    
    def get_color(self):
        return "#800000"

class RecursiveClusterBullet(ClusterBullet):
    def post_tick(self):
        if self.ticks_until_explode == 0:
            spawn_circle((self.position.x, self.position.y), 4, 3, bulletType=ClusterBullet)
            return True
        
        self.ticks_until_explode -= 1
    
    def get_color(self):
        return "#FF0000"

class EternalRecursiveClusterBullet(ClusterBullet):
    def post_tick(self):
        if self.ticks_until_explode == 0:
            spawn_circle((self.position.x, self.position.y), 2, 5, bulletType=ClusterBullet)
            self.ticks_until_explode += 90
        
        self.ticks_until_explode -= 1
    
    def get_color(self):
        return "#FFFFFF"

def pt_none(angle, speed, type, position, ticks, obj, mod = 1):
    return angle, speed, type, position

class BulletSpawner:
    def __init__(self, position, number, type, angle, speed, color, mod = 1, preTick = [pt_none], period = 30, activate_ticks = 0, deactivate_ticks = math.inf):
        self.position = position
        self.number = number
        self.type = type
        self.angle = angle
        self.speed = speed
        self.ticks = period
        self.period = period
        self.pretick = preTick
        self.mod = mod
        self.ticks_until_activate = activate_ticks
        self.active = self.ticks_until_activate == 0
        self.ticks_until_deactivate = deactivate_ticks
        self.ticks_alive = 0
        self.color = pygame.Color(color)
        self.stopped = []
    
    def tick(self):
        self.ticks_until_activate -= 1
        self.ticks_until_deactivate -= 1

        if self.ticks_until_activate <= 0: self.active = True
        if self.ticks_until_deactivate <= 0: self.active = False
        if not self.active: return

        for i in range(math.floor(len(self.pretick) / 2)):
            p = self.pretick[i * 2]
            m = self.pretick[(i * 2) + 1]
            if (i * 2) in self.stopped: continue
            self.angle, self.speed, self.type, self.position = p(self.angle, self.speed, self.type, self.position, self.ticks_alive, self, m)

        if self.ticks == 0:
            self.ticks = self.period
            spawn_circle(self.position, self.number, self.speed, self.angle, self.type)
        
        self.ticks -= 1
        self.ticks_alive += 1
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.position, 4)
        pygame.draw.circle(window, self.color.lerp("#000000", 0.9), self.position, 6, 2)

def pt_spin(angle, speed, type, position, ticks, obj, mod = 2):
    angle += mod
    # if ticks % 20 == 0: angle *= -1
    return angle, speed, type, position

def pt_sway(angle, speed, type, position, ticks, obj, mod = 1):
    p = pygame.Vector2(position)
    p.x = ((math.sin(ticks / (60 * (1 / mod)))) * (960 / 2)) + (960 / 2)
    return angle, speed, type, p

def pt_scale_speed(angle, speed, type, position, ticks, obj, mod = 1):
    return angle, speed + mod, type, position

def pt_sway_angle(angle, speed, type, position, ticks, obj, mod = 1):
    angle = math.sin(ticks / (60 * (1 / mod))) * 20
    return angle, speed, type, position

def pt_random_angle(angle, speed, type, position, ticks, obj, mod = 1):
    return random.randint(0, 360), speed, type, position

def pt_random_speed(angle, speed, type, position, ticks, obj, mod = 1):
    return angle, (random.randint(mod[0], mod[1]) * mod[2]) / mod[2], type, position

def pt_modify_after(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks == mod[0]:
        obj.pretick[mod[1]] = eval("original *FUNCTION* modifier".replace("*FUNCTION*", mod[2]), {
            "original": obj.pretick[mod[1]],
            "modifier": mod[3]
        })
    
    return angle, speed, type, position

def pt_modify_every(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks % mod[0] == 0:
        obj.pretick[mod[1]] = eval("original *FUNCTION* modifier".replace("*FUNCTION*", mod[2]), {
            "original": obj.pretick[mod[1]],
            "modifier": mod[3]
        })
    
    return angle, speed, type, position

def pt_modify_class_after(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks == mod[0]:
        new_value = eval("original *FUNCTION* modifier".replace("*FUNCTION*", mod[2]), {
            "original": eval(f"self.{mod[1]}", {
                "self": obj
            }),
            "modifier": mod[3]
        })

        setattr(obj, mod[1], new_value)
    
    return angle, speed, type, position

def pt_modify_class_every(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks % mod[0] == 0:
        new_value = eval("original *FUNCTION* modifier".replace("*FUNCTION*", mod[2]), {
            "original": eval(f"self.{mod[1]}", {
                "self": obj
            }),
            "modifier": mod[3]
        })

        setattr(obj, mod[1], new_value)
    
    return angle, speed, type, position

def pt_stop_after(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks == mod[0]:
        obj.stopped.append(mod[1])

def pt_restart_after(angle, speed, type, position, ticks, obj: BulletSpawner, mod = []):
    if ticks == mod[0] and mod[1] in obj.stopped:
        obj.stopped.remove(mod[1])

def pt_follow(angle, speed, type, position, ticks, obj, mod = 1):
    target = player_position
    pos = pygame.Vector2(position)
    pos.move_towards_ip(target, mod)
    return angle, speed, type, pos

def pt_distance_scale(angle, speed, type, ticks, obj, position, mod = 1):
    target = player_position
    pos = pygame.Vector2(position)
    dist = pos.distance_to(target)
    mx = mod[0]
    mn = mod[1]
    dist = pygame.math.clamp(dist, 0, mx)
    dist = pygame.math.remap(0, mx, mn, mx, dist)
    return angle, dist, type, pos


def get_axis(positive, negative):
    return pygame.key.get_pressed()[positive] - pygame.key.get_pressed()[negative]

def spawn_circle(position, number, speed, angle_offset = 0, bulletType = Bullet):
    position = pygame.Vector2(position)
    global b_buffer
    angle_step = 360 / number
    for i in range(number):
        b_buffer.append(bulletType(
            position,
            (i * angle_step) + angle_offset,
            speed
        ))

def load_level(id):
    global bulletSpawners
    global time_limit
    bulletSpawners = []
    
    for i in levels[id]:
        pts = []

        for x in range(math.floor(len(i["preticks"]) / 2)):
            pts.append(pretick_types[i["preticks"][x * 2]])
            print(pretick_types[i["preticks"][x * 2]])
            pts.append(i["preticks"][(x * 2) + 1])
        
        print(pts)

        current = BulletSpawner(
            i["pos"],
            i["number"],
            bullet_types[i["type"]],
            i["angle"],
            i["velocity"],
            color=colors[i["type"]],
            preTick=pts,
            period=i["period"],
            activate_ticks=i["activate"],
            deactivate_ticks=i["deactivate"]
        )

        bulletSpawners.append(current)
    
    time_limit = level_data[id]["time"]
    pygame.mixer.music.load("music/" + level_data[id]["song"])
    pygame.mixer_music.play()

bullets = [
]

bulletSpawners = [
]

bullet_types = [
    Bullet,                          # 0
    BoomerangBullet,                 # 1
    GravityBullet,                   # 2
    FrictionBullet,                  # 3
    ClusterBullet,                   # 4
    RecursiveClusterBullet,          # 5
    EternalRecursiveClusterBullet    # 6
]

C_HALF = 0x80

colors = [
    pygame.Color(0, 0, 0),
    pygame.Color(0, 0, C_HALF),
    pygame.Color(0, C_HALF, C_HALF),
    pygame.Color(C_HALF, 0, C_HALF),
    pygame.Color(0, C_HALF, 0),
    pygame.Color(C_HALF, C_HALF, 0),
    pygame.Color(C_HALF, C_HALF, C_HALF)
]

pretick_types = [
    pt_none,               # 0
    pt_spin,               # 1
    pt_sway,               # 2
    pt_scale_speed,        # 3
    pt_sway_angle,         # 4
    pt_random_angle,       # 5
    pt_random_speed,       # 6
    pt_follow,             # 7
    pt_distance_scale,     # 8
    pt_modify_after,       # 9
    pt_modify_every,       # 10
    pt_modify_class_after, # 11
    pt_modify_class_every, # 12
]

player_rect = pygame.Rect(pygame.Vector2(player_position.x - 4, player_position.y - 4), pygame.Vector2(player_position.x + 4, player_position.y + 4))

ticks = 0

start_x = 0
time_limit = 0

font = pygame.Font("font.ttf", 32)
small_font = pygame.Font("font.ttf", 16)

def drawText(font, text, color, pos):
    s = font.render(text, True, color)
    window.blit(s, pos)

load_level(0)

while running:
    b_buffer = bullets.copy()

    for i in bullets:
        if i.cull(): b_buffer.remove(i)
    
    bullets = b_buffer.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
    
    player_velocity *= player_decel
    
    player_velocity.x += get_axis(pygame.K_RIGHT, pygame.K_LEFT) * player_accel
    player_velocity.y += get_axis(pygame.K_DOWN, pygame.K_UP) * player_accel

    player_velocity.clamp_magnitude_ip(max_speed)

    player_position.x = pygame.math.clamp(player_position.x, 0, 960)
    player_position.y = pygame.math.clamp(player_position.y, 0, 540)

    player_position += player_velocity

    b_buffer = bullets.copy()

    # if ticks % 5 == 0:
    #     offs = (ticks / 5) * 45
    #     spawn_circle((start_x, 200), 1, 0, offs, bulletType=RecursiveClusterBullet)

    for i in bulletSpawners:
        i.tick()

    for i in bullets:
        i.pre_tick()
        i.move()
        die = i.post_tick()

        if die == True:
            b_buffer.remove(i)
        
        if i.position.distance_to(player_position) <= player_diam + 2:
            b_buffer.remove(i)
            health -= 1
    
    bullets = b_buffer.copy()

    window.fill(bg_color)

    pygame.draw.circle(window, "#FF0000", player_position, player_diam * 2)

    for i in bullets:
        i.draw()
    
    for i in bulletSpawners:
        i.draw()
    
    # draw UI

    drawText(font, str(health), "#000000", (4, 4))
    drawText(small_font, str(round(clock.get_fps())), "#000000", (4, 4 + 32 + 4))
    drawText(small_font, str(len(bullets)), "#000000", (4, 4 + 32 + 16 + 4))

    pygame.display.update()

    clock.tick(target_fps)
    ticks += 1

    start_x += 1

pygame.quit()