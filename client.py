# python 3.13
#
# Ephemeral Client
# 

import pygame
from pygame import *
import src.sprite as sprite
import src.visual as visual
import src.screen_settings as screen_settings
import src.log as log
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
import sys

class Game:
    objects = False # set to False as there are no objects yet
    tiles = False
    active_area = False,
    is_playing = True
    tick_timer = 0
    client = None
    cthread = None
    def animate(self):
        if self.objects != False:
            #print("Objects Len: " + len(self.objects))
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

def handle_recv(h, p):
    match h:
        case net.Network.Headers.UPDATE_CONNECTION:
            if len(p) >= 1 and p[0] == net.Network.Messages.CONNECTION_END:
                if Game.client != None:
                    Game.client.close()
                Game.is_playing = False
                log.log("Quitting Game (Server Closed)")
        case net.Network.Headers.DATA_TILEMAP:
            if len(p) >= 1:
                # unpack the tilemap
                pass
        case net.Network.Headers.DATA_OBJECTMAP:
            if len(p) >= 1:
                # unpack the objectmap
                pass
        case net.Network.Headers.DATA_FEATUREMAP:
            if len(p) >= 1:
                # unpack the featuremap
                pass
        case net.Network.Headers.UPDATE_CHAT:
            if len(p) >= 1:
                # update the chat
                pass
        case net.Network.Headers.UPDATE_OBJECT:
            if len(p) >= 1:
                # update the object list
                pass
        case net.Network.Headers.MODIFY_OBJECT:
            if len(p) >= 1:
                # modify an object
                pass

def client_thread(client: net.Client, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            msg = client.sock.recv(2048)
            if msg == 0b0:
                client.close()
                Game.client = None
                break
            header, payloads = net.unpack(msg)
            handle_recv(header, payloads)
            sh = str(bin(int(header)))[2:]
            ps = ""
            for payload in payloads:
                ps += "\n" + net.payload_str(header, payload)
            log.log(f"Recieved from server << Header: {sh}, Payloads: {ps}")
        except socket.SO_ERROR as e:
            log.log(e, log.LogLevel.Error)
    client.close()

class CThread(threading.Thread):
    def __init__(self, client):
        stop_event = threading.Event()
        super().__init__(None, client_thread, "CLIENT_THREAD", (client, stop_event), {})
        self.daemon = True
        self.stop_event = stop_event
    def stop(self):
        self.stop_event.set()

def handle_tick(dtime):
    if Game.tick_timer > 100:
        log.log(str(int(Game.tick_timer/50)) + " ticks were dropped", "Warning")
        Game.tick_timer = 0; # timer has fallen behind at least 2 ticks, drop all the ticks
    if Game.tick_timer >= 50:
        Game.tick(Game, dtime, Game.tick_timer)
        
        Game.tick_timer -= 50

def begin(screen, ip="127.0.0.1", port=2048):
    log.log("Starting game")

    screen.fill(visual.Colors.darkgrey)
    textobj = visual.create_text("Connecting to Server...", Vector2(screen_settings.DisplayParams.center[0], screen_settings.DisplayParams.center[1]), 48)
    text_sprite = sprite.Sprite(textobj[0])
    text_sprite.rect = textobj[1]
    screen.blit(text_sprite.image(), text_sprite.rect)
    pygame.display.flip()

    sock = None
    if ip != None and port != None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            sock.sendall(net.pack(net.Network.Headers.DEBUG_MESSAGE, ["Hello from client".encode("utf-8"),]))
            Game.client = net.Client((ip, port), sock)
            log.log(f"Connected to server {ip}")
            cthread = CThread(Game.client)
            cthread.start()
            Game.cthread = cthread
        except:
            log.log(f"Could not connect to server {ip}", log.LogLevel.Error)

    continue_application = True
    try:
        #run_menu_when_done = game.Game.play(game.Game, screen, client)
        clock = pygame.time.Clock()
        Game.is_playing = True

        # temporarily just add a player sprite to the list and open the test map
        player = Player(sprite.Sprite(TextureAssets.player("front").image(), 0), "LocalPlayer")
        Game.objects = list([player])
        Game.tiles = tile.open_tmap_from_area("test")

        dtime = 0

        log.log("Game Started")

        while Game.is_playing is True:
            dtime = clock.tick(settings.Settings.fps)
            Game.tick_timer += dtime

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.log("Quitting Game")
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

            screen_settings.draw_window(screen, Game.get_sprites(Game), clock.get_fps())

        log.log("Game Finished")
    except RuntimeError as e:
        log.log(e, log.LogLevel.Error)
        if settings.Settings.mode == "Development":
            return False # crash the client in development mode
    if Game.client != None:
        Game.client.close()
        log.log("Closing Connection")
    return continue_application

def begin_singleplayer(screen, port):
    pygame.display.set_caption(screen_settings.DisplayParams.titles.singleplayer)
    log.log("Joining singleplayer game")
    DiscordRPC.set(DiscordRPC, "In Game", "Playing Singleplayer")

    # start server
    if port != None:
        stop_event = threading.Event()
        sst = threading.Thread(None, server.start, "SINGLEPLAYER_SERVER", (port, 1, True, 1, stop_event), {}) # None, func, name, args, kwargs
        sst.start()
    
    try:
        cont = begin(screen, "127.0.0.1", port)
    except RuntimeError as e:
        log.log(e, log.LogLevel.Error)
    
    if port != None:
        #sst.join() # wait for server to stop
        stop_event.set()
    
    return cont

def begin_multiplayer(screen, addr, port):
    pygame.display.set_caption(screen_settings.DisplayParams.titles.multiplayer)
    log.log("Joining multiplayer game")
    DiscordRPC.set(DiscordRPC, "In Game", "Playing Multiplayer")
    cont = True
    try:
        cont = begin(screen, addr, port)
    except RuntimeError as e:
        log.log(e, log.LogLevel.Error)
    return cont

def main(): # allow the client to be started directly without having to call begin() and pass in the screen
    screen = pygame.display.set_mode(screen_settings.DisplayParams.size)
    begin_singleplayer(screen, None)

if __name__ == "__main__": # start the client if it is being run from command line, otherwise it is likely being run by import
    try:
        main()
    except Exception as error:
        if settings.Settings.mode == "Development":
            raise # crash the client
        log.log(f"Unexpected error: {error}", log.LogLevel.Error)
        sys.exit(1)
