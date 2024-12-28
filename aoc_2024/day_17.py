#!/usr/bin/env python3

import math
import re
import sys
import traceback

from common.utils import *


def parse_input(args):
    registers = {}
    register_lines, program_lines = read_multilines(args.input)
    for line in register_lines:
        register, val_str = re.fullmatch(r"Register (.*): (\d+)", line).groups()
        registers[register] = int(val_str)
    program = list(map(int, ltrim("".join(program_lines), "Program: ").split(",")))
    return registers, program


class ChronospatialComputer:
    def __init__(self, registers, program, pc=0):
        self.registers = registers.copy()
        self.program = program
        self.pc = pc
        self.output = []

    def step(self):
        try:
            # Next PC
            pc = self.pc + 2
            if self.opcode == 0:  # adv
                self.registers["A"] = self.divide(self.operand)
            elif self.opcode == 1:  # bxl
                self.registers["B"] = self.registers["B"] ^ self.operand
            elif self.opcode == 2:  # bst
                self.registers["B"] = self.combo_operand % 8
            elif self.opcode == 3:  # jnz
                if self.registers["A"] != 0:
                    pc = self.operand
            elif self.opcode == 4:  # bxc
                self.registers["B"] = self.registers["B"] ^ self.registers["C"]
            elif self.opcode == 5:  # out
                self.output.append(self.combo_operand % 8)
            elif self.opcode == 6:  # bdv
                self.registers["B"] = self.divide(self.operand)
            elif self.opcode == 7:  # cdv:
                self.registers["C"] = self.divide(self.operand)
            self.pc = pc
        except IndexError:
            raise StopIteration

    @property
    def opcode(self):
        return self.program[self.pc]

    @property
    def operand(self):
        return self.program[self.pc + 1]

    OPERAND_REGISTER_MAP = {4: "A", 5: "B", 6: "C"}

    @property
    def combo_operand(self):
        if self.operand <= 3:
            return self.operand
        register = self.OPERAND_REGISTER_MAP.get(self.operand)
        if register is not None:
            return self.registers[register]
        raise RuntimeError(f"Bad operand {self.operand}")

    def divide(self, operand):
        return math.floor(self.registers["A"] / pow(2, self.combo_operand))

    def run(self):
        while True:
            try:
                self.step()
            except StopIteration:
                break
        return self.output


def solve_part1(registers, program):
    vm = ChronospatialComputer(registers, program)
    result = vm.run()
    return ",".join(map(str, result))


# Program:
# - 2,4, bst (B = A % 8)
# - 1,7, bxl (B = B xor 7)
# - 7,5, cdv (C = A / (2^B)))
# - 1,7, bxl (B = B xor 7)
# - 4,6, bxc (B = B xor C)
# - 0,3, adv (A = A / 8)
# - 5,5, out (output B % 8)
# - 3,0  jnz (A != 0: goto 0)

# Simplified Program:
# - b = a % 8
# - c = int(a / pow(2, b ^ 7))
# - output (b ^ c) % 8
# - a = int(a / 8)


def solve_part2(desired_result):
    # Find all possible values of a that can lead to expected output in reverse
    solutions = HeapQ()
    solutions.push((len(desired_result) - 1, 0))  # Index into desired_result, calculated a value
    while solutions:
        i, a = solutions.pop()
        if i == -1:
            return a
        a = a * 8
        for b in range(8):
            _a = a + b
            c = int(_a / pow(2, b ^ 7))
            output = (b ^ c) % 8
            if output == desired_result[i]:
                solutions.push((i - 1, _a))
    return None


def main():
    args = parse_args()
    registers, program = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(registers, program)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(program)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
