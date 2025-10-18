import json
from entity import Entity
from player import Player
import pygame

def crop_tile(tileset, tile_position):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    surface.blit(tileset, (0, 0), pygame.Rect(pygame.Vector2(tile_position), (16, 16)))
    return surface

def parse_level(level_filename, tileset):
    with open(f"levels/{level_filename}.ldtk") as file:
        data = json.load(file)
    
    level = []
    player_pos = [0, 0]

    limits = pygame.Vector2(
        data["levels"][0]["pxWid"],
        data["levels"][0]["pxHei"]
    )
    
    for i in data["levels"][0]["layerInstances"][0]["gridTiles"]:
        tileID = i["src"]
        tilePos = i["px"]

        print(tileID)

        if tileID == [0, 48]: # P tile
            player_pos = tilePos
            continue

        sprite = crop_tile(tileset, tileID)

        tile = Entity(tilePos, (16, 16), sprite)

        level.append(tile)
    
    return [level, player_pos, limits]

if __name__ == "__main__":
    parse_level("level_1")