import usb_hid
from consts import *
import os
from time import sleep

device_path = "/dev/hidg0"

cnt = 0
def read():
    report = None
    with open(device_path, "rb+") as fd:
        report = fd.read(64)
        print("report", "b'{}'".format(''.join('\\x{:02x}'.format(b) for b in report)), None if report == None else len(report))
    return report
def write(bytes):
    with open(device_path, "rb+") as fd:
        fd.write(bytes)

while True:
    read()
    sleep(0.5)