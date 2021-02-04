#!/usr/bin/env python3

import traceback
import operator
import copy

from utils import *


class VM:
    def __init__(self, mem, patch_mem_values=None, input_values=None):
        self.mem = copy.copy(mem)
        self.ip = 0
        if patch_mem_values:
            for k, v in patch_mem_values.items():
                self.mem[k] = v
        self.output = []
        self.input = copy.copy(input_values or [])

    def decode_instruction(self):
        """ Decode instruction at self.ip and return opcode and modes """
        # Convert to str and pad
        instruction_str = str(self.mem[self.ip]).zfill(5)
        # Extract digits
        mode_3 = int(instruction_str[0])
        mode_2 = int(instruction_str[1])
        mode_1 = int(instruction_str[2])
        opcode = int(instruction_str[3:])
        return opcode, mode_1, mode_2, mode_3

    def operand(self, n):
        """ Get the nth operand """
        return self.mem[self.ip + n]

    def load(self, mode, operand):
        """ Load value based on mode: True = literal, False = dereference memory """
        if mode:
            return operand
        return self.mem[operand]

    def put(self, mode, operand, val):
        """ Put value in memory at operand """
        if mode:
            raise RuntimeError("Can not put in immediate mode")
        self.mem[operand] = val

    OPERATIONS_LLS = {
        # Load-Load-Store operations that take 3 params: p3 = operator(p1, p2)
        1: operator.add,
        2: operator.mul,
        7: lambda v1, v2: int(operator.lt(v1, v2)),
        8: lambda v1, v2: int(operator.eq(v1, v2)),
    }
    OPERATORS_EVAL_JUMP = {
        # Load+Eval?Jump operations: Evaluate condition on p1 and (conditionally) jump to p2
        5: bool,
        6: lambda c: not bool(c),
    }

    def step(self):
        opcode, mode_1, mode_2, mode_3 = self.decode_instruction()
        next_ip = self.ip + 1
        if opcode == 99:
            raise StopIteration
        elif opcode in self.OPERATIONS_LLS:
            # Load-Load-Store operations that take 3 params: p3 = operator(p1, p2)
            next_ip += 3
            operation = self.OPERATIONS_LLS[opcode]
            p1 = self.load(mode_1, self.operand(1))
            p2 = self.load(mode_2, self.operand(2))
            p3 = self.operand(3)
            result = operation(p1, p2)
            self.put(mode_3, p3, result)
        elif opcode == 3:
            # Input -> p1
            next_ip += 1
            self.put(mode_1, self.operand(1), self.input.pop(0))
        elif opcode == 4:
            # p1 -> Output
            next_ip += 1
            p1 = self.operand(1)
            v = self.load(mode_1, p1)
            self.output.append(v)
            log_debug(f"OUTPUT: ip {self.ip} addr {p1} val {v}")
        elif opcode in self.OPERATORS_EVAL_JUMP:
            # Load+Eval?Jump operations: Evaluate condition on p1 and (conditionally) jump to p2
            next_ip += 2
            condition = self.OPERATORS_EVAL_JUMP[opcode]
            p1 = self.load(mode_1, self.operand(1))
            p2 = self.load(mode_2, self.operand(2))
            if condition(p1):
                next_ip = p2
        else:
            raise RuntimeError(f"Invalid instruction: {self.mem[self.ip]} at {self.ip}")
        self.ip = next_ip

    def run(self):
        try:
            log_verbose(f"{self.ip}: {self.mem}")
            while True:
                self.step()
                log_verbose(f"{self.ip}: {self.mem}")
        except StopIteration:
            pass
        return self.mem[0]


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

    log_always("Part 1")
    vm = VM(data, input_values=[1])
    vm.run()
    log_always(vm.output)

    log_always("Part 2")
    vm = VM(data, input_values=[5])
    vm.run()
    log_always(vm.output)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
