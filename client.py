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
from time import sleep as s

def begin(screen):

    pygame.display.set_caption(screen_settings.DisplayParams.titles.game)

    screen.fill(visual.Colors.darkgrey)
    textobj = visual.create_text("Connecting to Server...", Vector2(screen_settings.DisplayParams.center[0], screen_settings.DisplayParams.center[1]), 48)
    text_sprite = sprite.Sprite.spriteobj_to_sprite(sprite.Sprite, textobj)
    screen.blit(text_sprite.image, text_sprite.rect)
    pygame.display.flip()
    s(1) # fake the wait for connect

    return game.Game.play(game.Game, screen)