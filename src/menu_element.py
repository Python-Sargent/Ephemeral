from src.sprite import Sprite
from pygame import Vector2
from src.visual import create_text
from src.texture import load_texture

class Clickable:
    def __init__(self, sprite, action):
        self.sprite = sprite
        self.action = action
    
    def click(self):
        self.action()
    
class Button(Clickable):
    def __init__(self, action, label, color, size, pos):
        button = Sprite(load_texture("menu_button.png"))
        text = Sprite.spriteobj_to_sprite(Sprite, create_text(label, Vector2(pos[0] + size / 2, pos[1] + size / 2), size, color))
        button.image.blit(text.image, text.rect)
        super().__init__(button, action)