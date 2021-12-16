#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from utils import *


BLACK = 0
WHITE = 1
TRANSPARENT = 2


def main():
    args = parse_args()
    data_raw = list(map(int, open(data_file_path_main(test=args.test)).read().strip()))
    log_verbose(data_raw)

    width = 3 if args.test else 25
    height = 2 if args.test else 6
    min_layer_zeros = None
    min_layer_score = None
    # Create final layer that is all transparent
    image = np.full((height, width), TRANSPARENT)
    for _layer in np.reshape(data_raw, (-1, width*height)):
        layer = np.reshape(_layer, (height, width))
        log_verbose(layer)
        # Part 1: Count zeros
        layer_zeros = np.sum(layer == 0)
        if min_layer_zeros is None or layer_zeros < min_layer_zeros:
            min_layer_zeros = layer_zeros
            min_layer_score = np.sum(layer == 1) * np.sum(layer == 2)
        # Part 2: Update image from layer where image is transparent
        indices = np.where(image == TRANSPARENT)
        image[indices] = layer[indices]
    log_always("Part 1:")
    log_always(min_layer_score)
    log_always("Part 2:")
    # log_always(image)
    for row in image:
        line = ""
        for pixel in row:
            line += "\u25A0" if pixel == WHITE else " "
        log_always(line)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
