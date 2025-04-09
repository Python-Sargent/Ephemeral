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

"""
def unpack(message):
    payloads = []
    #data_type = message[0]
    #header = message[1:4]
    header = message[:4]
    current_size = 0
    skip = 0
    for i in range(1, int(len(message)/4)): # search each nibble
        if skip > 0:
            skip -= 1
            continue
        nibble = message[i*4:i*4+4]
        if current_size == 0: # size nibble?
            current_size = int(message[i*4:i*4+8], 2) + 1
            payloads.append("")
            skip = 1
        else:
            payloads[len(payloads)-1] += (nibble)
            current_size -= 1
    #return data_type, header, payloads
    return header, payloads

def pack(header, payloads):
    message = str(bin(header))[2:].zfill(4)
    for payload in payloads:
        message += str(bin(int(len(payload)/4)))[2:].zfill(8) + str(payload)
        # This monstrosity is a joke, here is how it works:
        # len_of_payload = len(payload) # size in bits
        # size = int(len_of_payload/4) # turns it into the length in nibbles
        # str_size = str(size)[2:] # convert to string and remove the 0b
        # str_size_nibbles = str_size.zfill(8) # make the size two nibbles (a byte)
        # message += str_size_nibbles + payload # add the payload section to the final message
    return message
"""

def payld(payload):
    content = bytearray()
    content.append(len(payload))
    for i in range(len(payload)):
        content.append(int(payload[i]))
    return content

def pack(header, payloads): # takes array of integers
    content = bytearray()
    content.append(header)
    for payload in payloads:
        content.extend(payld(payload))
    return content

def unpack(content, out=0): # returns an array of integers
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
        return str(payload)

#print(pack(0b0001, ["000000000000", "0000000000000000"]))