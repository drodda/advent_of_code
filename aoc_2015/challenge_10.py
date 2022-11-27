#!/usr/bin/env python3

import itertools
import sys
import traceback

from common.utils import *


def iterate(val, n=1, verbose=False):
    if verbose:
        log_always(f"0: {val}")
    for i in range(n):
        val = "".join(["{}{}".format(len(list(g)), k) for k, g in itertools.groupby(val)])
        if verbose:
            log_always(f"{i + 1}: {val}")
    return val


def main():
    args = parse_args()
    val = open(data_file_path_main(test=args.test)).read().strip()
    n1 = 5 if args.test else 40
    n2 = 50 - n1

    log_always("Part 1")
    _val = iterate(val, n1, args.test and args.verbose)
    log_always(len(_val))

    log_always("Part 2")
    _val = iterate(_val, n2)
    log_always(len(_val))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
