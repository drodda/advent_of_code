#!/usr/bin/env python3

import sys
import traceback
import hashlib

from common.utils import *


def solve(data, prefix=""):
    i = 0
    while True:
        key = f"{data}{i}"
        _hash = hashlib.md5(key.encode()).hexdigest()
        log_debug(f"{i}: {key} => {_hash}")
        if _hash.startswith(prefix):
            return i
        i += 1


def main():
    args = parse_args()
    data = open(data_file_path_main(test=args.test)).read().strip()

    log_always("Part 1")
    result = solve(data, "00000")
    log_always(result)

    log_always("Part 2")
    result = solve(data, "000000")
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
