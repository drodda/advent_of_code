#!/usr/bin/env python3

import json
import sys
import traceback

from common.utils import *


def sum_numbers(obj, ignore_red=False):
    result = 0
    if isinstance(obj, dict):
        if not (ignore_red and "red" in obj.values()):
            for v in obj.values():
                result += sum_numbers(v, ignore_red=ignore_red)
    elif isinstance(obj, list):
        for v in obj:
            result += sum_numbers(v, ignore_red=ignore_red)
    elif isinstance(obj, int):
        result += obj
    return result


def main():
    args = parse_args()
    with open(data_file_path_main(test=args.test)) as f:
        data = json.load(f)

    log_always("Part 1")
    result = sum_numbers(data)
    log_always(result)

    log_always("Part 2")
    result = sum_numbers(data, ignore_red=True)
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
