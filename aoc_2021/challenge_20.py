#!/usr/bin/env python3

import sys
import traceback
from collections import defaultdict

from common.utils import *


def factory_0():
    """ Factory that returns 0 """
    return 0


def factory_1():
    """ Factory that returns 1 """
    return 1


def neighbours(x, y):
    """ Yield all neighbours of coordinate x,y """
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            yield x + dx, y + dy


def image_value(image_data, x, y):
    """ Calculate the value of an image pixel at x,y using the surrounding pixels """
    val_str = "".join([str(int(image_data[coord])) for coord in neighbours(x, y)])
    return int(val_str, 2)


def image_enhance(image_data, image_enhancement_algorithm):
    """ Apply image_enhancement_algorithm to image_data """
    # Set default of new image from previous image default and image_enhancement_algorithm
    default_value = image_enhancement_algorithm[-1] if image_data.default_factory() else image_enhancement_algorithm[0]
    result = defaultdict(factory_1 if default_value else factory_0)

    x_min = min([x for x, y in image_data])
    x_max = max([x for x, y in image_data])
    y_min = min([y for x, y in image_data])
    y_max = max([y for x, y in image_data])
    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            result[(x, y)] = image_enhancement_algorithm[image_value(image_data, x, y)]
    return result


def main():
    args = parse_args()
    data_raw = list(read_multilines(data_file_path_main(test=args.test)))
    image_enhancement_algorithm = [1 if val == "#" else 0 for val in data_raw[0][0]]
    image_data = defaultdict(factory_0)
    for y, line in enumerate(data_raw[1]):
        for x, c in enumerate(line):
            image_data[(x, y)] = True if c == "#" else False

    log.always("Part 1:")
    for i in range(2):
        image_data = image_enhance(image_data, image_enhancement_algorithm)
    log.always(sum(image_data.values()))

    log.always("Part 2:")
    for i in range(48):
        image_data = image_enhance(image_data, image_enhancement_algorithm)
    log.always(sum(image_data.values()))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)

