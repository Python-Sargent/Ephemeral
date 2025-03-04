import pygame

pygame.mixer.init()

if pygame.mixer.get_init():
    print("pygame.mixer initialized")
else:
    raise ValueError("Missing module 'pygame.mixer'")