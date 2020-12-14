#!/usr/bin/env python3

import traceback
import json
import itertools
# import numpy as np

from utils import *


LEN = 36
MASK_PASS = "X"


# Part 1


def to_bin_pad(val, padded_len=LEN):
    result = "{0:b}".format(val)
    result = "0" * (padded_len - len(result)) + result
    return result


def apply_bitmask_bin(bitmask, val_bin):
    result = "".join([val_bin[i] if bitmask[i] == MASK_PASS else bitmask[i] for i in range(LEN)])
    return result


def apply_bitmask(bitmask, val):
    val_bin = to_bin_pad(val)
    print_verbose(val_bin)
    result = apply_bitmask_bin(bitmask, val_bin)
    print_verbose(result)
    return int(result, 2)


# Part 2


def expand_floating_bitmask(bitmask):
    floating_bits = [(LEN - i - 1) for i in range(LEN) if bitmask[i] == MASK_PASS]
    floating_options = [(0, pow(2, i)) for i in floating_bits]
    floating_combinations = itertools.product(*floating_options)
    floating_addresses = [sum(combo) for combo in floating_combinations]
    print_verbose(f"{bitmask} => {floating_bits} ==> {floating_addresses}")
    return floating_addresses


def expand_floating_address(bitmask, address):
    bitmask_base = "".join("1" if c == "1" else "0" for c in bitmask)
    bitmask_inv = "".join("0" if c == MASK_PASS else "1" for c in bitmask)
    address_base = address & int(bitmask_inv, 2) | int(bitmask_base, 2)
    floating_addresses = expand_floating_bitmask(bitmask)
    return [address_base + float_address for float_address in floating_addresses]


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    data = read_lines(data_file, to_list=True)

    print_verbose(data)

    print("Part 1")
    bitmask = MASK_PASS * LEN
    mem = {}
    for line in data:
        print_verbose(line)
        inst, operand = line.split(" = ")
        if inst == "mask":
            bitmask = operand
        elif inst.startswith("mem"):
            address = int(ltrim(rtrim(inst, "]"), "mem["))
            val = apply_bitmask(bitmask, int(operand))
            mem[address] = val

    print(sum(mem.values()))
    print_debug()

    print("Part 2")
    bitmask = MASK_PASS * LEN
    mem = {}
    for line in data:
        print_verbose(line)
        inst, operand = line.split(" = ")
        if inst == "mask":
            bitmask = operand
        elif inst.startswith("mem"):
            address = int(ltrim(rtrim(inst, "]"), "mem["))
            val = int(operand)
            for float_address in expand_floating_address(bitmask, address):
                mem[float_address] = val
                print_verbose(f"{float_address} => {val}")
    if args.verbose:
        print(json.dumps(mem, indent=2))
    print(sum(mem.values()))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
