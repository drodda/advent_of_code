#!/usr/bin/env python3

import sys
import traceback
import numpy as np
import queue


from common.utils import *


def step(data):
    """ Run simulation a single step """
    x_max, y_max = data.shape
    # Increment every element
    data += 1
    # Flash those with value >= 9
    flashing = data > 9
    to_flash = queue.Queue()
    # Find elements that already need to flash
    for item in np.argwhere(flashing):
        to_flash.put(tuple(item))
    # Loop though elements that need to flash. This may cause more elements to flash
    while not to_flash.empty():
        x, y = to_flash.get()
        for _x in range(max(x - 1, 0), min(x + 2, x_max)):
            for _y in range(max(y - 1, 0), min(y + 2, y_max)):
                data[_x, _y] += 1
                if not flashing[_x, _y] and data[_x, _y] > 9:
                    flashing[_x, _y] = True
                    to_flash.put((_x, _y))
    data[flashing] = 0
    return np.sum(flashing)


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))
    data = np.array([list(map(int, line)) for line in lines])
    log.verbose(data)

    log.always("Part 1:")
    flash_count = 0
    _data = data.copy()
    for i in range(100):
        flash_count += step(_data)
        log.verbose(f"{i}:")
        log.verbose(_data)
    log.always(flash_count)

    log.always("Part 2:")
    # Loop until all elements flash (data == 0)
    _data = data.copy()
    i = 0
    while not np.all(_data == 0):
        i += 1
        step(_data)
    log.always(i)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
