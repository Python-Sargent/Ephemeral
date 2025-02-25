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

def load_texture(name):
    fullname = os.path.join("textures", name)
    try:
        image = pygame.image.load(fullname)
        print(fullname)
        #if image.get_alpha() is None:
        #    image = image.convert()
        #else:
        #    image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()

class DisplayParams:
    size = width, height = 1920, 1080
    title = "Ephemeral - Main Menu"
    fill_color = 20, 20, 20
    icon = load_texture("icon.png")[0]
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

class Textures:
    def player(img_name):
        return load_texture("player_" + img_name + ".png")
    def monster(img_name):
        return load_texture("monster_" + img_name + ".png")

DisplayParams.center = (DisplayParams.size[0] / 2, DisplayParams.size[1] / 2)

screen = pygame.display.set_mode(DisplayParams.size)
pygame.display.set_caption(DisplayParams.title)
pygame.display.set_icon(DisplayParams.icon)

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

class Scene:
    class Menu:
        music = False
    class Game:
        class Scenes:
            tiles = []
            objects = [] # pre placed objects (monsters, powerups, etc.)

class HealthSpec:
    def __init__(self, invulnerable = False, maxhealth = 100, health = 100, damage_group = "none"):
        if invulnerable == False:
            self.maxhealth = maxhealth
            self.health = health
        self.invulnerable = invulnerable
        self.damage_group = damage_group

class Game:
    class settings: # overwritten with server settings during multiplayer
        fps = 60
        maxhealth = 100
        player_hspec = HealthSpec(False, 100, 100, "friendly_player")
    sprites = False # set to False as there are no sprites yet
    players = False # same, but for specifically players
    scene = 0 # 0 is menu, 1 = game, 2 = settings
    game_scene = 0 # for scenes inside the game

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, rect, z_index = 0, object_index = False):
        self.rect = rect
        self.image = image
        self.z_index = z_index
        self.object_index = object_index

    #def update(self):

    def spriteobj_to_sprite(self, spriteobj, z_index = 0, object_index = False):
        if object_index != False:
            return self(spriteobj[0], spriteobj[1], z_index, object_index)
        else:
            return self(spriteobj[0], spriteobj[1])
    
    def is_sprite(self):
        return True

player_image = load_texture("player_front.png") # init the player sprite as the front facinf texture

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
    
    def remove(self):
        self.sprite = False
        self.rect = False
        self.health = 0
        self.max_health = 0
        self.alive = False
    
    def duplicate(self):
        return self(self.ttl, HealthSpec(self.invulnerable, self.max_health, self.health, self.damage_group), self.sprite)

class Player(Object):
    def __init__(self, sprite):
        super().__init__(-1, Game.settings.player_hspec, "collider", sprite) 
        self.pos = sprite.rect.center

class Monster(Object):
    def __init__(self, sprite, hspec, agression):
        super().__init__(60000, hspec, "collider", sprite) 
        self.pos = sprite.rect.center
        self.agression = agression # passive, agressive, passive_agressive, triggered

class LocalPlayer(Player):
    def __init__(self):
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
spriteobj = create_text("Connecting to Server...", Vector2(DisplayParams.center[0], DisplayParams.center[1]), 48)
sprite = Sprite.spriteobj_to_sprite(Sprite, spriteobj)
screen.blit(sprite.image, sprite.rect)
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

def main():

    should_continue = True

    # temporarily just add a player sprite to the list
    player = Player(Sprite.spriteobj_to_sprite(Sprite, Textures.player("front"), 0, 0))
    monster = Monster(Sprite.spriteobj_to_sprite(Sprite, Textures.monster("front"), 0, 1), HealthSpec(False, 100, 100, "monster"), "passive")
    Game.sprites = list([player.sprite, monster.sprite])

    deltaTime = 0

    while should_continue is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_continue = False

        draw_window(Game.sprites)
        deltaTime = clock.tick(Game.settings.fps) / 1000

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