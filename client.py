# python
#
# Multiplayer Networking Game
# 

import pygame
from pygame import *
import src.sprite as sprite
import src.visual as visual
import src.screen_settings as screen_settings
from src.log import log
import src.texture as texture
import src.settings as settings
import src.tile as tile
import src.object as obj
from src.player import Player
from src.texture import TextureAssets
from src.app_interaction import DiscordRPC
import src.net as net
import threading
import server
import socket

class Game:
    objects = False # set to False as there are no objects yet
    tiles = False
    active_area = False,
    is_playing = True
    tick_timer = 0
    def animate(self):
        if self.objects != False:
            for i in range(len(self.objects)):
                if texture.is_anim(self.objects[i].sprite.texture):
                    self.objects[i].sprite.texture.tick += 1 # step the tick
                    if self.objects[i].sprite.texture.tick >= self.objects[i].sprite.texture.delay[self.objects[i].sprite.texture.current]:
                        self.objects[i].sprite.texture.step()
                        self.objects[i].sprite.texture.tick = 0
        if self.tiles != False:
            for i in range(len(self.tiles)):
                self.tiles[i].animation.tick += 1 # step the tick
                if self.tiles[i].animation.tick >= self.tiles[i].animation.delay[self.tiles[i].animation.current]:
                    self.tiles[i].animation.step()
                    self.tiles[i].animation.tick = 0
    def tick(self, dtime, tick_time):
        self.animate(self)
    def get_sprites(self):
        sprites = []
        if self.tiles != False:
            for i in range(len(self.tiles)):
                ts = sprite.Sprite(self.tiles[i].image())
                ts.rect = self.tiles[i].rect
                sprites.append(ts)
        for i in range(len(self.objects)):
            sprites.append(self.objects[i].sprite)
        return sprites
    def get_local_player(self):
        for i in range(len(self.objects)):
            o = self.objects[i]
            if o.id and o.id == "LocalPlayer":
                return i, o
    #def delta(self, value, dtime):
    #    return value / 10 * dtime

def handle_tick(dtime):
    if Game.tick_timer > 100:
        log(str(int(Game.tick_timer/50)) + " ticks were dropped", "Warning")
        Game.tick_timer = 0; # timer has fallen behind at least 2 ticks, drop all the ticks
    if Game.tick_timer >= 50:
        Game.tick(Game, dtime, Game.tick_timer)
        Game.tick_timer -= 50

def begin(screen, ip="127.0.0.1", port=2048):

    pygame.display.set_caption(screen_settings.DisplayParams.titles.game)

    screen.fill(visual.Colors.darkgrey)
    textobj = visual.create_text("Connecting to Server...", Vector2(screen_settings.DisplayParams.center[0], screen_settings.DisplayParams.center[1]), 48)
    text_sprite = sprite.Sprite(textobj[0])
    text_sprite.rect = textobj[1]
    screen.blit(text_sprite.image(), text_sprite.rect)
    pygame.display.flip()

    client = None

    if ip != None and port != None:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_id = client.connect((ip, port))
            client.sendall(net.pack(net.Network.Headers.DEBUG_MESSAGE, ["Hello from client".encode("utf-8")]))
        except:
            log(f"Could not connect to server {ip}", "Error")

    continue_application = True
    try:
        #run_menu_when_done = game.Game.play(game.Game, screen, client)
        clock = pygame.time.Clock()

        pygame.display.set_caption(screen_settings.DisplayParams.titles.game)
        log("Starting Game")
        Game.is_playing = True

        # temporarily just add a player sprite to the list and open the test map
        player = Player(sprite.Sprite(TextureAssets.player("front").image(), 0), "LocalPlayer")
        Game.objects = list([player])
        Game.tiles = tile.open_tmap_from_area("test")

        dtime = 0

        while Game.is_playing is True:
            dtime = clock.tick(settings.Settings.fps)
            Game.tick_timer += dtime

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log("Quitting Game")
                    continue_application = False
                    Game.is_playing = False
                
            obj.removeDeadObjects(Game.objects)
            lpi, lpo = Game.get_local_player(Game)
                #elif event.type == pygame.KEYDOWN:
            #Keys.processPressed(Keys, pygame.key.get_pressed())
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                Game.objects[lpi].move(Vector2(0, -10))
            elif keys[pygame.K_s]:
                Game.objects[lpi].move(Vector2(0, 10))
            if keys[pygame.K_a]:
                Game.objects[lpi].move(Vector2(-10, 0))
            elif keys[pygame.K_d]:
                Game.objects[lpi].move(Vector2(10, 0))
            Game.objects[lpi].update(dtime)

            handle_tick(dtime)

            #print("frame: " + str(dtime))
            #print(Game.tick_timer)

            screen_settings.draw_window(screen, Game.get_sprites(Game))

        log("Game Finished")
    except error as e:
        log(e, "Error")
    return continue_application

def begin_singleplayer(screen, port):
    log("Joining singleplayer game")
    DiscordRPC.set(DiscordRPC, "In Game", "Playing Singleplayer")
    # start server
    #sst = threading.Thread(None, server.start, "SINGLEPLAYER_SERVER", (port, 1, True, 1, True), {}, False) # None, func, name, args, kwargs, daemon
    #sst.start()
    try:
        cont = begin(screen, "127.0.0.1", port)
    except error as e:
        log(e, "Error")
    #sst.join() # wait for server to stop
    return cont

def begin_multiplayer(screen, addr, port):
    log("Joining multiplayer game")
    DiscordRPC.set(DiscordRPC, "In Game", "Playing Multiplayer")
    cont = True
    try:
        cont = begin(screen, addr, port)
    except error as e:
        log(e, "Error")
    return cont

def main(): # allow the client to be started directly without having to call begin() and pass in the screen
    screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
    begin_singleplayer(screen, None)

if __name__ == "__main__": # start the client if it is being run from command line, otherwise it is likely being run by import
    main()
