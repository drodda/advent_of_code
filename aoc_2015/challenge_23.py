#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


class VM:

    def __init__(self, lines, reg_a=0, reg_b=0):
        self.data = lines
        self.ip = 0
        self.regs = {
            "a": reg_a,
            "b": reg_b,
        }

    def step(self):
        operand1 = None
        try:
            opcode, operand0 = self.data[self.ip].split(" ", 1)
        except IndexError:
            raise StopIteration
        if "," in operand0:
            operand0, operand1 = operand0.split(", ")
        log_debug(f"{self.ip}: {opcode} {operand0} {operand1}: {self.regs}")
        if opcode == "hlf":
            self.regs[operand0] = int(self.regs[operand0] / 2)
        elif opcode == "tpl":
            self.regs[operand0] = self.regs[operand0] * 3
        elif opcode == "inc":
            self.regs[operand0] += 1
        elif opcode == "jmp":
            self.ip += int(operand0) - 1
        elif opcode == "jie":
            if self.regs[operand0] % 2 == 0:
                self.ip += int(operand1) - 1
        elif opcode == "jio":
            if self.regs[operand0] == 1:
                self.ip += int(operand1) - 1
        else:
            raise ValueError(f"Illegal instruction: {opcode}")
        self.ip += 1

    def run(self):
        try:
            while True:
                self.step()
        except StopIteration:
            pass


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)

    log_always("Part 1")
    vm = VM(lines)
    vm.run()
    result = vm.regs["a" if args.test else "b"]
    log_always(result)

    log_always("Part 2")
    vm = VM(lines, reg_a=1)
    vm.run()
    result = vm.regs["a" if args.test else "b"]
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
