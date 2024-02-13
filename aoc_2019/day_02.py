#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import VM


def patch_memory(mem, patch_values):
    mem = mem.copy()
    for k, v in patch_values.items():
        mem[k] = v
    return mem


class NoSolution(Exception):
    """ Raised if there is no solution found in find_vm_solution """
    pass


def find_vm_solution(mem, target):
    """ Find mem values 1 and 2 that will produce result target """
    for x in range(100):
        for y in range(100):
            vm = VM(patch_memory(mem, {1: x, 2: y}))
            vm.run()
            if vm.mem_load(0) == target:
                return x, y
    raise NoSolution(f"No combination of start values will produce result {target}")


###############################################################################


def main():
    args = parse_args()
    data = read_csv_int(input_file_path_main(test=args.test), to_list=True)

    # Patch program
    patch_mem_values = {} if args.test else {1: 12, 2: 2}

    log.always("Part 1")
    vm = VM(patch_memory(data, patch_mem_values))
    vm.run()
    log.always(vm.mem_load(0))

    if not args.test:
        log.always("Part 2")
        try:
            x, y = find_vm_solution(data, 19690720)
            result = 100 * x + y
            log.always(f"{x}, {y} = {result}")
        except NoSolution as e:
            log.always(e)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
