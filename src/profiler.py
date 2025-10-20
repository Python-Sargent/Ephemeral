import src.visual as visual
from pygame import Vector2
from colorsys import hsv_to_rgb as HSV
from src.settings import Settings

def fps_color(fps, tar):
    if fps < tar:
        if fps < tar/2:
            return visual.COLOR(None, (0, 200, 255)).rgb
        else:
            return visual.COLOR(None, (20, 200, 255)).rgb
    else:
        return (255, 255, 255)
        

class Profiler:
    sprites = []
    toggle = False
    elapsed = 0
    dropped_ticks = 0
    def start(self):
        self.sprites.append(visual.create_text("FPS: Frames Per Second", Vector2(32, 8), 16))
        self.sprites.append(visual.create_text("DTA: Dropped Tick Coefficient", Vector2(32, 24), 16))
    def update(self, profile):
        self.elapsed += profile.dtime
        fps = profile.clock.get_fps()

        self.sprites[0] = visual.create_text("FPS: "+str(float("{:.2f}".format(fps))),
                                             Vector2(32, 8), 16, fps_color(fps, Settings.fps))
        self.sprites[1] = visual.create_text("DTC: "+str(float("{:.2f}".format(self.dropped_ticks/(self.elapsed/60)))), Vector2(32, 24), 16)

class Profile:
    def __init__(self, clock, dtime):
        self.clock = clock
        self.dtime = dtime