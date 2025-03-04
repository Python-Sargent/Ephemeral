# python
#
# Multiplayer Networking Game
# 

def EmptyFunction():
    pass

class Action:
    def __init__(self, func, func2 = EmptyFunction):
        self.func = func
        self.func2 = func2
    def run(self):
        self.func()
    def run2(self):
        self.func2()

class Keybind:
    def __init__(self, name, action):
        self.name = name
        self.action = action
    def press(self):
        self.action.run(self.action)
    def unpress(self):
        self.action.run2(self.action)

class Keys:
    class keys:
        KEY_FORWARD = "W"
        KEY_LEFT = "A"
        KEY_DOWN = "S"
        KEY_RIGHT = "D"
        #KEY_JUMP = pygame.Key.SPACE
    keybinds = list([])
    def processPressed(self, keys):
        self.pressed = keys
    def keydown(self, keys):
        for i in range(len(keys)):
            self.keybinds[keys[i]].press()
    def keyup(self, keys):
        for i in range(len(keys)):
            self.keybinds[keys[i]].unpress()