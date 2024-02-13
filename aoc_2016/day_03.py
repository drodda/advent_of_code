#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def solve(data):
    result = 0
    for triangle in data:
        if (sum(triangle) - max(triangle)) > max(triangle):
            log.info(f"Valid: {triangle}")
            result += 1
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))
    data = [
        list(map(int, line.split()))
        for line in lines
    ]

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    data_part2 = []
    for i in range(0, len(data), 3):
        for j in range(len(data[0])):
            data_part2.append([data[i + n][j] for n in range(3)])

    log.always("Part 2:")
    result = solve(data_part2)
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
