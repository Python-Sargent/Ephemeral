# python 3.13
#
# Ephemeral Audio Drivers
# 

import pygame
from src.log import log

pygame.mixer.init()

if pygame.mixer.get_init():
    log("pygame.mixer initialized")
else:
    raise ValueError("Missing module 'pygame.mixer'")