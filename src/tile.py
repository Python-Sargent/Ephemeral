# python
#
# Multiplayer Networking Game
# 

from src.texture import load_texture
from src.texture import load_spriteobj
from pygame import Vector2
from src.object import Object
from src.object import HealthSpec
from src.sprite import Sprite
from src.log import log
from src.settings import Settings
from src.texture import Animation
from src.texture import anim_image
from os import path
from random import randint as r

class Tiles:
    empty = 0
    grassy = 1
    stony = 2
    sandy = 3
    snowy = 4
    icy = 5
    dirty = 6
    water = 7
    deep_water = 8 # 4 bit number
    tiles = ("empty", "grassy", "stony", "sandy", "snowy", "icy", "dirty", "water", "deep_water")
    default_anim_len = 2
    #anim_lengths = (1, 4, 1, 1, 1, 1, 1, 4, 4)
    anim_lengths = (1, 4, 1, 1, 1, 1, 1, 8, 8)
    #anim_delay = (0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.5)
    delay_spec = ([20*0.5], # empty
                  [20*1], #   grassy
                  [20*0.5], # stony
                  [20*0.5], # sandy
                  [20*0.5], # snowy
                  [20*0.5], # icy
                  [20*0.5], # dirty
                  [20*0.5, 20*0.3, 20*0.2, 20*0.3, 20*0.5, 20*0.3, 20*0.2, 20*0.3], # water
                  [20*0.5, 20*0.3, 20*0.2, 20*0.3, 20*0.5, 20*0.3, 20*0.2, 20*0.3]) # deep_water
    random_offset = (0, 3, 0, 0, 0, 0, 0, 0, 0)

#def load_tile_image(index, scale = 4):
#    return load_texture("tile_" + Tiles.tiles[index] + ".png", scale, True)[0]

#def load_tile_transition_image(index, transition):
#    return load_texture("tile_" + Tiles.tiles[index]+ "_" + transition + ".png", 4, True)[0]

def extend_list(len1, ilist, fill_value=None):
    if len(ilist) < len1: ilist.extend([fill_value] * (len1 - len(ilist)))
    return ilist

def load_tile_anim(index, anim_len = Tiles.default_anim_len):
    d = Tiles.delay_spec[index]
    d = extend_list(anim_len, d, d[-1])
    ro = Tiles.random_offset[index]
    offset = r(0, ro)

    return Animation("tile_" + Tiles.tiles[index], anim_len, d, Settings.tile_scale, offset)

def load_tile_transition_anim(index, transition, anim_len = Tiles.default_anim_len, offset = 0):
    d = Tiles.delay_spec[index]
    d = extend_list(anim_len, d, d[-1])
    return Animation("tile_" + Tiles.tiles[index] + "_" + transition, anim_len, d, Settings.tile_scale, offset)

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
        self.animation = load_tile_anim(index, Tiles.anim_lengths[index])
        self.transition = transition
        t_image = anim_image(self.animation)
        self.rect = t_image.get_rect()
        self.rect.center = pos
        if transition:
            self.animation2 = load_tile_transition_anim(index, transition.tile_type, Tiles.anim_lengths[index], self.animation.current)
            image2 = anim_image(self.animation2)
            self.rect2 = image2.get_rect()
            self.rect2.center = pos
    def image(self):
        image1 = anim_image(self.animation)
        if self.transition:
            image2 = anim_image(self.animation2)
            image1.blit(image2, self.rect2)
        return image1

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

"""def deserialize_tilemap(file):
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
    fullname = path.join("maps", "name)
    try:
        objects = deserialize_objectmap(open(fullname))
    except FileNotFoundError:
        print(f"Cannot load objectmap: {fullname}")
        raise SystemExit
    return objects"""

def deserialize_map(file):
    mode = "tmap"
    tmap = list([])
    objects = list([])
    for line in file:
        #print(line)
        if line == "tmap\n": mode = "tmap"; continue #   set deserialize mode for the next lines
        elif line == "omap\n": mode = "omap"; continue

        if mode == "tmap":
            tline = list([])
            for i in line:
                tline.append(i)
            tmap.append(tline)
        if mode == "omap":
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
            sprite = Sprite(load_texture(image_path))
            sprite.rect.center = Vector2(posx, posy)
            obj = Object(ttl, HealthSpec(invulnerable, maxhealth, health), collider_type, sprite)
            objects.append(obj)
    return (tmap, objects)

def loadMap(name):
    fullname = path.join("maps", "map_"+name+".txt")
    try:
        area_map = deserialize_map(open(fullname))
    except FileNotFoundError:
        print(f"Cannot load objectmap: {fullname}")
        raise SystemExit
    return area_map

def loadArea(name):
    area_map = loadMap(name)
    return Area(area_map[0], area_map[1])

def tilelist_from_area(area):
    tilemap = area.tilemap
    tiles = list([])
    tpositions = list([])
    tindices = list([])
    for i in range(len(tilemap)):
        tilerow = tilemap[i]
        for j in range(len(tilemap[i-1])):
            #tile = area.tilemap[i][j]
            tindices.append((i, j))
            tpositions.append(Vector2((j) * (16 * Settings.tile_scale) + (8 * Settings.tile_scale), (i) * (16 * Settings.tile_scale) + 8 * Settings.tile_scale))
        for v in tilerow:
            if v == "\n": tilerow.remove("\n")
            else: tiles.append(v)
            
    #tiles = [i for s in tilerows for i in s]
    tiles2 = list([])
    for i in range(len(tiles)):
        #print(len(tilemap)) # 18  len
        #print(len(tiles)) #   693 len
        #print(i) #            324 tile index
        #y = i // (len(tilemap) - 1)
        #print(y) #      18  row
        #x = i % (len(tilemap[y]) - 1)
        #print(x, "\n") #      00  column
        #self.tiles.append(tile.Tile(int(tiles[i]), tpositions[i], tile.generate_transition(tilemap, tindices[i][0], tindices[i][1])))
        tiles2.append(Tile(int(tiles[i]), tpositions[i]))
    return tiles2

def open_tmap_from_area(name):
    log("Opening area: " + str(name))
    area = loadArea(name)
    return tilelist_from_area(area)

def serialize_object(obj):
    output = ""
    output += str(obj.ttl) + " "
    output += str(obj.invulnerable) + " "
    output += str(obj.maxhealth) + " "
    output += str(obj.health) + " "
    output += str(obj.collider_type) + " "
    output += "monster_front.png" + " " # TODO: make this actually get the path of the image
    output += str(obj.rect[0]) + " "
    output += str(obj.rect[1]) + "\n"
    return output
    # ttl, invulnerable, maxhealth, health, collider_type, image_path, posx, posy

def save_area(name, area):
    #log("Saving area: " + str(name))
    tmap = area.tilemap
    strfile = "tmap\n"
    for i in range(len(tmap)):
        line = ""
        for j in range(len(tmap[i])):
            line += str(tmap[i][j])
        strfile += str(line) + "\n"
    if area.objects != None: # if there are objects in this area
        strfile += "omap"
        for obj in area.objects:
            strfile += str(serialize_object(obj))
    #print(strfile)
    filepath = path.join("maps", "map_" + name + ".txt")
    file = open(filepath, "w")
    file.write(strfile)
    file.close()
    #objects = area.objects


class TileRotations:
    NONE = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4
    rotations = (0, 0, 90, 180, 270)