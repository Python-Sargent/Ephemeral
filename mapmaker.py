import src.tile as tile
import pygame
from pygame import *
import src.screen_settings as screen_settings
from src.texture import load_texture
from src.sprite import Sprite
from src.settings import Settings

pygame.init()

screen_settings.DisplayParams.center = (screen_settings.DisplayParams.size[0] / 2, screen_settings.DisplayParams.size[1] / 2)

screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
pygame.display.set_caption("Ephemeral Mapmaker")
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
            for i in range(len(self.tiles)):
                #print(self.tiles[i].rect)
                sprites.append(Sprite(self.tiles[i].image, self.tiles[i].rect))
                #if self.tiles[i].image2: sprites.append(Sprite(self.tiles[i].image2, self.tiles[i].rect2))
        return sprites
    current_tilemap = list([])
    selected_tile_type = 1

def draw_map(screen, sprites = False):
    if sprites == False:
        screen.fill(screen_settings.DisplayParams.fill_color)
    else:
        screen.fill(screen_settings.DisplayParams.fill_color)
        screen_settings.draw_frame(screen, sprites)
    display.flip()
    Window.should_update = False

default_map = ("8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888",
               "8888888888888888888888888888888")

def check_click():
    mousepos = pygame.mouse.get_pos()
    #print(mousepos)
    for i in range(len(Window.elements)):
        if Window.elements[i].rect.collidepoint(mousepos):
            #change the tile
            i2 = Window.elements[i].rect[0]
            j2 = Window.elements[i].rect[1]
            offset = 16 * Settings.tile_scale
            shift = 8 * Settings.tile_scale
            #pos = Vector2(j2 / offset + shift, i2 / offset + shift)
            #pos = Vector2(j2 / offset - shift, i2 / offset - shift)
            #pos = Vector2((j2 - shift) / offset + 0.5, (i2 - shift) / offset + 0.5)
            pos = Vector2(j2 / offset, i2 / offset)
            print(pos)
            x = int(pos[0])
            y = int(pos[1])
            print(Window.current_tilemap[x][y])
            Window.current_tilemap[x][y] = Window.selected_tile_type
            print(Window.current_tilemap[x][y])
            image = Window.elements[i].image
            rect = Window.elements[i].rect
            image = tile.load_tile_image(Window.selected_tile_type)
            Window.elements[i] = Sprite(image, rect)
            Window.should_update = True


def main():
    Window.should_continue = True
    
    area = tile.deserialize_map(default_map)
    Window.current_tilemap = area[0]
    Window.tiles = tile.init_area(tile.Area(area[0], None))
    Window.elements = Window.get_sprites(Window)

    print(Window.current_tilemap)
    print(len(Window.current_tilemap))
    for row in range(len(Window.current_tilemap)):
        print(len(Window.current_tilemap[row]))
        for column in Window.current_tilemap[row]:
            #print(len(column))
            pass

    while Window.should_continue is True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Window.should_continue = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_click()

        if Window.should_update == True: draw_map(screen, Window.elements)

    pygame.quit()

main()
