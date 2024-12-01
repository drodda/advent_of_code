#!/usr/bin/env python3

import itertools
import sys
import traceback

from common.utils import *


def iterate(val, n=1, verbose=False):
    if verbose:
        log.always(f"0: {val}")
    for i in range(n):
        val = "".join(["{}{}".format(len(list(g)), k) for k, g in itertools.groupby(val)])
        if verbose:
            log.always(f"{i + 1}: {val}")
    return val


def main():
    args = parse_args()
    val = open(args.input).read().strip()
    n1 = 5 if args.test else 40
    n2 = 50 - n1

    log.always("Part 1")
    _val = iterate(val, n1, args.test and args.verbose)
    log.always(len(_val))

    log.always("Part 2")
    _val = iterate(_val, n2)
    log.always(len(_val))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
