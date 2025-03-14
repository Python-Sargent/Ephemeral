# python
#
# Multiplayer Networking Game
# 

from src.sprite import Sprite
from pygame import Vector2
from src.visual import create_text
from src.texture import load_texture

class Clickable:
    def __init__(self, sprite, action, arguments):
        self.sprite = sprite
        self.action = action
        self.arguments = arguments
    
    def click(self):
        self.action(self.arguments)

class Button(Clickable):
    def __init__(self, action, arguments, label, color, size, pos):
        button = Sprite.spriteobj_to_sprite(Sprite, load_texture("menu_button.png", size))
        button.rect.center = pos
        text = Sprite.spriteobj_to_sprite(Sprite, create_text(label, Vector2(pos[0] + size / 2, pos[1] + size / 2), size * 32, color))
        button.image.blit(text.image, text.rect)
        self.size = size
        super().__init__(button, action, arguments)

    def hover(self):
        #print("hovering")
        pos = self.sprite.rect.center
        button = Sprite.spriteobj_to_sprite(Sprite, load_texture("menu_button_hovered.png", self.size))
        button.rect.center = pos
        self.sprite = button

    def unhover(self):
        #print("unhovering")
        pos = self.sprite.rect.center
        button = Sprite.spriteobj_to_sprite(Sprite, load_texture("menu_button.png", self.size))
        button.rect.center = pos
        self.sprite = button