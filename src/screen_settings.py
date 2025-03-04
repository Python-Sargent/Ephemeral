# python
#
# Multiplayer Networking Game
# 

from src.texture import load_texture
from pygame import display as pydisplay

class DisplayParams:
    size = width, height = 1920, 1080
    class titles:
        game = "Ephemeral - Singleplayer"
        menu = "Ephemeral - Main Menu"
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
    framerate = 60

DisplayParams.center = (DisplayParams.size[0] / 2, DisplayParams.size[1] / 2)

def draw_frame(screen, sprites):
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    

def draw_window(screen, sprites = False):
    if sprites == False:
        screen.fill(DisplayParams.fill_color)
    else:
        screen.fill(DisplayParams.fill_color)
        draw_frame(screen, sprites)
    pydisplay.flip()

def update_caption(caption):
    pydisplay.set_caption(caption)