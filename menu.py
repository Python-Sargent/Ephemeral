# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import src.screen_settings as screen_settings
from client import begin as begin_client

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
    def get_elements(self):
        return self.elements

def main():

    should_continue = True

    while should_continue is True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_continue = False

        should_continue = begin_client(screen)

        screen_settings.draw_window(screen, Menu.get_elements(Menu))

    pygame.quit()

main()