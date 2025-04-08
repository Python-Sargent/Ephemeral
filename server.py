import socket
import sys
import src.net as net
import threading

class ServerClient:
    def __init__(self, ip, sock):
        self.ip = ip
        self.sock = sock

class ThreadingClient(ServerClient):
    def __init__(self, client, thread):
        super().__init__(client.ip, client.sock)
        self.thread = thread

class Server:
    port = 2048
    client_max = 4
    host = socket.gethostbyname(socket.gethostname())
    multicast_group = "224.8.8.8"
    version = "0.1.0"
    client_limit = None
    clients = []
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    should_continue = True
    #clients = list([])
    def create(self, host=None, port=None):
        if host != None: self.host = host
        if port != None: self.port = port
        try:
            self.tcp.bind((self.host, self.port))
        except socket.error as e:
            str(e)
    def listen(self):
        self.tcp.listen(self.client_max)
    def accept_tcp(self):
        commsock, ip = self.tcp.accept()
        print("Client connected at " + str(ip))
        return ServerClient(ip, commsock)
    def get_info(self):
        payloads = []
        payloads.append(self.host.encode("utf-8"))
        payloads.append(self.version.encode("utf-8"))
        return payloads
    def handle_request(self, client, msg):
        header, payloads = net.unpack(msg)
        if header == net.Network.Headers.CLIENT_REQUEST:
            request = None
            if len(payloads) >= 1: request = payloads[0]
            match request:
                case net.Network.Requests.SERVER_GET_INFO:
                    return net.pack(net.Network.Headers.SERVER_INFO, self.get_info(self))
        return None
    #def recv_bytes(self, protocol, ip):
    #    if protocol == net.Network.PROTOCOL_TCP:
    #        for i in range(len(self.clients)):
    #            if self.clients[i].ip == ip:
    #                return self.clients[i].sock.recv(1024).decode("utf-8")
    #    elif protocol == net.Network.PROTOCOL_UDP:
    #        #return self.udp.recv()
    #        print("UDP not supported"
    #def recv_str(self, protocol, ip):
    #    if protocol == net.Network.PROTOCOL_TCP:
    #        for i in range(len(self.clients)):
    #            if self.clients[i].ip == ip:
    #                return self.clients[i].sock.recv(1024).decode("utf-8")
    #    elif protocol == net.Network.PROTOCOL_UDP:
    #        #return self.udp.recv()
    #        print("UDP not supported")
    #def close(self, ip):
    #    for i in range(len(self.clients)):
    #        if self.clients[i].ip == ip:
    #            self.clients[i].sock.close()
    #            self.clients.pop(i)

def threaded_tcpclient(client):
    client.sock.sendall(net.pack(net.Network.Headers.DEBUG_MESSAGE, ["Hello from server".encode("utf-8")]))
    while True:
        try:
            msg = client.sock.recv(2048)
            response = Server.handle_request(Server, client, msg)
            if response != None: client.sock.sendall(response)
            header, payloads = net.unpack(msg)
            sh = str(bin(int(header)))[2:]
            ps = ""
            for payload in payloads:
                ps += net.payload_str(header, payload) + "\n"
            print(f"Recieved from client << Header: {sh}, Payloads: {ps}")
        except RuntimeError as e:
            print(f"Error: {e}")
            break

    print(f"Connection with {client.ip} was closed.")
    client.sock.close()

options = sys.argv[1:]

options_len = len(options)
options_it = iter(options)

for op in options_it:
    match op:
        case "":
            pass
        case "--localhost":
            Server.host = "127.0.0.1"
        case "--port":
            port = next(options_it)
            if port and port != "":
                port = int(port)
                Server.port = port
        case "--client-max":
            limit = next(options_it)
            if limit and limit != "":
                limit = int(limit)
                Server.client_max = limit
        case "--client-limit":
            limit = next(options_it)
            if limit and limit != "":
                limit = int(limit)
                Server.client_limit = limit

if len(options) > 0:
    print(f"Running server with options: \nPort: {Server.port}\nHost: {Server.host}\nMaximum Waiting Clients: {Server.client_max}\nClient Limit: {Server.client_limit}")

def start(custom_port=None, custom_client_max=None, localhost_override=None, client_limit=None):
    if custom_port != None: Server.port = custom_port
    if custom_client_max != None: Server.client_max = custom_client_max
    if localhost_override != None and localhost_override == True: Server.host = "127.0.0.1"
    if client_limit != None: Server.client_limit = client_limit

    Server.create(Server)

    Server.listen(Server)

    while Server.should_continue is True:
        if Server.client_limit == None or len(Server.clients) < Server.client_limit:
            client = Server.accept_tcp(Server)
            client_thread = threading.Thread(None, threaded_tcpclient, "TCP_THREAD_"+str(len(Server.clients)), (client,), {}) # None, func, name, args, kwargs, *, daemon
            client_thread.daemon = True
            client_thread.start()
            Server.clients.append(ThreadingClient(client, client_thread))

            #thread_id = start_new_thread(threaded_tcpclient, (client,))

if __name__ == "__main__": # start the server if server.py has been run, otherwise we know it's being imported
    start()