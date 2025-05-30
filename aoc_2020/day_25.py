#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


MOD = 20201227
DEFAULT_SN = 7


###############################################################################


def gen_pubkey(sn, loop_size):
    return pow(sn, loop_size, MOD)


def brute_force_pubkey(sn, pubkey):
    val = 1
    for i in range(MOD):
        if val == pubkey:
            return i
        val = val * sn
        val = val % MOD


###############################################################################


def main():
    args = parse_args()
    data_file = args.input
    lines = read_lines(data_file, to_list=True)
    card_pub = int(lines[0])
    door_pub = int(lines[1])

    log.always("Part 1")
    log.verbose(gen_pubkey(DEFAULT_SN, 8))
    log.verbose(gen_pubkey(DEFAULT_SN, 11))

    # Brute force loop_size
    card_loop_size = brute_force_pubkey(DEFAULT_SN, card_pub)
    door_loop_size = brute_force_pubkey(DEFAULT_SN, door_pub)
    log.debug(f"Card loop size: {card_loop_size}")
    log.debug(f"Door loop size: {door_loop_size}")

    # Use loop size to generate encryption value
    card_val = gen_pubkey(door_pub, card_loop_size)
    door_val = gen_pubkey(card_pub, door_loop_size)
    log.always(f"Result: {card_val}  {door_val}")

    log.always("Part 2")
    log.always("There is no part 2")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
