#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


SNAFU_TO_DIGIT = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2
}
DIGIT_TO_SNAFU = {v: k for k, v in SNAFU_TO_DIGIT.items()}


def snafu_to_dec(s):
    base = 1
    result = 0
    for c in reversed(s):
        result += SNAFU_TO_DIGIT[c] * base
        base *= 5
    return result


def dec_to_snaf(v):
    snafu = []
    while v:
        v, res = divmod(v, 5)
        if res >= 3:
            v += 1
            res -= 5
        snafu.insert(0, DIGIT_TO_SNAFU[res])
    return "".join(snafu)


def solve(data):
    result = 0
    for i, line in enumerate(data):
        val = snafu_to_dec(line)
        log.debug(f"{i}\t{line}\t{val}")
        result += val
    log.debug(f"Result (decimal): {result}")
    return dec_to_snaf(result)


def main():
    args = parse_args()
    # dims, blizzards = parse_input(test=args.test)
    data = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    log.always("Part 2:")
    log.always("There is no part 2")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
