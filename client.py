# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import src.sprite as sprite
import src.visual as visual
import src.game as game
import src.screen_settings as screen_settings
from src.settings import Settings
import socket
from time import sleep as s

def begin(screen, ip="127.0.0.1", port=2048):

    pygame.display.set_caption(screen_settings.DisplayParams.titles.game)

    screen.fill(visual.Colors.darkgrey)
    textobj = visual.create_text("Connecting to Server...", Vector2(screen_settings.DisplayParams.center[0], screen_settings.DisplayParams.center[1]), 48)
    text_sprite = sprite.Sprite(textobj[0])
    text_sprite.rect = textobj[1]
    screen.blit(text_sprite.image(), text_sprite.rect)
    pygame.display.flip()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_id = client.connect((ip, port))
    client.send("Hello server!".encode("utf-8"))

    return game.Game.play(game.Game, screen)

def main(): # allow the client to be started directly without having to call begin() and pass in the screen
    screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
    begin(screen)

# main() should not be called here, as begin() will run twice when begin (imported as begin_client in menu) is used.