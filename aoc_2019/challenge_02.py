#!/usr/bin/env python3

import traceback
import operator
import copy

from utils import *


class VM:
    def __init__(self, mem, patch_mem_values=None):
        self.mem = copy.copy(mem)
        self.ip = 0
        if patch_mem_values:
            for k, v in patch_mem_values.items():
                self.mem[k] = v

    def step(self):
        instruction = self.mem[self.ip]
        if instruction == 99:
            raise StopIteration
        elif instruction == 1:
            self._do_operation(operator.add)
        elif instruction == 2:
            self._do_operation(operator.mul)
        else:
            raise RuntimeError(f"Invalid instruction: {self.mem[self.ip]} at {self.ip}")

    def run(self):
        try:
            while True:
                self.step()
                print_verbose(f"{self.ip}: {self.mem}")
        except StopIteration:
            pass
        return self.mem[0]

    def _do_operation(self, operation):
        addr_a = self.mem[self.ip + 1]
        addr_b = self.mem[self.ip + 2]
        addr_c = self.mem[self.ip + 3]
        a = self.mem[addr_a]
        b = self.mem[addr_b]
        result = operation(a, b)
        self.mem[addr_c] = result
        self.ip += 4
        print_verbose(f"{operation.__name__} {addr_a} ({a}) {addr_b} ({b}) => {addr_c} ({result})")


class NoSolution(Exception):
    """ Raised if there is no solution found in find_vm_solution """
    pass


def find_vm_solution(mem, target):
    """ Find mem values 1 and 2 that will produce result target """
    for x in range(100):
        for y in range(100):
            vm = VM(mem, {1: x, 2: y})
            result = vm.run()
            if result == target:
                return x, y
    raise NoSolution(f"No combination of start values will produce result {target}")


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    data = open(data_file).read()
    data = list(map(int, data.split(",")))

    # Patch program
    patch_mem_values = {} if args.test else {1: 12, 2: 2}

    print("Part 1")
    vm = VM(data, patch_mem_values)
    result = vm.run()
    print(result)

    if not args.test:
        print("Part 2")
        try:
            x, y = find_vm_solution(data, 19690720)
            result = 100 * x + y
            print(f"{x}, {y} = {result}")
        except NoSolution as e:
            print(e)



if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
