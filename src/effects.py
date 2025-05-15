# python 3.13
#
# Ephemeral Effects
# 

#################################################################
# Placeholders for functionality that has yet to be implemented #
#################################################################

class Effect: # effects: value * multiplier + blessing - curse
    def __init__(self, name, tick):
        self.name = name
        self.tick = tick

class Multiplier(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect

class Blessing(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect

class Curse(Effect):
    def __init__(self, name, tick, object):
        super().__init__(name, tick)
        self.object = object # provide the object being modified by the effect