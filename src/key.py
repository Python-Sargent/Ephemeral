# python 3.13
#
# Ephemeral Key Handling
# 

def EmptyFunction():
    pass

class KeyProvider:
    def __init__(self, actionlist):
        self.modkeys = []
        if len(actionlist) == 4:
            self.modkeys = actionlist
        else:
            for i in range(len(actionlist)):
                self.modkeys.append(actionlist[i])
            for i in range(len(self.modkeys)-4):
                self.modkeys.append(EmptyFunction)

class KeyDef:
    def __init__(self, kpv):
        modkeys = kpv.modkeys
        # modkeys is a tuple or list: (key, ctrl+key, shift+key, ctrl+shift+key)
        self.f1 = modkeys[0]
        self.f2 = modkeys[1]
        self.f3 = modkeys[2]
        self.f4 = modkeys[3]

class KeyAction:
    def __init__(self, f1=None, f2=None, f3=None, f4=None):
        self.func = f1
        self.func2 = f2
        self.func3 = f3
        self.func4 = f4

class Action:
    def __init__(self, key_action):
        self.func = key_action.func
        self.func2 = key_action.func2
        self.func3 = key_action.func3
        self.func4 = key_action.func4
    def run(self):
        self.func()
    def run2(self):
        self.func2()
    def run3(self):
        self.func3()
    def run4(self):
        self.func4()

class Keybind:
    def __init__(self, name, action):
        self.name = name
        self.action = action
    def press(self):
        self.action.activate(self.action)
    def unpress(self):
        self.action.deactivate(self.action)

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