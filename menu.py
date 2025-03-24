# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import src.screen_settings as screen_settings
from client import begin as begin_client
from src.sprite import Sprite
from src.texture import load_texture
import src.menu_element as menu_element
from src.visual import Colors
import src.log as log
from src.app_interaction import DiscordRPC
from src.settings import Settings

pygame.init()

screen_settings.DisplayParams.center = (screen_settings.DisplayParams.size[0] / 2, screen_settings.DisplayParams.size[1] / 2)

screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
pygame.display.set_caption(screen_settings.DisplayParams.titles.menu)
pygame.display.set_icon(screen_settings.DisplayParams.icon)

clock = pygame.time.Clock()

volume = 0.5

class Scene:
    class Menu:
        music = False
    class Game:
        areas = list([])

class Menu:
    elements = list([])
    def get_sprites(self):
        sprites = list([])
        for i in range(len(self.elements)):
            sprites.append(self.elements[i].sprite)
        return sprites
    should_continue = True
    should_update = True
    def join_singleplayer(self):
        log.log("Joining singleplayer game")
        DiscordRPC.set(DiscordRPC, "In Game", "Playing Singleplayer")
        self.should_continue = begin_client(screen) # TODO eventually pass in the server ip (localip or multiplayer server ip)

def draw_menu(screen, sprites = False):
    if sprites == False:
        screen.fill(screen_settings.DisplayParams.fill_color)
    else:
        screen.fill(screen_settings.DisplayParams.fill_color)
        screen_settings.draw_frame(screen, sprites)
    display.flip()
    Menu.should_update = False

def check_hover(elements):
    mousepos = pygame.mouse.get_pos()
    for i in range(len(elements)):
        if elements[i].sprite.rect.collidepoint(mousepos):
            try:
                elements[i].hover()
                Menu.should_update = True
            except:
                pass # doesn't matter if I do pass or continue
        else:
            try:
                elements[i].unhover()
                Menu.should_update = True
            except:
                pass

def check_click(elements):
    mousepos = pygame.mouse.get_pos()
    for i in range(len(elements)):
        if elements[i].sprite.rect.collidepoint(mousepos):
            try:
                elements[i].click()
                #Menu.should_update = True
            except:
                continue

def main():

    #bg = Sprite.spriteobj_to_sprite(Sprite, load_spriteobj("menu_bg.png"))
    #Menu.elements.append(bg)

    log.log_begin()

    play = menu_element.Button(Menu.join_singleplayer, Menu, "Singleplayer", Colors.white, 4, Vector2(screen_settings.DisplayParams.width / 2, screen_settings.DisplayParams.height / 2))
    Menu.elements.append(play)

    DiscordRPC.set(DiscordRPC, "In Menu", "Sitting in Main Menu")

    while Menu.should_continue is True:
        dtime = clock.tick(Settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.log("Quitting Menu")
                Menu.should_continue = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_click(Menu.elements)
        
        check_hover(Menu.elements)

        if Menu.should_update is True: draw_menu(screen, Menu.get_sprites(Menu))

        #if Menu.should_continue is True: Menu.join_singleplayer(Menu)

    pygame.quit()

    DiscordRPC.stop(DiscordRPC)

    log.log("Menu Stopped")

    log.log_end()

main()