from message import Message
from util import *


def handle(message: Message):
    print("handling ping")
    return build_response(message.cid, message.cmd, message.data)
