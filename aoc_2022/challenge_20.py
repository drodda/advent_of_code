#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def simulate(data, reps=1):
    indices = list(range(len(data)))
    log.debug(f"Initial data: {[data[x] for x in indices]}")
    for rep in range(reps):
        log.info(f"Round {rep + 1} of {reps}")
        for i, n in enumerate(data):
            index = indices.index(i)
            indices = indices[:index] + indices[index + 1:]
            new_index = (index + n) % len(indices)
            indices.insert(new_index, i)
        log.debug(f"Round {rep + 1} of {reps}: {[data[x] for x in indices]}")
    return [data[x] for x in indices]


def solve_part1(data):
    vals = simulate(data)
    index = vals.index(0)
    result = 0
    for i in [1000, 2000, 3000]:
        result += vals[(index + i) % len(vals)]
    return result


def solve_part2(data):
    _data = [x * 811589153 for x in data]
    vals = simulate(_data, 10)
    index = vals.index(0)
    result = 0
    for i in [1000, 2000, 3000]:
        result += vals[(index + i) % len(vals)]
    return result


def main():
    args = parse_args()
    data = read_list_int(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
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
