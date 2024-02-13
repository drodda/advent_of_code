#!/usr/bin/env python3
import hashlib
import sys
import traceback
from common.utils import *


def solve(seed):
    result1 = ""
    result2 = [None] * 8
    i = 0
    while len(result1) < 8 or None in result2:
        md5hash = hashlib.md5(f"{seed}{i}".encode()).hexdigest()
        if md5hash.startswith("0" * 5):
            log.info(f"{i: 10d} {md5hash[:8]}")
            if len(result1) < 8:
                result1 += md5hash[5]
            index = int(md5hash[5], 16)
            if index < len(result2) and result2[index] is None:
                result2[index] = md5hash[6]
        i += 1
    return result1, "".join(result2)


def main():
    args = parse_args()
    with open(input_file_path_main(test=args.test)) as f:
        seed = f.read().strip()

    result1, result2 = solve(seed)

    log.always("Part 1:")
    log.always(result1)

    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
