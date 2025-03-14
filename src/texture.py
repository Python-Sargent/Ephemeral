# python
#
# Multiplayer Networking Game
# 

from pygame import transform
from pygame import image as pyimage
from os import path
from src.log import log

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
    return image, image.get_rect()

