# python
#
# Multiplayer Networking Game
# 

from pygame import sprite

class Sprite(sprite.Sprite):
    def __init__(self, image, rect, z_index = 0):
        self.rect = rect
        self.image = image
        self.z_index = z_index

    def spriteobj_to_sprite(self, spriteobj, z_index = 0):
        return self(spriteobj[0], spriteobj[1], z_index)
    
    def is_sprite(self):
        return True