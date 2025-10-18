import json
import pygame
from textures import textures

class Tile:
    def __init__(self, position, texture):
        self.hitbox = pygame.Rect(position, (16, 16))
        self.texture = textures[texture]
        self.position = pygame.Vector2(position[0], position[1])
    
    def render(self, surface):
        surface.blit(self.texture, self.position)

def parse_level(name):
    path = f"levels/{name}.ldtk"

    with open(path) as file:
        data = json.load(file)
    
    tiles = data["levels"][0]["layerInstances"][0]["gridTiles"]
    actual_tiles = []

    for i in tiles:
        tile = Tile(i["px"], i["src"][0])
        actual_tiles.append(tile)
    
    return actual_tiles

if __name__ == "__main__":
    parse_level("level1")