import usb_hid
from consts import *
import os
from time import sleep
from util import *
from commands.handle import handle
from message import Message

device_path = "/dev/hidg0"

current_message = None


def write(bytes):
    with open(device_path, "rb+") as fd:
        fd.write(bytes)


def parse_packet(packet):
    global current_message
    print("parsing packet", packet, len(packet))
    cmd = packet[4]
    is_init = cmd >= 0x80  # bit 7 set
    if is_init:  # is an initialization packet
        if current_message == None:  # we are not currently processing anything
            current_message = Message(packet)
        else:
            print("busy :(")  # TODO: send an error response
    else:  # is a continuation packet
        if current_message == None:
            raise Exception(
                "Spurious continuation packet without initialization packet")
        else:
            cid = int.from_bytes(packet[:4], "big")
            if cid == current_message.cid:
                current_message.process_cont_packet(packet)
    if current_message != None and current_message.done:
        # handle message
        response = handle(current_message)
        current_message = None
        if response:
            write(response)


def read():
    report = None
    with open(device_path, "rb+") as fd:
        report = fd.read(64)
        if (len(report) == 64):
            parse_packet(report)
    return report


while (True):
    read()
    sleep(0.5)
