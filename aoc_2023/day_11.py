#!/usr/bin/env python3
import itertools
import sys
import traceback
from common.utils import *


def solve(data, scale=1):
    galaxies = []
    galaxy_ys = set()
    galaxy_xs = set()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "#":
                galaxies.append((y, x))
                galaxy_ys.add(y)
                galaxy_xs.add(x)
    result = 0
    for galaxy_a, galaxy_b in itertools.combinations(galaxies, 2):
        y1, y2 = sorted((galaxy_a[0], galaxy_b[0]))
        x1, x2 = sorted((galaxy_a[1], galaxy_b[1]))
        dist = (y2 - y1) + (x2 - x1) + (scale - 1) * (len([y for y in range(y1 + 1, y2) if y not in galaxy_ys]) + len([x for x in range(x1 + 1, x2) if x not in galaxy_xs]))
        log.debug(f"{galaxy_a} -> {galaxy_b} = {dist}")
        result += dist
    return result


def main():
    args = parse_args()
    data = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(data, scale=2)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, scale=(100 if args.test else 1000000))
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
