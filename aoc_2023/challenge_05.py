#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def solve(transforms, seeds):
    result = sys.maxsize
    for seed in seeds:
        _result = seed
        for transform in transforms:
            for dest_start, src_start, _range in transform:
                if src_start <= _result <= src_start + _range:
                    _result = _result - src_start + dest_start
                    break
        log.info(f"{seed} = {_result}")
        result = min(result, _result)
    return result


def expand_seeds(seeds):
    for seed_start, seed_range in grouper(seeds, 2):
        log.info(f"{seed_start}:{seed_range}")
        for i in range(seed_range):
            yield seed_start + i


def main():
    args = parse_args()
    data = read_multilines(data_file_path_main(test=args.test))
    header = next(data)
    seeds = list(map(int, header[0].split("seeds: ", 1)[1].split(" ")))

    transforms = []
    for lines in data:
        transform = [
            list(map(int, line.split(" ")))
            for line in lines[1:]
        ]
        transforms.append(transform)

    log.always("Part 1:")
    result = solve(transforms, seeds)
    log.always(result)

    log.always("Part 2:")
    result = solve(transforms, expand_seeds(seeds))
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
