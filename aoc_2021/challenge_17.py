#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


def simulate(vx, vy, x_max, y_min):
    x = 0
    y = 0
    while True:
        x += vx
        y += vy
        if x > x_max or y < y_min:
            break
        yield x, y
        vx -= 1 if vx > 0 else -1 if vx < 0 else 0
        vy -= 1


def main():
    args = parse_args()
    data = open(data_file_path_main(test=args.test)).read().strip()

    groups = re.match(r"target area: x=(-?[\d]+)..(-?[\d]+), y=(-?[\d]+)..(-?[\d]+)", data).groups()
    x1, x2, y1, y2 = list(map(int, groups))

    best_y = 0
    count = 0

    for vx in range(1, x2 + 1):
        for vy in range(y1, y2 + x2):
            coords = list(simulate(vx, vy, x2, y1))
            if not coords:
                continue
            x, y = coords[-1]
            if not (x1 <= x <= x2 and y1 <= y <= y2):
                continue
            count += 1
            max_y = max([coord[1] for coord in coords])
            best_y = max(best_y, max_y)
            log.info(f"{vx}, {vy} = {coords}, {max_y}")
            # break
    log.always("Part 1:")
    log.always(best_y)
    log.always("Part 2:")
    log.always(count)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
