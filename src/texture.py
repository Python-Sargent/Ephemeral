# python
#
# Multiplayer Networking Game
# 

from pygame import transform
from pygame import image as pyimage
from os import path
from src.log import log
from src.settings import Settings

def load_texture(name, scale = False, use_convert = False):
    fullname = path.join("textures", name)
    try:
        image = pyimage.load(fullname)
        if use_convert != False:
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
    except FileNotFoundError:
        #print(f"Cannot load image: {fullname}")
        log(f"Cannot load image: {fullname}")
        #raise SystemExit
        raise OSError("Cannot load " + str(fullname))
    if scale != False:
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = transform.scale(image, size)
    return image

def load_spriteobj(name, scale = False, use_convert = False):
    fullname = path.join("textures", name)
    try:
        image = pyimage.load(fullname)
        if use_convert != False:
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
    except FileNotFoundError:
        #print(f"Cannot load image: {fullname}")
        log(f"Cannot load image: {fullname}")
        #raise SystemExit
        raise OSError("Cannot load " + str(fullname))
    if scale != False:
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = transform.scale(image, size)
    return image, image.get_rect()

class Animation:
    def __init__(self, anim_path, anim_len, anim_delay, anim_scale = 4, offset = 0): # anim path should follow this format: 'player_anim' which will be 'textures/player_anim/0.png' etc.
        self.anim = list([]) # list of image surfaces
        if type(anim_path) == type(""):
            for i in range(anim_len):
                self.anim.append(load_texture(path.join(anim_path, str(i) + ".png"), anim_scale, True))
        #else:
        #    self.image = anim_path
        if anim_len != None: self.current = min(offset, anim_len-1)
        #if anim_len != None: self.image = self.anim[self.current] # set the current image to the one specified by self.current index
        self.delay = anim_delay #              list of delay values for each frame
        self.tick = 0
    def step(self, i=1):
        if self.current + i < len(self.anim):
            self.current += i
        elif i <= 1:
            self.current = 0
        #print(self.current)
        #self.image = self.anim[self.current]
    def update(self):
        pass
        #self.image = self.anim[self.current]
    def image(self):
        return self.anim[self.current]

def texture_type(input):
    if type(input) == type(list()):
        return "anim"
    else:
        return "image"

def anim_image(animation):
    if type(animation) == type(Animation(None, None, None)) and type(animation.anim) == type(list([])):
        return animation.anim[animation.current]
    else:
        #print("anim_image() returning: " + str(animation))
        return animation
    
def is_anim(animation):
    if type(animation) == type(Animation(None, None, None)): return True

class TextureProperties():
    def __init__(self, path, len = 1, delay = Settings.tick_speed * 2, scale = 4):
        # Image Properties
        self.path = path
        self.scale = scale

        # Animation Properties
        self.anim_path = path
        self.anim_len = len
        self.anim_scale = scale

class TextureType():
    TEXTURE_ANIMATION = "anim"
    TEXTURE_IMAGE = "img"

def extend_list(len1, ilist, fill_value=None):
    if len(ilist) < len1: ilist.extend([fill_value] * (len1 - len(ilist)))
    return ilist

class Texture():
    def __init__(self, path, texture_type, properties = None):
        if path == None or texture_type == None: return
        if texture_type == TextureType.TEXTURE_ANIMATION and properties != None: # if animation
            if len(properties.delay) < properties.len: # do we need to extend the delay list
                last_delay = properties.delay[-1] # get the last delay in the list
                delay = extend_list(properties.len, properties.delay, fill_value=last_delay)
            self.texture = Animation(path, properties.len, delay, properties.scale)
            self.tick = 0 # when this reaches the delay for the frame then we should step
        elif texture_type == TextureType.TEXTURE_IMAGE and properties != None:
            self.texture = load_texture(path, properties.scale)[0]
    def image(self):
        if is_anim(self.texture):
            return self.texture.image()
        else:
            return self.texture

def is_texture(texture):
    if type(texture) == type(Texture(None, None)): return True
