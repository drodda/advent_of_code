#!/usr/bin/env python3

import math
import sys
import traceback

from common.utils import *


def factors(n):
    result = [i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
    result += [int(n / d) for d in result[::-1] if n != d * d]
    return result


def presents_1(_factors):
    return sum(_factors) * 10


def presents_2(_factors):
    return sum([d for d in _factors if _factors[-1] / d <= 50]) * 11


def main():
    args = parse_args()
    value = int(open(input_file_path_main(test=args.test)).read())

    i = 1
    result_1 = None
    result_2 = None
    while result_1 is None or result_2 is None:
        _factors = factors(i)
        if result_1 is None and presents_1(_factors) >= value:
            result_1 = i
        if result_2 is None and presents_2(_factors) >= value:
            result_2 = i
        i += 1

    log.always("Part 1")
    log.always(result_1)

    log.always("Part 2")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
