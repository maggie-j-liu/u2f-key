import usb_hid
from consts import *
import os
from time import sleep

# DEVICE_DESCRIPTOR = bytes((
#     0x06,  0xD0,  0xF1,	        #   Usage Page (F1D0h),         
#     0x09,  0x01,				#   Usage (01h),                
#     0xA1,  0x01,				#   Collection (Application),   
#     0x09,  0x20,				#       Usage (20h),            
#     0x15,  0x00,				#       Logical Minimum (0),    
#     0x26,  0xFF,  0x00,	        #       Logical Maximum (255),  
#     0x75,  0x08,				#       Report Size (8),        
#     0x95,  0x40,				#       Report Count (64),      
#     0x81,  0x02,				#       Input (Variable),       
#     0x09,  0x21,				#       Usage (21h),            
#     0x15,  0x00,				#       Logical Minimum (0),    
#     0x26,  0xFF,  0x00,	        #       Logical Maximum (255),  
#     0x75,  0x08,				#       Report Size (8),        
#     0x95,  0x40,				#       Report Count (64),      
#     0x91,  0x02,				#       Output (Variable),      
#     0xC0						#   End Collection              
# ))
# \\x06\\xD0\\xF1\\x09\\x01\\xA1\\x01\\x09\\x20\\x15\\x00\\x26\\xFF\\x00\\x75\\x08\\x95\\x40\\x81\\x02\\x09\\x21\\x15\\x00\\x26\\xFF\\x00\\x75\\x08\\x95\\x40\\x91\\x02\\xC0
# Set up a keyboard device.

# device = usb_hid.Device(
#     descriptor=DEVICE_DESCRIPTOR,
#     report_ids=(0,),
#     in_report_lengths=(8,), 
#     out_report_lengths=(8,),
#     usage_page=0x1,
#     usage=0x6,
# )
# usb_hid.enable((device,))

# device.send_report(bytearray(8))

device_path = "/dev/hidg0"

# arr = bytearray(64)
# arr[0] = 9 
# print(arr)
# with open(device_path, "rb+") as fd:
    # fd.write(arr)

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

# while True:
#     read()
#     cnt += 1
#     if cnt == 8:
#         break
#     sleep(0.5)

# arr = bytearray(64)
# arr[0] = U2FHID_ERROR
# arr[1] = 1
# arr[2] = ERR_INVALID_CMD
# print(arr)
# write(arr)

while True:
    read()
    sleep(0.5)