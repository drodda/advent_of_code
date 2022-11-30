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
        log.debug(f"{i}: {key} => {_hash}")
        if _hash.startswith(prefix):
            return i
        i += 1


def main():
    args = parse_args()
    data = open(data_file_path_main(test=args.test)).read().strip()

    log.always("Part 1")
    result = solve(data, "00000")
    log.always(result)

    log.always("Part 2")
    result = solve(data, "000000")
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
