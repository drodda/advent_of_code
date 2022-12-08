#!/usr/bin/env python3

import sys
import traceback
import numpy as np
from common.utils import *


def parse_input(test=False):
    lines = read_lines(data_file_path_main(test=test))
    data = np.array([list(map(int, line)) for line in lines])
    return data


def visible_mask(row):
    """ Return list of trees visible on row from left """
    result = np.zeros(len(row), dtype=bool)
    result[0] = True
    tallest = row[0]
    for i in range(1, len(row)):
        if row[i] > tallest:
            result[i] = True
            tallest = row[i]
    return result


def solve_part1(data):
    result = np.zeros(data.shape, dtype=bool)
    for x in range(0, data.shape[0]):
        result[x, :] += visible_mask(data[x, :])
        result[x, :] += np.flip(visible_mask(np.flip(data[x, :])))
    for y in range(0, data.shape[1]):
        result[:, y] += visible_mask(data[:, y])
        result[:, y] += np.flip(visible_mask(np.flip(data[:, y])))
    return np.sum(result)


def solve_part2(data):
    result = 0
    for x in range(1, data.shape[0] - 1):
        for y in range(1, data.shape[1] - 1):
            # Calculate scenic score for position x, y
            height = data[x, y]
            _result = 1
            for row in [
                np.flip(data[:x, y]),  # Left
                data[x + 1:, y],  # Right
                np.flip(data[x, :y]),  # Up
                data[x, y + 1:],  # Down
            ]:
                for i, _height in enumerate(row):
                    n = i + 1
                    if _height >= height or n == len(row):
                        _result *= n
                        break
            result = max(result, _result)
    return result


def main():
    args = parse_args()
    data = parse_input(test=args.test)

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    # print(visible_neighbours(data, 3, 2))
    result = solve_part2(data)
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
