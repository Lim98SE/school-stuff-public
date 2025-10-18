import pygame
import random

window = pygame.display.set_mode((800, 600))
tile_size = 16
map_size = pygame.Vector2(80, 80)

map_surface = pygame.Surface(round(map_size * 16))

directions = [
    pygame.Vector2(0, 1),
    pygame.Vector2(0, -1),
    pygame.Vector2(1, 0),
    pygame.Vector2(-1, 0),
]

tile_metadata = {
    0: {
        "frames": 4,
        "coords": pygame.Vector2(0, 0)
    },
    1: {
        "frames": 4,
        "coords": pygame.Vector2(1, 0)
    },
    2: {
        "frames": 1,
        "coords": pygame.Vector2(2, 0)
    }
}

frame_advance_counter = 0

walker_dir = random.choice(directions)
steps_until_change = 1

walker_pos = round(map_size / 2)
player_pos = walker_pos.copy() * tile_size

map = []
for y in range(int(map_size.y)):
    map.append([])

    for x in range(int(map_size.x)):
        map[y].append(random.randint(0, 1))

def step():
    global walker_dir
    global walker_pos
    global steps_until_change
    global map

    steps_until_change -= 1

    if steps_until_change == 0:
        walker_dir = random.choice(directions)
        steps_until_change = random.randint(1, 3)

    walker_pos += walker_dir
    walker_pos.x = walker_pos.x % map_size.x
    walker_pos.y = walker_pos.y % map_size.y

    map[int(walker_pos.y)][int(walker_pos.x)] = 2

for i in range(random.randint(2000, 10000)):
    step()

def get_tile(tileset: pygame.Surface, tile_id):
    md = tile_metadata[tile_id]
    coords = md["coords"] * 16
    frame = (current_anim_frame % md["frames"])
    coords.y += (frame * 16)

    return tileset.subsurface(coords, [tile_size] * 2)

def draw_map():
    X, Y = 0, 0
    global camera_pos
    global cam_rect
    for y in map:
        for x in y:
            coords = pygame.Vector2(X, Y) * tile_size
            coords -= camera_pos

            if coords.x < -64 or coords.x > window.get_width() + 64: continue

            tile = get_tile(tileset, x)
            map_surface.blit(tile, coords)
            X += 1
        
        X = 0
        Y += 1

tileset = pygame.image.load("tileset.png")

running = True
clock = pygame.time.Clock()

current_anim_frame = 0

camera_pos = pygame.Vector2((0, 0))
camera_zoom = 1
cam_rect = pygame.Rect(camera_pos, window.get_size())

def get_axis(positive, negative):
    return int(pygame.key.get_pressed()[positive]) - int(pygame.key.get_pressed()[negative])

def get_vector(up, down, left, right):
    v_axis = get_axis(down, up)
    h_axis = get_axis(right, left)

    return pygame.Vector2(h_axis, v_axis)

while running:
    pygame.display.set_caption(f"FPS: {round(clock.get_fps())}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))

    camera_pos += get_vector(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT) * 8

    camera_pos.x = pygame.math.clamp(camera_pos.x, 0, (map_size.x * 16) - window.get_width())
    camera_pos.y = pygame.math.clamp(camera_pos.y, 0, (map_size.y * 16) - window.get_height())
    cam_rect = pygame.Rect(camera_pos, window.get_size())
    camera_zoom = pygame.math.clamp(camera_zoom, 1, 10)
    draw_map()
    map_surface_toblit = map_surface.subsurface((0, 0), window.get_size())
    window.blit(map_surface_toblit)
    pygame.display.flip()

    clock.tick(60)
    frame_advance_counter -= 1

    if frame_advance_counter <= 0:
        frame_advance_counter = 4
        current_anim_frame += 1

pygame.quit()