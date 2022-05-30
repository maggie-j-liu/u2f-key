from consts import *
from util import *
from message import Message


def handle(message: Message):
    message.cid = 1
    bcnt = 17
    data = bytearray(bcnt)
    data[0:8] = message.data  # nonce
    data[8:12] = message.cid.to_bytes(4, byteorder="big")
    data[12] = U2FHID_IF_VERSION  # protocol version
    data[13] = 1  # major version
    data[14] = 0  # minor version
    data[15] = 1  # device version
    data[16] = 0  # capabilities
    response = build_response(CID_BROADCAST, message.cmd, data)
    print("sending init response", [format_bytes(r) for r in response])
    return response
