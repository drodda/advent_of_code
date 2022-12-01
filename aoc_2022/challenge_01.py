#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def main():
    args = parse_args()
    data = [list(map(int, item)) for item in read_multilines(data_file_path_main(test=args.test))]
    total = sorted([sum(l) for l in data], reverse=True)

    log.always("Part 1:")
    result = total[0]
    log.always(result)

    log.always("Part 2:")
    result = sum(total[:3])
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
