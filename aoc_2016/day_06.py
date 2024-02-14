#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


def solve(lines):
    result1 = ""
    result2 = ""
    for i in range(len(lines[0])):
        col = [line[i] for line in lines]
        counter = collections.Counter(col).most_common()
        result1 += counter[0][0]
        result2 += counter[-1][0]
    return result1, result2


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    result1, result2 = solve(lines)

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
