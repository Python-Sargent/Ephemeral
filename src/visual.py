# python
#
# Multiplayer Networking Game
# 

from src.object import HealthSpec
from src.settings import Settings

class Colors:
    red = 255, 0, 0
    orange = 175, 80, 0
    yellow = 200, 200, 5
    green = 0, 255, 0
    cyan = 5, 125, 125
    blue = 0, 0, 255
    purple = 125, 5, 125
    black = 0, 0, 0
    white = 255, 255, 255
    darkgrey = 80, 80, 80
    darkgrey2 = 60, 60, 70

class Particle:
    def __init__(self, ttl, sprite = False): # TTL is Time To Live
        if sprite != False:
            if sprite.is_sprite():
                self.sprite = sprite
            else:
                self.rect = sprite
                self.sprite = False
        self.ttl = ttl
        self.lifetime = 0
    
    def remove(self):
        self.sprite = False
        self.rect = False
        self.alive = False
    
    def duplicate(self):
        return self(self.ttl, HealthSpec(self.invulnerable, self.max_health, self.health, self.damage_group), self.sprite)

def create_text(text, pos, size = 32, color = Colors.white):
    from pygame import font
    textfont = font.Font(Settings.font, size)
    image = textfont.render(text, False, color)
    rect = image.get_rect()
    rect.center = (pos.x, pos.y)
    return (image, rect) # returns a spriteobj