# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import os
from random import randint
from time import sleep as s

pygame.init()

pygame.mixer.init()

if pygame.mixer.get_init():
    print("pygame.mixer initialized")
else:
    raise ValueError("Missing module 'pygame.mixer'")

def load_texture(name, scale = False, use_convert = False):
    fullname = os.path.join("textures", name)
    try:
        image = pygame.image.load(fullname)
        if use_convert != False:
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    if scale != False:
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pygame.transform.scale(image, size)
    return image, image.get_rect()

class DisplayParams:
    size = width, height = 1920, 1080
    title = "Ephemeral - Main Menu"
    fill_color = 20, 20, 20
    icon = load_texture("icon.png", False, False)[0]
    class Sizes:
        scalar = 60
        class Heading:
            h1 = 64
            h2 = 56
            h3 = 48
            sub = 16
            tiny = 8
        fontsize = 32
    center = [0, 0]

DisplayParams.center = (DisplayParams.size[0] / 2, DisplayParams.size[1] / 2)

screen = pygame.display.set_mode(DisplayParams.size)
pygame.display.set_caption(DisplayParams.title)
pygame.display.set_icon(DisplayParams.icon)

class Textures:
    def player(img_name):
        return load_texture("player_" + img_name + ".png", Game.settings.player_scale, True)
    def monster(img_name):
        return load_texture("monster_" + img_name + ".png", Game.settings.monster_scale, True)

"""
Traceback (most recent call last):
  File "/home/user/Github/Project/client.py", line 208, in <module>
    player_image = load_texture("player_front.png", Game.settings.player_scale)
  File "/home/user/Github/Project/client.py", line 35, in load_texture
    image = pygame.transform.scale(image, size)
pygame.error: Surfaces must not be locked during blit
"""

clock = pygame.time.Clock()

class Colors:
    red = 255, 0, 0
    orange = 175, 80, 0
    yellow = 200, 200, 5
    green = 0, 255, 0
    cyan = 5, 125, 125
    blue = 0, 0, 255
    purple = 125, 5, 125
    black = 0, 0, 0
    white = 255, 255, 255
    darkgrey = 80, 80, 80
    darkgrey2 = 60, 60, 70

Font = pygame.font.Font

volume = 0.5

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
    return load_texture("tile_" + Tiles.tiles[index] + ".png", Game.settings.tile_scale, True)[0]

def load_tile_transition_image(index, transition):
    return load_texture("tile_" + Tiles.tiles[index]+ "_" + transition + ".png", Game.settings.tile_scale, True)[0]

class TileMap:
    def __init__(self, tiles):
        self.tiles = tiles
        self.types = set(self.tiles) # create a set of all types in the TileMap

class Area:
    def __init__(self, tilemap, objects):
        self.tilemap = tilemap
        self.objects = objects

class Scene:
    class Menu:
        music = False
    class Game:
        areas = list([])

class TileTransition:
    def __init__(self, tile_type, rotation):
        self.tile_type = tile_type
        self.rotation = rotation

class Tile:
    def __init__(self, index, pos, transition = None):
        self.tile = index
        image = load_tile_image(index)
        self.image1 = image
        self.rect = image.get_rect()
        self.rect.center = pos
        if transition:
            self.image2 = load_tile_transition_image(index, transition.tile_type) # for transitional tiles
            self.rect2 = image.get_rect()
            self.rect2.center = pos

def get_3x3(input_list, index1, index2):
    """
    Crops a 2D list to a 3x3 pattern from the center if possible.
    If the input is smaller than 3x3 in either dimension, it will return as much as possible from the center-ish.
    """
    num_rows_input = len(input_list)
    if num_rows_input == 0 or type(input_list) != type(list()) :
        return []  # Handle empty input

    num_cols_input_first_row = len(input_list[0]) if num_rows_input > 0 else 0

    start_row = max(-1, (index1 - 2))  # Calculate starting row index
    start_col = max(-1, (index2 - 2)) # Calculate starting col index

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

def get_index_offset(dir):
    ioffset = [
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (1, 1)]
    ]
    if dir == 1:
        return ioffset[0][1]
    elif dir == 2:
        return ioffset[1][0]
    elif dir == 3:
        return ioffset[2][1]
    elif dir == 4:
        return ioffset[1][2]
    """
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4
    """

def generate_transition(tlist, index1, index2):
    border_list = get_3x3(tlist, index1, index2)
    dir = randint(1, 4) # follow the TileRotations layout
    offset = get_index_offset(dir)
    #if len(border_list) - 1 <= offset[0]:

    #for v in range(len(border_list)):
    #    for h in range(len(border_list[v])):
    #        pass
    transition = TileTransition()
    return transition

def deserialize_tilemap(file):
    tmap = list([])
    for line in file:
        tline = list([])
        for i in range(len(line)):
            tline.append(line[i])
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
    fullname = os.path.join("maps", filename)
    try:
        tilemap = deserialize_tilemap(open(fullname))
    except FileNotFoundError:
        print(f"Cannot load tilemap: {fullname}")
        raise SystemExit
    return tilemap

def loadObjectMap(name):
    fullname = os.path.join("maps", name)
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

class HealthSpec:
    def __init__(self, invulnerable = False, maxhealth = 100, health = 100, damage_group = "none"):
        if invulnerable == False:
            self.maxhealth = maxhealth
            self.health = health
        self.invulnerable = invulnerable
        self.damage_group = damage_group

class TileRotations:
    NONE = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4
    rotations = (0, 0, 90, 180, 270)

class Game:
    class settings: # overwritten with server settings during multiplayer
        fps = 60
        maxhealth = 100
        player_hspec = HealthSpec(False, 100, 100, "friendly_player")
        player_scale = 4
        monster_scale = 4
        tile_scale = 4
        player_speed = 7
        drag = 1
    objects = False # set to False as there are no objects yet
    tiles = False
    players = False
    active_area = False,
    scene = 0 # 0 is menu, 1 = game, 2 = settings
    game_scene = 0 # for the current scene inside the game
    local_player = None
    is_playing = False
    def get_sprites(self):
        sprites = []
        if self.tiles != False:
            for i in range(len(self.tiles)):
                sprites.append(Sprite(self.tiles[i].image1, self.tiles[i].rect))
        for i in range(len(self.objects)):
            sprites.append(self.objects[i].sprite)
        return sprites
    def open_area(self, name):
        area = loadArea(name)
        tiles = list([])
        tpositions = list([])
        for i in range(len(area.tilemap)):
            tilerow = area.tilemap[i]
            for j in range(len(area.tilemap[i])):
                #tile = area.tilemap[i][j]
                tpositions.append(Vector2(j * (16 * Game.settings.tile_scale) + (8 * Game.settings.tile_scale), i * (16 * Game.settings.tile_scale) + 8 * Game.settings.tile_scale))
            for v in tilerow:
                if v == "\n": tilerow.remove("\n")
                del v
            for v in tilerow:
                tiles.append(v)
        #tiles = [i for s in tilerows for i in s]
        self.tiles = list([])
        for i in range(len(tiles)):
            self.tiles.append(Tile(int(tiles[i]), tpositions[i]))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, rect, z_index = 0):
        self.rect = rect
        self.image = image
        self.z_index = z_index

    #def update(self):

    def spriteobj_to_sprite(self, spriteobj, z_index = 0):
        return self(spriteobj[0], spriteobj[1], z_index)
    
    def is_sprite(self):
        return True

#player_image = load_texture("player_front.png", Game.settings.player_scale) # init the player sprite as the front facing texture

class Object:
    def __init__(self, ttl, hspec, collider_type = "collider", sprite = False): # TTL is Time To Live
        if sprite != False:
            if sprite.is_sprite():
                self.sprite = sprite
            else:
                self.rect = sprite
                self.sprite = False
        self.max_health = hspec.maxhealth
        self.health = hspec.health
        self.invulnerable = hspec.invulnerable
        self.damage_group = hspec.damage_group
        self.ttl = ttl
        self.lifetime = 0
        self.collider_type = collider_type # collider, trigger, none
        self.alive = True
    
    def remove(self):
        self.sprite = False
        self.rect = False
        self.health = 0
        self.max_health = 0
        self.alive = False
    
    def duplicate(self):
        return self(self.ttl, HealthSpec(self.invulnerable, self.max_health, self.health, self.damage_group), self.sprite)

class Effect: # effects: value * multiplier + blessing - curse
    def __init__(self, name, tick):
        self.name = name
        self.tick = tick

class Multiplier(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect

class Blessing(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect

class Curse(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect

class Player(Object):
    def __init__(self, sprite):
        super().__init__(-1, Game.settings.player_hspec, "collider", sprite) 
        self.pos = sprite.rect.center
    textures = ["back", "left", "front", "right"]
    velocity = Vector2(0, 0)
    effects = list([])
    def set_pos(self, vec2):
        self.sprite.rect.center = vec2
    def get_pos(self):
        return self.sprite.rect.center
    def set_texture(self, texture):
        self.sprite.image = texture
    def set_animation(self, animation_index):
        self.sprite.image = Textures.player(self.textures[animation_index])[0]

    def animate_move(self, pos, delta):
        if pos[0] < delta[0]:
            self.set_animation(3)
        elif pos[0] > delta[0]:
            self.set_animation(1)
        if pos[1] < delta[1]:
            if pos[0] < delta[0]:
                self.set_animation(3)
            elif pos[0] > delta[0]:
                self.set_animation(1)
            else:
                self.set_animation(2)
        elif pos[1] > delta[1]:
            self.set_animation(0)
    def apply_drag(self):
        if self.velocity[0] < 0:
            self.velocity[0] += Game.settings.drag
        elif self.velocity[0] > 0:
            self.velocity[0] -= Game.settings.drag
        if self.velocity[1] < 0:
            self.velocity[1] += Game.settings.drag
        elif self.velocity[1] > 0:
            self.velocity[1] -= Game.settings.drag
    def move(self, vec2):
        self.animate_move(self.sprite.rect.center, self.sprite.rect.center + vec2)
        self.velocity = Vector2(max(min(self.velocity[0] + vec2[0], Game.settings.player_speed), -Game.settings.player_speed), max(min(self.velocity[1] + vec2[1], Game.settings.player_speed), -Game.settings.player_speed))
    def update(self):
        self.apply_drag()
        self.sprite.rect.center += self.velocity



class Monster(Object):
    def __init__(self, sprite, hspec, agression):
        super().__init__(60000, hspec, "collider", sprite) 
        self.pos = sprite.rect.center
        self.agression = agression # passive, agressive, passive_agressive, triggered
    def set_pos(self, vec2):
        self.sprite.rect.center = vec2
    def get_pos(self):
        return self.sprite.rect.center
    def set_texture(self, texture):
        self.sprite.image = texture
    def set_animation(self, animation_index):
        self.sprite.image = Textures.player(self.textures[animation_index])[0]

    def animate_move(self, pos, delta):
        if pos[0] < delta[0]:
            self.set_animation(3)
        elif pos[0] > delta[0]:
            self.set_animation(1)
        if pos[1] < delta[1]:
            if pos[0] < delta[0]:
                self.set_animation(3)
            elif pos[0] > delta[0]:
                self.set_animation(1)
            else:
                self.set_animation(2)
        elif pos[1] > delta[1]:
            self.set_animation(0)
    def apply_drag(self):
        if self.velocity[0] < 0:
            self.velocity[0] += Game.settings.drag
        elif self.velocity[0] > 0:
            self.velocity[0] -= Game.settings.drag
        if self.velocity[1] < 0:
            self.velocity[1] += Game.settings.drag
        elif self.velocity[1] > 0:
            self.velocity[1] -= Game.settings.drag
    def move(self, vec2):
        self.animate_move(self.sprite.rect.center, self.sprite.rect.center + vec2)
        self.velocity = Vector2(max(min(self.velocity[0] + vec2[0], Game.settings.monster_speed), -Game.settings.monster_speed), max(min(self.velocity[1] + vec2[1], Game.settings.monster_speed), -Game.settings.monster_speed))
    def update(self):
        self.apply_drag()
        self.sprite.rect.center += self.velocity

# ClientSide

class Particle:
    def __init__(self, ttl, sprite = False): # TTL is Time To Live
        if sprite != False:
            if sprite.is_sprite():
                self.sprite = sprite
            else:
                self.rect = sprite
                self.sprite = False
        self.ttl = ttl
        self.lifetime = 0
    
    def remove(self):
        self.sprite = False
        self.rect = False
        self.alive = False
    
    def duplicate(self):
        return self(self.ttl, HealthSpec(self.invulnerable, self.max_health, self.health, self.damage_group), self.sprite)

class LocalPlayer(Player):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.maxhealth = Game.settings.maxhealth
        self.health = self.maxhealth

def create_text(text, pos, size = DisplayParams.Sizes.fontsize, color = Colors.white):
    font = Font(None, size)
    image = font.render(text, False, color)
    rect = image.get_rect()
    rect.center = (pos.x, pos.y)
    return (image, rect) # returns a spriteobj

#def Spriteobj(image, rect): # condense an image and rect into a spriteobj
#    return (image, rect)

screen.fill(Colors.darkgrey)
textobj = create_text("Connecting to Server...", Vector2(DisplayParams.center[0], DisplayParams.center[1]), 48)
text_sprite = Sprite.spriteobj_to_sprite(Sprite, textobj)
screen.blit(text_sprite.image, text_sprite.rect)
pygame.display.flip()
clock = pygame.time.Clock()
s(1) # fake the wait for connect

def draw_frame(sprites):
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    

def draw_window(sprites = False):
    if sprites == False:
        screen.fill(DisplayParams.fill_color)
    else:
        screen.fill(DisplayParams.fill_color)
        draw_frame(sprites)
    pygame.display.flip()

def update_caption(caption):
    pygame.display.set_caption(caption)

def EmptyFunction():
    pass

class Action:
    def __init__(self, func, func2 = EmptyFunction):
        self.func = func
        self.func2 = func2
    def run(self):
        self.func()
    def run2(self):
        self.func2()

class Keybind:
    def __init__(self, name, action):
        self.name = name
        self.action = action
    def press(self):
        self.action.run(self.action)
    def unpress(self):
        self.action.run2(self.action)


class Keys:
    class keys:
        KEY_FORWARD = "W"
        KEY_LEFT = "A"
        KEY_DOWN = "S"
        KEY_RIGHT = "D"
        #KEY_JUMP = pygame.Key.SPACE
    keybinds = list([])
    def processPressed(self, keys):
        self.pressed = keys
    def keydown(self, keys):
        for i in range(len(keys)):
            self.keybinds[keys[i]].press()
    def keyup(self, keys):
        for i in range(len(keys)):
            self.keybinds[keys[i]].unpress()

def removeDeadObjects(objects):
    for i in range(len(objects)):
        obj = objects[i]
        if obj.health <= 0:
            objects.pop(i)
    return objects

def main():

    should_continue = True

    # temporarily just add a player and monster sprite to the list
    Game.local_player = LocalPlayer(Sprite.spriteobj_to_sprite(Sprite, Textures.player("front"), 0))
    monster = Monster(Sprite.spriteobj_to_sprite(Sprite, Textures.monster("front"), 0), HealthSpec(False, 100, 100, "monster"), "passive")
    Game.objects = list([Game.local_player, monster])
    Game.open_area(Game, "test")

    dtime = 0

    while should_continue is True:
        dtime = clock.tick(Game.settings.fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_continue = False
            #elif event.type == pygame.KEYDOWN:
        #Keys.processPressed(Keys, pygame.key.get_pressed())
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            Game.local_player.move(Vector2(0, -10))
        elif keys[pygame.K_s]:
            Game.local_player.move(Vector2(0, 10))
        if keys[pygame.K_a]:
            Game.local_player.move(Vector2(-10, 0))
        elif keys[pygame.K_d]:
            Game.local_player.move(Vector2(10, 0))
        Game.local_player.update() # should implement dtime at some point

        draw_window(Game.get_sprites(Game))

    pygame.quit()

main()


"""
def load_png(name):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()
"""