# python 3.13
#
# Ephemeral Sprites
# 

from pygame import sprite as pysprite
from src.texture import Animation
from src.texture import is_anim
from src.texture import is_texture

class Sprite(pysprite.Sprite):
    def __init__(self, texture, z_index = 0):
        if is_anim(texture) or is_texture(texture): self.rect = texture.image().get_rect()
        else: self.rect = texture.get_rect()
        self.texture = None
        if type(texture) == "str":
            self.texture = Animation(texture, 0, [0])
        else:
            self.texture = texture
        #self.image = anim_image(self.texture)
        self.z_index = z_index

    def spriteobj_to_sprite(self, spriteobj, z_index = 0):
        sprite = self(spriteobj[0], z_index)
        sprite.rect = spriteobj[1]
        return sprite
    
    def is_sprite(self):
        return True
    
    def image(self):
        if self.texture != None:
            if is_anim(self.texture):
                return self.texture.image()
            else: return self.texture
        #else: return self.image