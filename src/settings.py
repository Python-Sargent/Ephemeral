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
    port = 2048
    multicast_group = "224.8.8.8"