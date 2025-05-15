# python 3.13
#
# Ephemeral Server
# 

import socket
import sys
import src.net as net
from src.net import Client as ServerClient
from src.version import Version
import threading
import src.log as log
import src.settings as settings

l = log.Log("server_log.txt")

def __del_client__(server, ip):
    ci = server.get_client(ip)
    if ci != None:
        server.clients[ci].end_connection()
        server.clients.pop(ci)
        return True
    else:
        return False

def __handle_request__(server, client: ServerClient, header, payloads):
        if header == net.Network.Headers.CLIENT_REQUEST:
            request = None
            if len(payloads) >= 1: request = payloads[0]
            match request:
                case net.Network.Requests.SERVER_GET_INFO:
                    return net.pack(net.Network.Headers.SERVER_INFO, server.get_info())
                case net.Network.Requests.CLIENT_INPUT:
                    try: inp = payloads[1]
                    except: l.log(f"Invalid/Missing input from {client.ip}, in request CLIENT_INPUT<{net.Network.Requests.CLIENT_INPUT}>", log.LogLevel.Error); inp = None
                    server.recieve_input(client, inp)
                    return None
                case net.Network.Requests.CLIENT_END:
                    __del_client__(server, client.ip)
                    return None # connection has ended, we shouldn't be trying to send anything through the socket as it's now closed
        elif header == net.Network.Headers.UPDATE_CONNECTION:
            u = None
            if len(payloads) >= 1: u = payloads[0]
            if u != None and u == net.Network.Messages.CONNECTION_END:
                client.sock.close()
                __del_client__(server, client.ip)
        return None

def threaded_tcpclient(client: ServerClient, stop_event: threading.Event, server):
    client.sock.sendall(net.pack(net.Network.Headers.DEBUG_MESSAGE, ["Hello from server".encode("utf-8"),]))
    while not stop_event.is_set():
        try:
            msg = client.sock.recv(2048)
            #print(type(msg))
            if type(msg) == type(int()) and msg == 0 or msg == bytes():
                client.close()
                stop_event.set()
                __del_client__(server, client.ip)
                break
            header, payloads = net.unpack(msg)
            response = __handle_request__(server, client, header, payloads)
            if response != None: client.sock.sendall(response)
            sh = str(bin(int(header)))[2:]
            ps = ""
            for payload in payloads:
                ps += "\n" + net.payload_str(header, payload)
            l.log(f"Recieved from client << Header: {sh}, Payloads: {ps}")
        except RuntimeError as e:
            l.log(e, log.LogLevel.Error)
            break
    client.close()

class ClientThread(threading.Thread):
    def __init__(self, client: ServerClient, server):
        stop_event = threading.Event()
        super().__init__(None, threaded_tcpclient, "CLIENT_THREAD", (client, stop_event, server), {})
        self.daemon = True
        self.stop_event = stop_event
    def stop(self):
        self.stop_event.set()

class ThreadClient:
    def __init__(self, client: ServerClient, thread: ClientThread):
        self.client = client
        self.thread = thread
    def end_connection(self):
        self.client.close()
        self.thread.stop()

class Server:
    def __init__(self, name = "Ephemeral Server", c=[4, None], host = socket.gethostbyname(socket.gethostname()), port = 2048):
        self.name = name
        self.port = port
        self.client_max = c[0]
        self.client_limit = c[1]
        self.host = host
        self.version = Version.ServerVersion
        self.clients = list([])
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.should_continue = True
    def create(self, host=None, port=None):
        if host != None: self.host = host
        if port != None: self.port = port
        try:
            self.tcp.bind((self.host, self.port))
        except socket.error as e:
            l.log(e, log.LogLevel.Error)
            return None
    def listen(self):
        self.tcp.listen(self.client_max)
    def accept_tcp(self):
        commsock, ip = self.tcp.accept()
        l.log("Client connected at " + str(ip))
        return ServerClient(ip, commsock)
    def get_info(self):
        payloads = bytearray()
        payloads.extend((self.display_name + "\n").encode("utf-8"))
        payloads.extend((self.host + "\n").encode("utf-8"))
        payloads.extend((self.version + "\n").encode("utf-8"))
        return payloads
    def get_client(self, name):
        for i in range(len(self.clients)):
            tclient = self.clients[i]
            try:
                if tclient.client.sock.getpeername()[0] == name[0] or tclient.client.ip == name[0]:
                    return i
            except:
                return None
    def recieve_input(self, client: ServerClient, inp):
        l.log(f"Recieved input from client at {client.ip}, Input: {inp}")
    def stop(self):
        self.should_continue = False
        for i in range(len(self.clients)):
            self.clients[i].end_connection()
            self.clients.pop(i)
        self.tcp.close()
    #def recv_bytes(self, protocol, ip):
    #    if protocol == net.Network.PROTOCOL_TCP:
    #        for i in range(len(self.clients)):
    #            if self.clients[i].ip == ip:
    #                return self.clients[i].sock.recv(1024).decode("utf-8")
    #    elif protocol == net.Network.PROTOCOL_UDP:
    #        #return self.udp.recv()
    #        l.log("UDP not supported"
    #def recv_str(self, protocol, ip):
    #    if protocol == net.Network.PROTOCOL_TCP:
    #        for i in range(len(self.clients)):
    #            if self.clients[i].ip == ip:
    #                return self.clients[i].sock.recv(1024).decode("utf-8")
    #    elif protocol == net.Network.PROTOCOL_UDP:
    #        #return self.udp.recv()
    #        l.log("UDP not supported")
    #def close(self, ip):
    #    for i in range(len(self.clients)):
    #        if self.clients[i].ip == ip:
    #            self.clients[i].sock.close()
    #            self.clients.pop(i)

options = sys.argv[1:]

options_len = len(options)
options_it = iter(options)

class __options__:
    def __init__(self):
        self.localhost = None
        self.port = None
        self.cmax = None
        self.climit = None

opt = __options__()

for op in options_it:
    match op:
        case "":
            pass
        case "--localhost":
            opt.localhost = True
        case "--port":
            port = next(options_it)
            if port and port != "":
                port = int(port)
                opt.port = port
        case "--client-max":
            limit = next(options_it)
            if limit and limit != "":
                limit = int(limit)
                opt.client_max = limit
        case "--client-limit":
            limit = next(options_it)
            if limit and limit != "":
                limit = int(limit)
                opt.client_limit = limit

if len(options) > 0:
    l.log(f"Running server with options: \nPort: {opt.port}\nLocalhost: {opt.localhost}\nMaximum Waiting Clients: {opt.cmax}\nClient Limit: {opt.climit}")

def start(custom_port=None, custom_client_max=None, localhost_override=None, client_limit=None, stop_event=None, server = Server()):
    if custom_port != None: server.port = custom_port
    if custom_client_max != None: server.client_max = custom_client_max
    if localhost_override != None and localhost_override == True: server.host = "127.0.0.1"
    if client_limit != None: server.client_limit = client_limit

    l.log("Server started")

    server.create()
    server.listen()

    while server.should_continue is True:
        if server.client_limit == None or len(server.clients) < server.client_limit:
            client = server.accept_tcp()
            client_thread = ClientThread(client, server)
            client_thread.start()
            server.clients.append(ThreadClient(client, client_thread))
    server.stop()

if __name__ == "__main__": # start the server if server.py has been run, otherwise we it's being imported
    try:
        start(opt.port, opt.cmax, opt.localhost, opt.climit)
    except Exception as error:
        if settings.Settings.mode == "Development":
            raise # crash the server in development mode
        l.log(f"Unexpected error: {error}", log.LogLevel.Error)
        sys.exit(1)