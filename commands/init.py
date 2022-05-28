from consts import *
from util import *
from packets.initialization import InitializationPacket

def handle(packet: InitializationPacket):
    txt = input("type to simulate touching the key: ")
    print("you typed ", txt)
    response = bytearray(HID_RPT_SIZE)
    response[0:4] = CID_BROADCAST.to_bytes(4, byteorder="big") # cid
    print('cmd', packet.cmd)
    response[4] = packet.cmd # cmd
    response[5:7] = (17).to_bytes(2, byteorder="big") 
    response[7:15] = packet.data # nonce
    response[15:19] = packet.cid.to_bytes(4, byteorder="big") 
    response[19] = U2FHID_IF_VERSION # protocol version
    response[20] = 1 # major version
    response[21] = 0 # minor version
    response[22] = 1 # device version
    response[23] = 0 # capabilities
    print("sending init response", format_bytes(response))
    return response

