# python 3.13
#
# Ephemeral Graphics
# 

from src.settings import Settings
from src.texture import load_texture
from pygame import transform
from pygame import Surface

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
    color_dict = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "silver": (150, 150, 150),
        "gold": (255, 200, 10)
    }

"""
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
"""
        
def create_text(text, pos, size = 32, color = Colors.white):
    from pygame import font
    font.init() # initalize the font to get rid of edge cases, can be called more than once without causing issues
    textfont = font.Font(Settings.font, size)
    image = textfont.render(text, False, color)
    rect = image.get_rect()
    rect.center = (pos.x, pos.y)
    return (image, rect) # returns a spriteobj

def create_button(text, pos):
    from pygame import font
    font.init()
    textfont = font.Font(Settings.font, 32)
    textimage = textfont.render(text, False, Colors.white)
    textrect = textimage.get_rect()
    textrect.center = (pos.x, pos.y)
    return (textimage, textrect) # returns a spriteobj

def create_image(name, pos, size, scalar=None):
    t = load_texture(name)
    if scalar == True: # fit image to size
        t = transform.scale(t, size.x / t.get_width(), size.y / t.get_height())
    elif scalar == False: # scale image aspectively
        if abs(size.x - t.get_width()) < abs(size.y - t.get_height()):
            ar = t.get_height() / t.get_width()
            th = int(size.x * ar)
            tw = size.x
            t = transform.scale(t, tw / t.get_width(), th / t.get_height())
    elif scalar == None:
        t = transform.scale(t, size.x, size.y)
    rect = t.get_rect()
    rect.topleft = pos
    return (t, rect)

def create_surface(pos, size, color):
    s = Surface(size)
    s.fill(color)
    r = s.get_rect()
    r.topleft = pos
    return (s, r)

class Fade:
    def __init__(self, duration, fade_surface) -> None:
        self.duration = duration
        self.surface = fade_surface
        if self.duration >= 0:
            self.surface.set_alpha(0)
    def get_fade(self, dtime):
        current_alpha = self.surface.get_alpha()
        if current_alpha is None:
            self.surface.set_alpha(0 if self.duration >= 0 else 255)
            current_alpha = self.surface.get_alpha()
        
        fade_speed = 255 / self.duration / 60 / 10
        new_alpha = current_alpha + fade_speed * dtime
        if self.duration >= 0:
            if new_alpha >= 255:
                self.surface.set_alpha(255)
            else:
                self.surface.set_alpha(new_alpha)
        else:
            if new_alpha <= 0:
                self.surface.set_alpha(0)
            else:
                self.surface.set_alpha(new_alpha)

        self.surface.set_alpha(int(new_alpha))
        return self.surface
    def reset(self):
        if self.duration >= 0:
            self.surface.set_alpha(0)
        else:
            self.surface.set_alpha(255)