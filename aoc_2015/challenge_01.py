#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def main():
    args = parse_args()
    data = open(data_file_path_main(test=args.test)).read().strip()

    log.always("Part 1")
    result = data.count("(") - data.count(")")
    log.always(result)

    log.always("Part 2")
    level = 0
    result = None
    for i, c in enumerate(data):
        level += 1 if c == "(" else -1 if c == ")" else 0
        if level == -1:
            result = i + 1
            break
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
