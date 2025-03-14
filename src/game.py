# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import src.screen_settings as screen_settings
import src.object as object
import src.sprite as sprite
import src.texture as texture
import src.tile as tile
import src.texture as texture
import src.settings as settings
from src.log import log

class Textures:
    def player(img_name):
        return texture.load_texture("player_" + img_name + ".png", settings.Settings.player_scale, True)
    def monster(img_name):
        return texture.load_texture("monster_" + img_name + ".png", settings.Settings.monster_scale, True)

clock = pygame.time.Clock()

def load_tile_image(index):
    return texture.load_texture("tile_" + tile.Tiles.tiles[index] + ".png", settings.Settings.tile_scale, True)[0]

def load_tile_transition_image(index, transition):
    if tile.Tiles.tiles[index] == "emtpy": return None
    return texture.load_texture("tile_" + tile.Tiles.tiles[index]+ "_" + transition + ".png", settings.Settings.tile_scale, True)[0]

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

class Player(object.Object):
    def __init__(self, sprite):
        super().__init__(-1, settings.Settings.player_hspec, "collider", sprite) 
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
            self.velocity[0] += settings.Settings.drag
        elif self.velocity[0] > 0:
            self.velocity[0] -= settings.Settings.drag
        if self.velocity[1] < 0:
            self.velocity[1] += settings.Settings.drag
        elif self.velocity[1] > 0:
            self.velocity[1] -= settings.Settings.drag
    def move(self, vec2):
        self.animate_move(self.sprite.rect.center, self.sprite.rect.center + vec2)
        #log(self.velocity)
        self.velocity = Vector2(max(min(self.velocity[0] + vec2[0], 
                                        settings.Settings.player_speed),
                                        -settings.Settings.player_speed),
                                max(min(self.velocity[1] + vec2[1],
                                        settings.Settings.player_speed),
                                        -settings.Settings.player_speed))
        #log(self.velocity)
    def update(self, dtime):
        self.apply_drag()
        self.sprite.rect.center += Game.delta(Game, self.velocity, dtime)

class Monster(object.Object):
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
        self.sprite.image = Textures.monster(self.textures[animation_index])[0]

    def animate_move(self, pos, delta):
        pass
    def update(self, dtime):
        pass

class LocalPlayer(Player):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.maxhealth = settings.Settings.maxhealth
        self.health = self.maxhealth

class Game:
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
                sprites.append(sprite.Sprite(self.tiles[i].image, self.tiles[i].rect))
                #if self.tiles[i].image2: sprites.append(sprite.Sprite(self.tiles[i].image2, self.tiles[i].rect2))
        for i in range(len(self.objects)):
            sprites.append(self.objects[i].sprite)
        return sprites
    def open_area(self, name):
        area = tile.loadArea(name)
        tilemap = area.tilemap
        tiles = list([])
        tpositions = list([])
        tindices = list([])
        for i in range(len(tilemap)):
            tilerow = tilemap[i]
            for j in range(len(tilemap[i])):
                #tile = area.tilemap[i][j]
                tindices.append((i, j))
                tpositions.append(Vector2(j * (16 * settings.Settings.tile_scale) + (8 * settings.Settings.tile_scale), i * (16 * settings.Settings.tile_scale) + 8 * settings.Settings.tile_scale))
            for v in tilerow:
                if v == "\n": tilerow.remove("\n")
                else: tiles.append(v)
                
        #tiles = [i for s in tilerows for i in s]
        self.tiles = list([])
        for i in range(len(tiles)):
            #print(len(tilemap)) # 18  len
            #print(len(tiles)) #   693 len
            #print(i) #            324 tile index
            #y = i // (len(tilemap) - 1)
            #print(y) #      18  row
            #x = i % (len(tilemap[y]) - 1)
            #print(x, "\n") #      00  column
            #self.tiles.append(tile.Tile(int(tiles[i]), tpositions[i], tile.generate_transition(tilemap, tindices[i][0], tindices[i][1])))
            self.tiles.append(tile.Tile(int(tiles[i]), tpositions[i]))
    def delta(self, value, dtime):
        return value / 10 * dtime
    def play(self, screen):
        is_playing = True

        # temporarily just add a player and monster sprite to the list
        self.local_player = LocalPlayer(sprite.Sprite.spriteobj_to_sprite(sprite.Sprite, Textures.player("front"), 0))
        monster = Monster(sprite.Sprite.spriteobj_to_sprite(sprite.Sprite, Textures.monster("front"), 0), object.HealthSpec(False, 100, 100, "monster"), "passive")
        self.objects = list([self.local_player, monster])
        self.open_area(self, "test")

        dtime = 0

        while is_playing is True:
            dtime = clock.tick(settings.Settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            object.removeDeadObjects(self.objects)
                #elif event.type == pygame.KEYDOWN:
            #Keys.processPressed(Keys, pygame.key.get_pressed())
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.local_player.move(Vector2(0, -10))
            elif keys[pygame.K_s]:
                self.local_player.move(Vector2(0, 10))
            if keys[pygame.K_a]:
                self.local_player.move(Vector2(-10, 0))
            elif keys[pygame.K_d]:
                self.local_player.move(Vector2(10, 0))
            self.local_player.update(dtime)
            screen_settings.draw_window(screen, self.get_sprites(self))
        pygame.quit()
        return True # return to the menu after game is done.