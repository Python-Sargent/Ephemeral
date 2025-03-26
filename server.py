import socket

class ServerClient:
    def __init__(self, ip, sock):
        self.ip = ip
        self.sock = sock

class Server:
    class Settings:
        port = 2048
        host = socket.gethostbyname(socket.gethostname()) # for multiplayer and LAN
        #host = "127.0.0.1" # localhost for testing and singleplayer
        multicast_group = "224.8.8.8"
        client_limit = 4 # maximum amount of unanswered connections
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = list([])
    def create(self, host=None, port=None):
        if host != None: self.host = host
        if port != None: self.port = port
        self.tcp.bind((self.Settings.host, self.Settings.port))
        pass
    def listen(self):
        self.tcp.listen(self.Settings.client_limit)
    def accept(self):
        commsock, ip = self.tcp.accept()
        self.clients.append(ServerClient(ip, commsock))
        print("Client connected at " + str(ip))
        return ip
    def recv_bytes(self, protocol, ip):
        if protocol == Network.PROTOCOL_TCP:
            for i in range(len(self.clients)):
                if self.clients[i].ip == ip:
                    return self.clients[i].sock.recv(1024).decode("utf-8")
        elif protocol == Network.PROTOCOL_UDP:
            #return self.udp.recv()
            print("UDP not supported")
            pass
    def recv_str(self, protocol, ip):
        if protocol == Network.PROTOCOL_TCP:
            for i in range(len(self.clients)):
                if self.clients[i].ip == ip:
                    return self.clients[i].sock.recv(1024).decode("utf-8")
        elif protocol == Network.PROTOCOL_UDP:
            #return self.udp.recv()
            print("UDP not supported")
            pass
    def close(self, ip):
        for i in range(len(self.clients)):
            if self.clients[i].ip == ip:
                self.clients[i].sock.close()
                self.clients.pop(i)
    


class Network:
    def send(ip, content):
        pass # send content to ip
    def recieve(ip = None):
        pass # recieve incoming data
    def serialize(content):
        pass # convert content to sendable form
    def deserialize(content):
        pass
    class RequestTypes:
        SERVER_GET_INFO = "INFO"
        SERVER_ADD_CLIENT = "CLIENT_ADD"
        SERVER_REMOVE_CLIENT = "CLIENT_REMOVE"
        SERVER_CLIENT_INPUT = "CLIENT_INPUT"
    class Headers:
        DATA_TILEMAP = 0b1111
    PROTOCOL_TCP = "TCP"
    PROTOCOL_UDP = "UDP"

def serialize_message(header, payload):
    # return header + payload
    pass


def main():
    Server.create(Server)

    running = True
    
    Server.listen(Server)
    while running is True:
        ip = Server.accept(Server)

        print(Server.recv_str(Server, Network.PROTOCOL_TCP, ip))
    Server.close(Server, ip)

main()

"""
import socket
import struct
from src.settings import Settings
from _thread import *
import sys

UDP_MULTICAST_GROUP = Settings.multicast_group
UDP_PORT = Settings.port

server = "192.168.0.70"
port = UDP_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
"""