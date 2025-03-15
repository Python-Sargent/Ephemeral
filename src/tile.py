# python
#
# Multiplayer Networking Game
# 

from src.texture import load_texture
from pygame import Vector2
from src.object import Object
from src.object import HealthSpec
from src.sprite import Sprite
from os import path

class Tiles:
    empty = 0
    grassy = 1
    stony = 2
    sandy = 3
    snowy = 4
    icy = 5
    dirty = 6
    water = 7
    deep_water = 8
    tiles = ("empty", "grassy", "stony", "sandy", "snowy", "icy", "dirty", "water", "deep_water")

def load_tile_image(index):
    return load_texture("tile_" + Tiles.tiles[index] + ".png", 4, True)[0]

def load_tile_transition_image(index, transition):
    return load_texture("tile_" + Tiles.tiles[index]+ "_" + transition + ".png", 4, True)[0]

class TileMap:
    def __init__(self, tiles):
        self.tiles = tiles
        self.types = set(self.tiles) # create a set of all types in the TileMap

class Area:
    def __init__(self, tilemap, objects):
        self.tilemap = tilemap
        self.objects = objects

class TileTransition:
    def __init__(self, tile_type, rotation):
        self.tile_type = tile_type
        self.rotation = rotation

class Tile:
    def __init__(self, index, pos, transition = None):
        self.tile = index
        image = load_tile_image(index)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = pos
        if transition:
            image2 = load_tile_transition_image(index, transition.tile_type) # for transitional tiles
            rect2 = image.get_rect()
            rect2.center = pos
            self.image.blit(image2, rect2)

def get_3x3(input_list, y, x):
    num_rows_input = len(input_list)
    if num_rows_input == 0 or type(input_list) != type(list()) :
        return []  # Handle empty input

    num_cols_input_first_row = len(input_list[0]) if num_rows_input > 0 else 0

    start_row = max(-1, (y - 2))  # Calculate starting row index
    start_col = max(-1, (x - 2)) # Calculate starting col index

    cropped_list = []
    for i in range(3):
        row = []
        for j in range(3):
            row_index = start_row + i
            col_index = start_col + j

            if 0 <= row_index < num_rows_input and 0 <= col_index < num_cols_input_first_row:
                row.append(input_list[row_index][col_index])
            else:
                # Handle cases where center crop goes out of bounds
                # For now, we'll just skip if out of bounds
                pass

        if row: # Only append rows that have elements (handle cases where center is partially out of bounds)
            cropped_list.append(row)

    return cropped_list

def get_index_offset(v):
    ioffset = [
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (1, 1)]
    ]

    if v == 1:
        return ioffset[0][1] # North
    elif v == 2:
        return ioffset[1][0] # West
    elif v == 3:
        return ioffset[2][1] # South
    elif v == 4:
        return ioffset[1][2] # East

def generate_transition(tlist, y, x):
    if tlist[y][x] == 0: return None # 0 (Empty) tile does not have any transition at this time
    border_list = get_3x3(tlist, y, x)
    #if len(border_list) - 1 <= offset[0]:

    for v in range(len(border_list)):
        offset = get_index_offset(v)
        for h in range(len(border_list[v])):
            pass
    transition = TileTransition("corner", 1)
    return transition

def deserialize_tilemap(file):
    tmap = list([])
    for line in file:
        tline = list([])
        for i in line:
            tline.append(i)
        tmap.append(tline)
    return tmap

def deserialize_objectmap(file):
    objects = list([])
    for line in file:
        line = line.replace('\n', "") # remove the tailing newline charactor (not the best way?)
        oline = line.split(" ") #example of a line:
        # -1 0 100 100 collider monster_front.png 0 0
        # ttl, invulnerable, maxhealth, health, collider_type, image_path, posx, posy
        ttl = int(oline[0])
        invulnerable = int(oline[1])
        maxhealth = int(oline[2])
        health = int(oline[3])
        collider_type = oline[4]
        image_path = oline[5]
        posx = int(oline[6])
        posy = int(oline[7])
        sprite = Sprite.spriteobj_to_sprite(Sprite, load_texture(image_path))
        sprite.rect.center = Vector2(posx, posy)
        obj = Object(ttl, HealthSpec(invulnerable, maxhealth, health), collider_type, sprite)
        objects.append(obj)
    return objects


def loadTileMap(filename):
    fullname = path.join("maps", filename)
    try:
        tilemap = deserialize_tilemap(open(fullname))
    except FileNotFoundError:
        print(f"Cannot load tilemap: {fullname}")
        raise SystemExit
    return tilemap

def loadObjectMap(name):
    fullname = path.join("maps", name)
    try:
        objects = deserialize_objectmap(open(fullname))
    except FileNotFoundError:
        print(f"Cannot load objectmap: {fullname}")
        raise SystemExit
    return objects

def loadArea(name):
    tilemap = loadTileMap("tilemap_" + name + ".txt")
    objects = loadObjectMap("objectmap_" + name + ".txt")
    return Area(tilemap, objects)

class TileRotations:
    NONE = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4
    rotations = (0, 0, 90, 180, 270)