# python
#
# Multiplayer Networking Game
# 

from src.object import HealthSpec

class Settings:
    fps = 60
    tick_speed = 20
    maxhealth = 100
    player_hspec = HealthSpec(False, 100, 100, "friendly_player")
    player_scale = 4
    monster_scale = 4
    tile_scale = 4
    player_speed = 5
    monster_speed = 2
    drag = 1
    font = None
    volume = 0.5
    def set(self, d): # this is a bad way to do it TODO make this a table or smth like that instead
        match d.name:
            case "fps":
                if d.value != None:
                    self.fps = d.value

def load_settings(filename="settings.txt"):
    try:
        file = open(filename)
        for line in file:
            line = line.replace('\n', "") # remove the tailing newline charactor (not the best way?)
            sl = line.split(" ")
            name = None
            desc = None
            dv = None
            if len(sl) >= 1:
                name = int(sl[0])
                if len(sl) >= 2:
                    desc = int(sl[1])
                    if len(sl) >= 3:
                        dv = int(sl[2])
            Settings.set(Settings, SETTING(name, desc, dv))
    except FileNotFoundError:
        print(f"Cannot load settings file: {filename}")
        raise SystemExit

class SETTING:
    def __init__(self, name, description=None, default_value=None):
        self.name = name
        if description != None:
            self.desc = description
        else:
            self.desc = self.name[:1].upper() + self.name[1:] # make the description just a textual version of the name
        self.value = None
        if default_value != None:
            self.value = default_value
