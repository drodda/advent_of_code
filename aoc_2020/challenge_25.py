#!/usr/bin/env python3
import traceback

from utils import *


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
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file, to_list=True)
    card_pub = int(lines[0])
    door_pub = int(lines[1])

    log_always("Part 1")
    log_verbose(gen_pubkey(DEFAULT_SN, 8))
    log_verbose(gen_pubkey(DEFAULT_SN, 11))

    # Brute force loop_size
    card_loop_size = brute_force_pubkey(DEFAULT_SN, card_pub)
    door_loop_size = brute_force_pubkey(DEFAULT_SN, door_pub)
    log_debug(f"Card loop size: {card_loop_size}")
    log_debug(f"Door loop size: {door_loop_size}")

    # Use loop size to generate encryption value
    card_val = gen_pubkey(door_pub, card_loop_size)
    door_val = gen_pubkey(card_pub, door_loop_size)
    log_always(f"Result: {card_val}  {door_val}")

    log_always("Part 2")
    log_always("There is no part 2")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
