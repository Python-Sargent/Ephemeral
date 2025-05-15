# python 3.13
#
# Ephemeral Transition Viewer
# 

import src.tile as tile
import pygame
from pygame import *
import src.screen_settings as screen_settings
from src.sprite import Sprite
from src.settings import Settings
import src.log as log
from src.visual import create_text

pygame.init()

#screen_settings.DisplayParams.center = (screen_settings.DisplayParams.size[0] / 2, screen_settings.DisplayParams.size[1] / 2)

screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
pygame.display.set_caption("Ephemeral Transition Viewer")
pygame.display.set_icon(screen_settings.DisplayParams.icon)

clock = pygame.time.Clock()

volume = 0.5

class Scene:
    class Menu:
        music = False
    class Game:
        areas = list([])

class Window:
    elements = list([])
    tiles = list([])
    should_continue = True
    should_update = True
    def get_sprites(self):
        sprites = []
        if self.tiles != False:
            offset = (screen_settings.DisplayParams.size[0]/2 - 16*Settings.tile_scale*3, screen_settings.DisplayParams.size[1]/2 - 16*Settings.tile_scale*3) # center the tiles
            for i in range(len(self.tiles)):
                #print(self.tiles[i].rect)
                sprite = Sprite(self.tiles[i].image())
                rect = self.tiles[i].rect
                rect[0] = int(offset[0]) + rect[0]
                rect[1] = int(offset[1]) + rect[1]
                sprite.rect = rect
                sprites.append(sprite)
                #if self.tiles[i].image2: sprites.append(Sprite(self.tiles[i].image2, self.tiles[i].rect2))
        if self.transition_sprite != None: sprites.append(self.transition_sprite)
        return sprites
    current_tilemap = list([])
    selected_tile_type = 8
    current_tile_scale = Settings.tile_scale
    transition_sprite = None

def draw_map(screen, sprites = False):
    if sprites == False:
        screen.fill(screen_settings.DisplayParams.fill_color)
    else:
        screen.fill(screen_settings.DisplayParams.fill_color)
        screen_settings.draw_frame(screen, sprites)
    display.flip()
    Window.should_update = False

default_map = ("111",
               "111",
               "111")

def check_click():
    mousepos = pygame.mouse.get_pos()
    #print(mousepos)
    for i in range(len(Window.elements)):
        if Window.elements[i].rect.collidepoint(mousepos):
            #change the tile
            i2 = Window.elements[i].rect[0]
            j2 = Window.elements[i].rect[1]
            offset = 16 * Settings.tile_scale
            offsetx = screen_settings.DisplayParams.size[0]/2 - 16*Settings.tile_scale*3
            offsety = screen_settings.DisplayParams.size[1]/2 - 16*Settings.tile_scale*3
            #shift = 8 * Settings.tile_scale
            #pos = Vector2(j2 / offset + shift, i2 / offset + shift)
            #pos = Vector2(j2 / offset - shift, i2 / offset - shift)
            #pos = Vector2((j2 - shift) / offset + 0.5, (i2 - shift) / offset + 0.5)
            pos = Vector2(j2 / (offset - offsetx), i2 / (offset - offsety))
            y = int(pos[0])
            x = int(pos[1])
            print("y: " + str(y))
            print("x: " + str(x))
            #Window.current_tilemap[y][x] = Window.selected_tile_type
            Window.should_update = True
            transition = tile.generate_transition(Window.current_tilemap, y, x)
            print(transition.tile_type)
            print("")
            transition_animation = tile.load_tile_transition_anim(Window.selected_tile_type, transition.tile_type)
            Window.transition_sprite = Sprite(transition_animation)
            new_rect = (screen_settings.DisplayParams.width/2 - 16*Settings.tile_scale, 1600)
            Window.transition_sprite.rect.center= new_rect

def main():
    Window.should_continue = True

    log.log_begin()
    
    area = tile.deserialize_map(default_map)
    Window.current_tilemap = area[0]
    Window.tiles = tile.tilelist_from_area(tile.Area(area[0], None))
    Window.elements = Window.get_sprites(Window)

    textobj = create_text("This tool does not currently work", Vector2(screen_settings.DisplayParams.center[0]-64, screen_settings.DisplayParams.center[1]+64), 96)
    text_sprite = Sprite(textobj[0])
    text_sprite.rect = textobj[1]

    while Window.should_continue is True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Window.should_continue = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_click()
        
        if Window.should_update == True: draw_map(screen, Window.elements); screen.blit(text_sprite.image(), text_sprite.rect); display.flip()

    pygame.quit()

    log.log_end()

main()
