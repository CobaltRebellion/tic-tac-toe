import json

def packet_complete(packet_buffer):
    length = packet_buffer[0:2]
    length = int.from_bytes(length, 'big')

    dataLength = len(packet_buffer) - 2

    if dataLength >= length:
        return True
    else:
        return False
    
def get_next_packet(s, packet_buffer):
    """
    Return the next json packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    try: 

        while not packet_complete(packet_buffer):
            packet_buffer += s.recv(5)
            if not packet_buffer:
                return None

        length = packet_buffer[0:2]
        length = int.from_bytes(length, 'big')

        packetEnd = 2 + length
        packet = packet_buffer[0:packetEnd]

        packet_buffer = packet_buffer[packetEnd:]

        return(packet)
    
    # probably bad to do this, will figure out another way to make this work with /q maybe rearanging certain things
    except:
        return None

def extract_json(json_packet):
    """
    Extract json from a packet.

    Returns the word decoded as a string.
    """

    length = json_packet[0:2]
    length = int.from_bytes(length, 'big')

    data = json_packet[2:]

    converted_json = json.loads(data.decode())

    return converted_json

def build_packet(json):
    packet = b''

    json_bytes = json.encode()
    json_len = len(json_bytes)
    json_len_bytes = json_len.to_bytes(2, "big")
    packet += json_len_bytes + json_bytes

    return packet