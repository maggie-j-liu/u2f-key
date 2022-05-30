from consts import *


def format_bytes(bytes_obj):
    return ''.join('\\x{:02x}'.format(b) for b in bytes_obj)


def build_response(cid, cmd, data):
    bcnt = len(data)
    packets = []
    init_packet = bytearray(HID_RPT_SIZE)
    init_packet[0:4] = cid.to_bytes(4, byteorder="big")
    init_packet[4] = cmd
    init_packet[5:7] = bcnt.to_bytes(2, byteorder="big")
    included = min(HID_RPT_SIZE - 7, bcnt)
    init_packet[7:7 + included] = data[:included]
    packets.append(init_packet)
    seq = 0
    while included < bcnt:
        cnt_packet = bytearray(HID_RPT_SIZE)
        cnt_packet[0:4] = cid.to_bytes(4, byteorder="big")
        cnt_packet[4] = seq
        to_include = min(HID_RPT_SIZE - 5, bcnt - included)
        cnt_packet[5:5 + to_include] = data[included:included + to_include]
        packets.append(cnt_packet)
        seq += 1
        included += to_include

    return packets
