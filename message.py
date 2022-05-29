from util import *


class Message:
    def __init__(self, packet):
        self.cid = int.from_bytes(packet[:4], "big")
        self.cmd = packet[4]
        self.data_len = packet[5] << 8 | packet[6]
        if self.data_len <= 64 - 7:
            # no continuation packets
            self.done = True
            self.data_cursor = self.data_len
        else:
            # will have continuation packets
            self.done = False
            self.data_cursor = 64 - 7
        self.data = bytearray(self.data_len)
        self.data[:self.data_cursor] = packet[7:7 + self.data_cursor]
        self.next_cont_packet = 0
        print("initialization packet", self.cid,
              self.cmd, format_bytes(self.data))

    def process_cont_packet(self, packet):
        if self.done:
            raise Exception(
                "Continuation packet sent when message is already done")

        cid = int.from_bytes(packet[:4], "big")
        if cid != self.cid:
            raise Exception(
                f"Cid doesn't match: initial {self.cid}, current {cid}")

        seq = packet[4]
        if seq != self.next_cont_packet:
            raise Exception("Continuation packet sent out of order")

        data = packet[5:]
        bytes_needed = self.data_len - self.data_cursor
        data_end = min(len(data), bytes_needed)
        self.data[self.data_cursor:self.data_cursor +
                  data_end] = data[:data_end]
        self.data_cursor += len(data)
        self.done = self.data_cursor == self.data_len
        if not self.done:
            self.next_cont_packet = seq + 1
        print("continuation packet", self.cid,
              self.cmd, format_bytes(self.data))
