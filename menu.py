# python 3.13
#
# Ephemeral Main Menu
# 

import pygame
from pygame import *
import src.screen_settings as screen_settings
import client
from src.sprite import Sprite
from src.texture import load_texture
import src.menu_element as menu_element
from src.visual import Colors
import src.log as log
from src.app_interaction import DiscordRPC
from src.settings import Settings
from src.profiler import Profiler
import sys

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
    singleplayer_server_thread = None
    def join_singleplayer(self):
        try:
            port = self.port
            if self.no_server == True:
                port = None
            self.should_continue = client.begin_singleplayer(screen, port)
        except RuntimeError as e:
            log.log(e, log.LogLevel.Error)

    def join_multiplayer(self):
        try:
            port = self.port
            addr = self.address
            if self.no_server == True:
                port = None
                addr = None
            self.should_continue = client.begin_multiplayer(screen, addr, port)
        except RuntimeError as e:
            log.log(e, log.LogLevel.Error)

    no_server = False
    port = 2048
    address = "127.0.0.1"

def draw_menu(screen, sprites = False, profiler=None):
    screen_settings.draw_window(screen, sprites, profiler)
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

# command line options

options = sys.argv[1:]

options_len = len(options)
options_it = iter(options)

for op in options_it:
    match op:
        case "":
            pass
        case "--no-server":
            Menu.no_server = True
        case "--port":
            port = options_it.__next__()
            if port and port != "":
                port = int(port)
                Menu.port = port
        case "--address":
            addr = options_it.__next__()
            if addr and addr != "":
                Menu.address = addr

def main():
    log.log_begin()

    if screen_settings.check_resize(screen, True):
        log.log("Updating Display Params due to forced resize: (" +
                str(screen_settings.DisplayParams.width) + "x" +
                str(screen_settings.DisplayParams.height) + ")", log.LogLevel.Warn)

    bg = menu_element.Background(Sprite(load_texture("menu_background.png", 4, True)))
    Menu.elements.append(bg)

    DiscordRPC.set(DiscordRPC, "In Menu", "Sitting in Main Menu")


    play = menu_element.Button(Menu.join_singleplayer, Menu, "Singleplayer", Colors.white.rgb, 4, Vector2(screen_settings.DisplayParams.width / 2, screen_settings.DisplayParams.height / 2 * 0.4))
    Menu.elements.append(play)
    play2 = menu_element.Button(Menu.join_multiplayer, Menu, "Multiplayer", Colors.white.rgb, 4, Vector2(screen_settings.DisplayParams.width / 2, screen_settings.DisplayParams.height / 2 * 0.8))
    Menu.elements.append(play2)

    while Menu.should_continue is True:
        dtime = clock.tick(Settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.log("Quitting Menu")
                Menu.should_continue = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_click(Menu.elements)
        
        check_hover(Menu.elements)
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_F5]:
        #    Profiler.toggle = not Profiler.toggle
        if Menu.should_update is True: draw_menu(screen, Menu.get_sprites(Menu), None)

    pygame.quit()
    DiscordRPC.stop(DiscordRPC)
    log.log("Menu Stopped")
    log.log_end()

try:
    main()
except Exception as error:
    log.log(error, log.LogLevel.Error)