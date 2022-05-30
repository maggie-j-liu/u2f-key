from message import Message
from consts import *
from commands import init, msg


def handle(message: Message):
    if message.cmd == U2FHID_INIT:
        return init.handle(message)
    elif message.cmd == U2FHID_MSG:
        return msg.handle(message)
    elif message.cmd == U2FHID_PING or message.cmd == U2FHID_SYNC:
        print(f"Unimplemented command: {message.cmd}")
        return False
    else:  # unrecognized command
        response = bytearray(HID_RPT_SIZE)
        response[0:4] = message.cid.to_bytes(4, byteorder="big")
        response[4] = U2FHID_ERROR
        response[5:7] = (1).to_bytes(2, byteorder="big")
        response[7] = ERR_INVALID_CMD
        return [response]
