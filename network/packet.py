# PACKET TYPES
#
# 0 -> connect
#   -> args: 16-byte UUID
#   ->     : 15-byte username
#   -> reply: 0xFF 0x00 for error, 0x01 {player ID} for success
# 1 -> info
#   -> args: none
#   -> reply: packet 1: packet count (player data)
#   ->      : packet n: player ID, X/Y coords (16-bit each), appearance (4-bit RGB + 4-bit hat ID), 3-bit rotation
# 2 -> move
#   -> args: 16-bit X, 16-bit Y, 3-bit angle
#   -> reply: 0x01 XX YY A for success, 0xFF XX YY A for error (XX YY are server-side coords)
# 3 -> equip
#   -> args: 4-bit item index
#   -> reply: 0x01 for success, 0xFF for error
# 4 -> pickup
#   -> args: 4-bit item ID, 16-bit X, 16-bit Y
#   -> reply: 0x01 for success, 0xFF for error
# 5 -> drop
#   -> args: 4-bit item index, 16-bit X, 16-bit Y
#   -> reply: 0x01 for success, 0xFF for error
# 6 -> send chat
#   -> args: packet 1: length (up to 64 packets, so max chat length is (65 * 32) - 1) (2079)
#   -> reply: 0x01 for success, 0xFF for error
# 7 -> recieve chat
#   -> args: only recieving
#   -> reply: packet 1: length (1 byte) + chat data
#   ->        packet n: chat data
# 8 -> disconnect
#   -> args: none
#   -> reply: none

import math

class PacketEncodeError(Exception):
    pass

def encode_packet(type, data):
    if (len(data)) >= 32: raise(PacketEncodeError)
    packet = bytearray([type]) + data
    diff = 32 - len(packet)
    if (diff > 0):
        packet += bytes([0xFF]) * diff
    return packet

def decode_packet(packet_data):
    ptype = packet_data[0]

    match (ptype):
        case 2:
            x = int.from_bytes(packet_data[1:3], signed=True)
            y = int.from_bytes(packet_data[3:5], signed=True)
            a = int.from_bytes(packet_data[5] & 0b111)
            return {
                "x": x,
                "y": y,
                "r": a
            }
        
        case _:
            return packet_data[1:]

def hexdump(data):
    for i in range(len(data)):
        if i % 16 == 0: print()
        print(hex(data[i])[2:].zfill(2).upper(), end=" ")
    
    print()

def gen_chat_packets(chat_message):
    chat_message = chat_message.encode("UTF-8")
    packet_num = math.ceil((len(chat_message) - 31) / 32) + 1
    first_packet = chat_message[:31]
    packets = [
        encode_packet(7, first_packet)
    ]
    print(chat_message)
    for i in range(packet_num):
        start_index = i * 32
        end_index = (i + 1) * 32
        packets.append(chat_message[start_index:end_index])
    
    diff = 32 - len(packets[-1])
    if (diff > 0):
        packets[-1] += bytes([0xFF]) * diff
    
    return packets