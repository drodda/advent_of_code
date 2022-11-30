#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


HEX_BIN = {
    "0": (0, 0, 0, 0),
    "1": (0, 0, 0, 1),
    "2": (0, 0, 1, 0),
    "3": (0, 0, 1, 1),
    "4": (0, 1, 0, 0),
    "5": (0, 1, 0, 1),
    "6": (0, 1, 1, 0),
    "7": (0, 1, 1, 1),
    "8": (1, 0, 0, 0),
    "9": (1, 0, 0, 1),
    "A": (1, 0, 1, 0),
    "B": (1, 0, 1, 1),
    "C": (1, 1, 0, 0),
    "D": (1, 1, 0, 1),
    "E": (1, 1, 1, 0),
    "F": (1, 1, 1, 1),
}


def next_n(iterator, n):
    """ Return the next n elements from iterator """
    return [next(iterator) for _ in range(n)]


def hex_to_bits(hex_str):
    """ Generator: yields bits from hex string big-endian """
    for item in hex_str.upper():
        for bit in HEX_BIN[item]:
            yield bit


def bin_to_int(bits):
    """ Convert a list of bits (1, 0) to integer """
    return int("".join(map(str, bits)), 2)


class Packet:
    def __init__(self, ver, typ, value=None):
        self.ver = ver
        self.typ = typ
        self.value = value
        self.packets = []

    def __repr__(self):
        return f"({self.value}, {self.packets})"

    def add_packet(self, packet):
        """ Add a sub-packet """
        self.packets.append(packet)

    def evaluate(self):
        """ Recursively evaluate packet and sub-packets """
        packets_values = [_packet.evaluate() for _packet in self.packets]
        if self.typ == 4:
            return self.value
        if self.typ == 0:
            return sum(packets_values)
        if self.typ == 1:
            result = 1
            for _val in packets_values:
                result = result * _val
            return result
        if self.typ == 2:
            result = packets_values[0]
            for _val in packets_values[1:]:
                result = min(result, _val)
            return result
        if self.typ == 3:
            result = packets_values[0]
            for _val in packets_values[1:]:
                result = max(result, _val)
            return result
        if self.typ == 5:
            return 1 if packets_values[0] > packets_values[1] else 0
        if self.typ == 6:
            return 1 if packets_values[0] < packets_values[1] else 0
        if self.typ == 7:
            return 1 if packets_values[0] == packets_values[1] else 0

    @classmethod
    def from_hex(cls, hex_str):
        """ Parse Packet (and sub-packets) from hex string """
        bits_gen = hex_to_bits(hex_str)
        return cls.from_bits(bits_gen)

    @classmethod
    def from_bits(cls, bits_gen):
        """ Parse Packet (and sub-packets) from binary data (as generator) """
        pkt_ver = bin_to_int(next_n(bits_gen, 3))
        pkt_type = bin_to_int(next_n(bits_gen, 3))
        packet = cls(pkt_ver, pkt_type)
        if pkt_type == 4:
            bits = []
            while True:
                new_bits = next_n(bits_gen, 5)
                bits.extend(new_bits[1:])
                if new_bits[0] == 0:
                    break
            packet.value = bin_to_int(bits)
        else:
            pkt_len_id = next_n(bits_gen, 1)[0]
            if pkt_len_id == 0:
                pkt_len = bin_to_int(next_n(bits_gen, 15))
                # Read bits from bits_gen, create a new iterator to parse sub-packets
                pkt_data = next_n(bits_gen, pkt_len)
                _bits_gen = iter(pkt_data)
                while True:
                    try:
                        _packet = cls.from_bits(_bits_gen)
                        packet.add_packet(_packet)
                    except StopIteration:
                        break
            else:
                pkts_len = bin_to_int(next_n(bits_gen, 11))
                # Sub-packets can be parsed directly from source bits_gen
                for i in range(pkts_len):
                    _packet = cls.from_bits(bits_gen)
                    packet.add_packet(_packet)
        return packet


def packet_add_version(packet):
    result = packet.ver + sum([packet_add_version(_packet) for _packet in packet.packets])
    return result


def main():
    data = open(data_file_path_main(test=False)).read()

    log.always("Part 1:")
    packet = Packet.from_hex(data)
    result = packet_add_version(packet)
    log.always(result)
    log.always("Part 2:")
    result = packet.evaluate()
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
