#!/usr/bin/env python3

import sys
import traceback

from utils import *

TARGET_SUM = 2020


def main():
    args = parse_args()
    data = list(read_list_int(data_file_path_main(test=args.test)))

    log_always("Part 1:")
    for i, x in enumerate(data):
        for j, y in enumerate(data[i+1:]):
            if x + y == TARGET_SUM:
                log_always(f"Candidate: {x} * {y} = {x*y}")

    log_always("Part 2:")
    for i, x in enumerate(data):
        for j, y in enumerate(data[i+1:]):
            for k, z in enumerate(data[j + 1:]):
                if x + y + z == TARGET_SUM:
                    log_always(f"Candidate: {x} * {y} * {z} = {x*y*z}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
