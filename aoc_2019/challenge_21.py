#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import *


PROGRAM_1 = [  # (!A or !B or !C) and D
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "WALK",
]

PROGRAM_2 = [  # (!A or !B or !C) and D and (E or H)
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
    "RUN",
]


def solve(data, program):
    program_str = "\n".join(program) + "\n"
    program_bytes = list(map(ord, program_str))
    vm = VM(data, program_bytes)
    vm.run()
    output = list(vm.output.queue)
    result = None
    if output and output[-1] > 255:
        result = output[-1]
        output = output[:-1]
    for line in "".join(map(chr, output)).splitlines():
        log_info(f"> {line}")
    return result


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    data = list(map(int, lines[0].split(",")))

    log_always("Part 1")
    result = solve(data, PROGRAM_1)
    log_always(result)

    log_always("Part 2")
    result = solve(data, PROGRAM_2)
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
