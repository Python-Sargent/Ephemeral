# python 3.13
#
# Ephemeral Visual/Display Settings
# 

from src.texture import load_texture
from pygame import display as pydisplay
from src.visual import create_text
from pygame import Vector2

class DisplayParams:
    size = width, height = 1920, 1080
    class titles:
        singleplayer = "Ephemeral - Singleplayer"
        multiplayer = "Ephemeral - Multiplayer"
        menu = "Ephemeral - Main Menu"
    fill_color = 20, 20, 20
    icon = load_texture("icon.png", False, False)
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
        screen.blit(sprites[i].image(), sprites[i].rect)

def draw_window(screen, sprites = False, fps=None):
    if sprites == False:
        screen.fill(DisplayParams.fill_color)
    else:
        screen.fill(DisplayParams.fill_color)
        draw_frame(screen, sprites)
    if fps != None:
        textobj = create_text("Fps: "+str(float("{:.2f}".format(fps))), Vector2(32, 8), 16)
        screen.blit(textobj[0], textobj[1])
    pydisplay.flip()

def update_caption(caption):
    pydisplay.set_caption(caption)