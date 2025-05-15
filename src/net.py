# python 3.13
#
# Ephemeral Networking
# 

import socket
import src.log as log

class Network:
    class Requests:
        SERVER_GET_INFO = 0b00
        CLIENT_AUTH = 0b01
        CLIENT_INPUT = 0b10
        CLIENT_END = 0b11
    class Headers: # headers follow this format: first number is datatype, next three are header
        # COMMON HEADERS
        DEBUG_MESSAGE = 0b0000
        UPDATE_CHAT = 0b0110
        UPDATE_CONNECTION = 0b0111
        # SERVER HEADERS
        DATA_TILEMAP = 0b0001
        DATA_OBJECTMAP = 0b0010
        DATA_FEATUREMAP = 0b0011
        UPDATE_OBJECT = 0b0101
        MODIFY_OBJECT = 0b0011
        SERVER_INFO = 0b1001
        # CLIENT HEADERS
        CLIENT_REQUEST = 0b1000 # client is requesting data (payload specifies what the request is)
    class Messages:
        # Update Connection Header
        CONNECTION_END = 0b0
        CONNECTION_ESTABLISHED = 0b1
        # Client Auth
        AUTH_DENIAL = 0b0
        AUTH_HANDSHAKE = 0b1
    PROTOCOL_TCP = 0b0
    PROTOCOL_UDP = 0b1

def check_addr(a):
    try: socket.inet_aton(a); return "IPv4"
    except: pass
    try: socket.inet_pton(socket.AF_INET6, a); return "IPv6"
    except: pass
    return False

class NetAddress:
    def __init__(self, addr):
        try:
            self.ip = addr[0]
            self.port = addr[1]
        except:
            #log.log("Invalid address tuple provided to NetAddress in object creation", log.LogLevel.Error)
            raise ValueError("Invalid address (requires tuple)")
        self.addr = addr
        self.protocol = check_addr(self.ip)

class Client:
    def __init__(self, addr, sock: socket.socket):
        if type(addr) == type(str()):
            self.ip = addr
        elif type(addr) == type(tuple()):
            self.address = NetAddress(addr)
            self.ip = self.address.ip
        else:
            self.addr = addr
        self.sock = sock
    def send(self, content):
        try:
            self.sock.sendall(content)
        except socket.error as e:
            log.log(e, log.LogLevel.Error)
    def close(self):
        r = True
        try:
            self.sock.sendall(pack(Network.Headers.UPDATE_CONNECTION, [Network.Messages.CONNECTION_END,]))
        except:
            r = False
        self.sock.close()
        return r

"""
def unpack(message):
    payloads = []
    #data_type = message[0]
    #header = message[1:4]
    header = message[:4]
    current_size = 0
    skip = 0
    for i in range(1, int(len(message)/4)): # search each nybble
        if skip > 0:
            skip -= 1
            continue
        nybble = message[i*4:i*4+4]
        if current_size == 0: # size nybble?
            current_size = int(message[i*4:i*4+8], 2) + 1
            payloads.append("")
            skip = 1
        else:
            payloads[len(payloads)-1] += (nybble)
            current_size -= 1
    #return data_type, header, payloads
    return header, payloads

def pack(header, payloads):
    message = str(bin(header))[2:].zfill(4)
    for payload in payloads:
        message += str(bin(int(len(payload)/4)))[2:].zfill(8) + str(payload)
        # This monstrosity is a joke, here is how it works:
        # len_of_payload = len(payload) # size in bits
        # size = int(len_of_payload/4) # turns it into the length in nybbles
        # str_size = str(size)[2:] # convert to string and remove the 0b
        # str_size_nybbles = str_size.zfill(8) # make the size two nybbles (a byte)
        # message += str_size_nybbles + payload # add the payload section to the final message
    return message
"""

def payld(payload):
    if type(payload) == type(bytes()) or type(payload) == type(bytearray()) or type(payload) == type(list()) and len(payload) >= 1 and type(payload[0]) == type(int()):
        content = bytearray()
        content.append(len(payload))
        for i in range(len(payload)):
            content.append(int(payload[i]))
        return content
    elif type(payload) == type(int()):
        content = bytearray()
        payload_bytes = bytearray()
        for n in payload:
            payload_bytes.append(n)
        content.append(len(payload_bytes).to_bytes(1))
        content.extend(payload_bytes)
        return content
    else:
        return bytearray()

def pack(header, payloads): # takes array of integers or bytes objects
    content = bytearray()
    content.append(header)
    for payload in payloads:
        content.extend(payld(payload))
    return content

def unpack(content, out=0): # returns an array of integers or bytes
    if len(content) <= 0: raise ValueError("Cannot unpack empty bytearray")
    content = bytearray(content)
    header = content[0]
    content.pop(0)
    payloads = []
    current_size = 0
    for i in range(len(content)):
        byte = content[i]
        if current_size == 0:
            current_size = int(byte)
            payloads.append(list([]))
        else:
            o = None
            if out == 0: o = int(byte)
            elif out == 1: o = byte
            payloads[len(payloads)-1].append(o)
            current_size -= 1
    return header, payloads


def payload_str(header, payload):
    if header == Network.Headers.DEBUG_MESSAGE:
        b = bytearray()
        for i in payload:
            b.append(i)
        return b.decode("utf-8")
    else:
        p = ""
        if type(payload) == type(list()):
            for v in payload:
                p += str(v)
        else:
            p = str(payload)
        return p

#print(pack(0b0001, ["000000000000", "0000000000000000"]))