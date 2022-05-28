import usb_hid
from consts import *
import os
from time import sleep
from util import *
from packets.initialization import InitializationPacket
from commands import init

device_path = "/dev/hidg0"

def write(bytes):
    with open(device_path, "rb+") as fd:
        fd.write(bytes)

def parse_packet(packet):
    print("parsing packet", packet, len(packet))
    cmd = packet[4]
    is_init = cmd >= 0x80 # bit 7 set
    print("is_init", is_init)
    cid = int.from_bytes(packet[:4], "big")
    if is_init:
        data_len = packet[5] << 8 | packet[6]
        segment_end = min(data_len + 7, 64)
        data = packet[7:segment_end]
        print(cid, cmd, data)
        initialization_packet = InitializationPacket(cid=1, cmd=cmd, data=data)
        response = init.handle(initialization_packet)
        write(response)

def read():
    report = None
    with open(device_path, "rb+") as fd:
        report = fd.read(64)
        print("report", f"b'{format_bytes(report)}'", None if report == None else len(report))
        if (len(report) == 64):
            parse_packet(report)
    return report

while (True):
    read()
    sleep(0.5)