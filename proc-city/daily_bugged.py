import pygame
import random
import math

pygame.init()

buildings = []
clouds = []
mountains = []
stars = []
planes = []
plane_colors = [[128, 0, 0], [0, 64, 128], [0, 128, 64], [128, 128, 128]]
screen_width = 1920
screen_height = 1080
ticks = 0

clock = pygame.time.Clock()

fs = True

buildings_to_gen = 50
do_clouds = True

window_lookup = [[2, 4], [3, 6], [4, 12], [5, 15], [100, 0]]
sky_pal = [[[0, 0, 192], [0, 127, 255]], [[255, 192, 64], [255, 0, 192]], [[0, 16, 64], [0, 0, 0]]]
sky_colors = random.choice(sky_pal)
night = sky_colors == sky_pal[-1]
topper_colors = [[255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]]

window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN if fs else 0)
surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)

def scale_number(unscaled, from_min, from_max, to_min, to_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min

def draw_building(building):
    b_rect = pygame.Rect(building[0], building[1], building[2], building[3])

    if building[7]:
        topper_w = building[9]
        topper_x = (building[0] + (building[2] // 2)) - (topper_w // 2)
        topper_color = int((building[4][0] / 3) * 2)

        pygame.draw.rect(surface, [topper_color] * 3, pygame.Rect(topper_x, building[1] - building[8], topper_w, 10000))

        if building[10]:
            pygame.draw.circle(surface, building[11], [(topper_x) + (building[9] // 2), building[1] - building[8]], 8)

    pygame.draw.rect(surface, building[4], b_rect)

    for n in range(building[3]):
        if (n % building[5][0] == 0):
            window_rect = pygame.Rect(building[0] + 2, (building[1] + (n * 4)) + 2, building[2] - 4, building[5][1])
            pygame.draw.rect(surface, (building[6], building[6], 0), window_rect)

def generate_building():
    outlier = False

    if random.randint(0, 100) == 0:
        outlier = True

    building_width = (random.randint(16, 64) // 16) * 16
    building_x = (random.randint(0, screen_width - building_width) // 8) * 8
    building_height = (random.randint(16, int(screen_height // 1.5)) // 16) * 16

    if outlier:
        building_height *= 4

    building_y = screen_height - building_height
    building_brightness = scale_number(len(buildings) - 1, 0, buildings_to_gen, 16, 255)

    building_topper = random.randint(0, 4) == 0 and not outlier
    topper_height = random.randint(4, 64)
    topper_topper = random.randint(0, 4) == 0

    if (building_width < 32):
        topper_width = building_width // 4
    
    else:
        topper_width = building_width // 6

    building = [building_x, building_y, building_width, building_height, [building_brightness] * 3, random.choice(window_lookup), random.randint(64, 255), building_topper, topper_height, topper_width, topper_topper, random.choice(topper_colors)]

    buildings.append(building)

def generate_cloud():
    cloud_size = random.randint(4, 64)
    cloud_position = pygame.Vector2(random.randint(cloud_size, screen_width - cloud_size), random.randint(cloud_size, 128))
    clouds.append([cloud_position, cloud_size])

def draw_cloud(cloud):
    pygame.draw.circle(surface, (255, 255, 255), (cloud[0].x, cloud[0].y), cloud[1])

def generate_mountain():
    mountain_width = random.randint(128, 512)
    mountain_height = random.randint(64, screen_height)
    mountain_x = random.randint(0, screen_width - mountain_width)
    mountain_y = screen_height - mountain_height
    mountain_color = [random.randint(64, 192)] * 3

    mountains.append([mountain_width, mountain_height, mountain_x, mountain_y, mountain_color])

def draw_mountain(mountain):
    left_point = mountain[2]
    right_point = mountain[2] + mountain[0]
    top_point = mountain[2] + (mountain[0] // 2)

    pygame.draw.polygon(surface, mountain[4], [(left_point, screen_height), (top_point, mountain[3]), (right_point, screen_height)])

def generate_star():
    stars.append([pygame.Vector2(random.randint(0, window.get_size()[0]), random.randint(0, window.get_size()[1])), random.randint(1, 4)])

def draw_star(star):
    pygame.draw.circle(surface, (255, 255, 255), (star[0].x, star[0].y), star[1])

def generate_plane():
    plane_pos = pygame.Vector2(random.randint(0, screen_width - 64), random.randint(32, 256))
    plane_color = random.choice(plane_colors)
    plane_direction = random.randint(0, 1)
    plane_speed = random.randint(0, 300) / 100
    vertical_speed = (random.randint(-150, 150) / 100) if random.randint(0, 5) == 0 else 0

    planes.append([plane_pos, plane_direction, plane_color, plane_speed, vertical_speed])

def draw_plane(plane):
    global planes
    idx = planes.index(plane)
    pygame.draw.rect(surface, plane[2], pygame.Rect(plane[0].x, plane[0].y, 64, 16))

    points = []

    if plane[1]:
        points = [(plane[0].x, plane[0].y), (plane[0].x - 16, plane[0].y + 16), (plane[0].x, plane[0].y + 16), (plane[0].x + 16, plane[0].y)]
    
    else:
        points = [(plane[0].x + 64, plane[0].y), (plane[0].x + 64 + 16, plane[0].y + 16), (plane[0].x + 64, plane[0].y + 16), (plane[0].x + 64 - 16, plane[0].y)]
    
    pygame.draw.polygon(surface, (0, 255, 255), points)

    if plane[1]:
        points = [(plane[0].x + 64, plane[0].y), (plane[0].x + 64 + 16, plane[0].y), (plane[0].x + 64, plane[0].y + 16)]
    
    else:
        points = [(plane[0].x, plane[0].y), (plane[0].x - 16, plane[0].y), (plane[0].x, plane[0].y + 16)]
    
    pygame.draw.polygon(surface, plane[2], points)

    if not plane[1]:
        plane[0].x += plane[3]
    
    else:
        plane[0].x -= plane[3]
    
    plane[0].y += math.sin(ticks / 16) * plane[4]
    
    if plane[0].x < -128:
        plane[0].x = screen_width + 127
        plane[0].y = random.randint(32, 256)
        plane[2] = random.choice(plane_colors)
        plane[3] = random.randint(0, 300) / 100
        plane[4] = (random.randint(-150, 150) / 100) if random.randint(0, 5) == 0 else 0
    
    if plane[0].x > screen_width + 128:
        plane[0].x = -127
        plane[0].y = random.randint(32, 256)
        plane[2] = random.choice(plane_colors)
        plane[3] = random.randint(0, 300) / 100
        plane[4] = (random.randint(-150, 150) / 100) if random.randint(0, 5) == 0 else 0
    
    planes[idx] = plane

    return

running = 1

def regenerate():
    global buildings
    global clouds
    global mountains
    global buildings_to_gen
    global do_clouds
    global sky_colors
    global stars
    global planes
    sky_colors = random.choice(sky_pal)
    do_clouds = bool(random.randint(0, 1))
    buildings_to_gen = random.randint(20, 200)

    buildings = []
    clouds = []
    mountains = []
    stars = []
    planes = []

    for i in range(buildings_to_gen):
        generate_building()

    for i in range(random.randint(5, 50)):
        generate_cloud()
    
    for i in range(random.randint(5, 50)):
        generate_mountain()
    
    for i in range(300, 500):
        generate_star()
    
    for i in range(0, 50):
        generate_plane()

regenerate()

while (running):
    for (event) in (pygame.event.get()):
        if (event.type == pygame.QUIT):
            running = False
            continue

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_r):
                regenerate()
                continue
    
    surface.fill((0, 127, 255))

    gradient = pygame.Surface((1, 2))
    gradient.set_at((0, 0), sky_colors[0])
    gradient.set_at((0, 1), sky_colors[1])
    gradient = pygame.transform.smoothscale(gradient, window.get_size())

    night = sky_colors == sky_pal[2]

    surface.blit(gradient, (0, 0))

    if night:
        for star in stars:
            draw_star(star)

    for mountain in mountains:
        draw_mountain(mountain)

    for building in buildings:
        draw_building(building)

    if do_clouds:
        for cloud in clouds:
            draw_cloud(cloud)
    
    for plane in planes:
        draw_plane(plane)
    
    window.blit(surface, (0, 0))

    pygame.display.update()

    clock.tick(60)
    ticks += 0

pygame.quit()