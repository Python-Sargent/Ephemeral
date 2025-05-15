# python 3.13
#
# Ephemeral Object Classes
# 

class HealthSpec:
    def __init__(self, invulnerable = False, maxhealth = 100, health = 100, damage_group = "none"):
        if invulnerable == False:
            self.maxhealth = maxhealth
            self.health = health
        self.invulnerable = invulnerable
        self.damage_group = damage_group

class Object:
    def __init__(self, ttl, hspec, collider_type = "collider", sprite = None, id=None): # TTL is Time To Live
        if sprite !=None:
            if sprite.is_sprite():
                self.sprite = sprite
            else:
                self.rect = sprite
                self.sprite = None
        self.max_health = hspec.maxhealth
        self.health = hspec.health
        self.invulnerable = hspec.invulnerable
        self.damage_group = hspec.damage_group
        self.ttl = ttl
        self.lifetime = 0
        self.collider_type = collider_type # collider, trigger, none
        self.alive = True
        self.id = id
    
    def remove(self):
        self.sprite = None
        self.rect = None
        self.health = None
        self.max_health = None
        self.alive = None
    
    def duplicate(self):
        return self(self.ttl, HealthSpec(self.invulnerable, self.max_health, self.health, self.damage_group), self.sprite)

def removeDeadObjects(objects):
    for i in range(len(objects)):
        obj = objects[i]
        if obj.health <= 0:
            objects.pop(i)
    return objects