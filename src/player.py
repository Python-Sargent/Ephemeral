# python 3.13
#
# Ephemeral Player Class
# 

from src.settings import Settings
from pygame import Vector2
from src.texture import TextureAssets
from src.object import Object

class Player(Object):
    def __init__(self, sprite, name):
        super().__init__(-1, Settings.player_hspec, "collider", sprite, name) 
        self.pos = sprite.rect.center
    textures = ["back", "left", "front", "right"]
    velocity = Vector2(0, 0)
    effects = list([])
    def set_pos(self, vec2):
        self.sprite.rect.center = vec2
    def get_pos(self):
        return self.sprite.rect.center
    #def set_texture(self, texture):
    #    self.sprite.image = texture
    def set_texture(self, texture_index):
        self.sprite.texture = TextureAssets.player(self.textures[texture_index])

    def animate_move(self, pos, delta):
        if pos[0] < delta[0]:
            self.set_texture(3)
        elif pos[0] > delta[0]:
            self.set_texture(1)
        if pos[1] < delta[1]:
            if pos[0] < delta[0]:
                self.set_texture(3)
            elif pos[0] > delta[0]:
                self.set_texture(1)
            else:
                self.set_texture(2)
        elif pos[1] > delta[1]:
            self.set_texture(0)
    def apply_drag(self):
        if self.velocity[0] < 0:
            self.velocity[0] += Settings.drag
        elif self.velocity[0] > 0:
            self.velocity[0] -= Settings.drag
        if self.velocity[1] < 0:
            self.velocity[1] += Settings.drag
        elif self.velocity[1] > 0:
            self.velocity[1] -= Settings.drag
    def move(self, vec2):
        self.animate_move(self.sprite.rect.center, self.sprite.rect.center + vec2)
        #log(self.velocity)
        self.velocity = Vector2(max(min(self.velocity[0] + vec2[0], 
                                        Settings.player_speed),
                                        -Settings.player_speed),
                                max(min(self.velocity[1] + vec2[1],
                                        Settings.player_speed),
                                        -Settings.player_speed))
        #log(self.velocity)
    def update(self, dtime):
        self.apply_drag()
        self.sprite.rect.center += self.velocity / 10 * dtime