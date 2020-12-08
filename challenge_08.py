#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb
import re
import json
import numpy as np
import string

from utils import *




# def parse_input(filename):
#     lines = read_lines(filename, strip_empty=True)
#     return [parse_instruction(line) for line in lines]


class ExecutionInfiniteLoop(Exception):
    pass


class ExecutionCompleted(Exception):
    pass


class ExecutionError(Exception):
    pass


class VM:
    def __init__(self, lines):
        self.instructions = [self.parse_instruction(line) for line in lines]
        self.ip = 0
        self.ip_count = 0
        self.acc = 0

    def step(self):
        instruction = self.get_instruction()
        # Check for infinite loop
        if self.instruction_seen(instruction):
            raise ExecutionInfiniteLoop
        print_debug(f"{self.ip}: {self.acc}: {instruction[0]} {instruction[1]}")
        # Mark as run
        self.instruction_set_seen(instruction)
        instruction[2] = True
        self.ip_count += 1
        # Do instruction
        if instruction[0] == "nop":
            self.ip += 1
        elif instruction[0] == "acc":
            self.acc += instruction[1]
            self.ip += 1
        elif instruction[0] == "jmp":
            self.ip += instruction[1]
        else:
            raise RuntimeError(f"Unknown instruction: {instruction}")

    def get_instruction(self, ip=None):
        if ip is None:
            ip = self.ip
        n_instructions = len(self.instructions)
        if ip == n_instructions:
            raise ExecutionCompleted
        if ip > n_instructions:
            raise ExecutionError
        return self.instructions[ip]

    def instruction_seen(self, instruction=None):
        if instruction is None:
            instruction = self.get_instruction()
        return instruction[2]

    def instruction_set_seen(self, instruction=None, seen=True):
        if instruction is None:
            instruction = self.get_instruction()
        instruction[2] = seen

    def run(self):
        while True:
            self.step()

    def reset(self):
        for instruction in self.instructions:
            self.instruction_set_seen(instruction, False)
        self.ip = 0
        self.ip_count = 0
        self.acc = 0

    @staticmethod
    def parse_instruction(line):
        inst, inc = line.split()
        return [inst, int(inc), False]


def action_swap(action):
    if action == "jmp":
        return "nop"
    if action == "nop":
        return "jmp"
    return action


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    vm = VM(lines)
    print("Part 1:")
    try:
        vm.run()
    except ExecutionInfiniteLoop:
        print(f"{vm.acc}")
    except ExecutionCompleted:
        print(f"Execution completed??")
    except ExecutionError:
        print(f"Execution Error??")

    print()
    print("Part 2:")
    if args.test:
        if args.test:
            lines = read_lines(data_file_path("test", "b"))
            vm = VM(lines)

    for i, instruction in enumerate(vm.instructions):
        action_orig = instruction[0]
        if action_orig in ["jmp", "nop"]:
            # Swap instruction and run
            try:
                instruction[0] = action_swap(action_orig)
                vm.reset()
                vm.run()
            except ExecutionInfiniteLoop:
                print(f"Swap {i}: ExecutionInfiniteLoop")
            except ExecutionError:
                print(f"Swap {i}: ExecutionError")
            except ExecutionCompleted:
                print(f"Swap {i}: Execution completed")
                print(f"{vm.acc}")
                break
            instruction[0] = action_orig


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
