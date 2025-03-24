class Server:
    class Settings:
        port = 20001
        multicast_group = "224.8.8.8"

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