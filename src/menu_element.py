# python 3.13
#
# Ephemeral Menu Elements
# 

from src.sprite import Sprite
from pygame import Vector2
from src.visual import create_text
from src.texture import load_texture
from src.texture import load_spriteobj

class Clickable:
    def __init__(self, sprite, action, arguments):
        self.sprite = sprite
        self.action = action
        self.arguments = arguments
    
    def click(self):
        self.action(self.arguments)

class Button(Clickable):
    def __init__(self, action, arguments, label, color, size, pos):
        button = Sprite(load_texture("menu_button.png", size))
        button.rect.center = pos
        text = Sprite.spriteobj_to_sprite(Sprite, create_text(label, Vector2(pos[0] + size / 2, pos[1] + size / 2), size * 32, color))
        b_img = button.image()
        b_img.blit(text.image(), text.rect)
        self.size = size
        b_rect = button.rect
        button = Sprite(b_img)
        button.rect = b_rect
        super().__init__(button, action, arguments)

    def hover(self):
        #print("hovering")
        pos = self.sprite.rect.center
        button = Sprite.spriteobj_to_sprite(Sprite, load_spriteobj("menu_button_hovered.png", self.size))
        button.rect.center = pos
        del self.sprite
        self.sprite = button

    def unhover(self):
        #print("unhovering")
        pos = self.sprite.rect.center
        button = Sprite.spriteobj_to_sprite(Sprite, load_spriteobj("menu_button.png", self.size))
        button.rect.center = pos
        del self.sprite
        self.sprite = button

class Background():
    def __init__(self, sprite):
        self.sprite = sprite