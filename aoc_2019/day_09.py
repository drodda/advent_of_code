#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import *


###############################################################################


def main():
    args = parse_args()
    lines = read_lines(args.input)
    data = [list(map(int, line.split(","))) for line in lines]

    log.always("Part 1")
    for item in data:
        log.info(list_pretty(item))
        vm = VM(item, input_queue=[1])
        vm.run()
        log.always(list(vm.output.queue))

    log.always("Part 2")
    for item in data:
        log.info(list_pretty(item))
        vm = VM(item, input_queue=[2])
        vm.run()
        log.always(list(vm.output.queue))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
