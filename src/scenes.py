import src.event as event
import pygame
from pygame import display
from src.screen_settings import DisplayParams
from visual import Fade

# Cut Scenes (clientside)
class CutsceneElement:
    def __init__(self, length, action):
        self.length = length
        self.action = action

class Cutscene:
    def __init__(self, background, overlay, fade: tuple): # fade_in: int(1, 255)
        self.bg = background
        self.fg = overlay
        self.fade_in = fade[0]
        self.fade = Fade(-1)
    def fadeIn(self):
        self.fade.reset()
    def fadeOut(self):
        self.fade.reset()
        self.fade.duration = abs(self.fade.duration)
    def start(self, screen):
        clock = pygame.time.Clock()
        while self.running:
            dtime = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            screen.fill((255, 255, 255))
            screen.blit(self.fade.get_fade(dtime), (0, 0))
            display.flip()
        return True
