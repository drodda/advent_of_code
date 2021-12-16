#!/usr/bin/env python3

import sys
import traceback

from utils import *


class ExecutionException(Exception):
    pass


class ExecutionInfiniteLoop(ExecutionException):
    def __init__(self):
        super().__init__("Infinite Loop")


class ExecutionCompleted(ExecutionException):
    def __init__(self):
        super().__init__("Execution Completed")


class ExecutionError(ExecutionException):
    def __init__(self, msg=None):
        msg_extra = f": {msg}" if msg else ""
        super().__init__(f"Execution Error{msg_extra}")


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
        log_verbose(f"{self.ip}: {self.acc}: {instruction[0]} {instruction[1]}")
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
    log_always("Part 1:")
    try:
        vm.run()
    except ExecutionInfiniteLoop:
        log_always(f"{vm.acc}")
    except ExecutionException as e:
        log_always(f"Execution finished: {e}")

    log_always()
    log_always("Part 2:")
    if args.test:
        if args.test:
            lines = read_lines(data_file_path("test", "b"))
            vm = VM(lines)
            try:
                vm.run()
            except ExecutionInfiniteLoop:
                log_always(f"{vm.acc}")
            except ExecutionException as e:
                log_always(f"Execution finished: {e}")

    # Find instructions that were used in the infinite loop in Part 1
    used_instructions = [i for i in range(len(vm.instructions)) if vm.instruction_seen(vm.get_instruction(i))]
    for i in used_instructions:
        instruction = vm.get_instruction(i)
        action_orig = instruction[0]
        if action_orig in ["jmp", "nop"]:
            # Swap instruction and run
            try:
                action_new = action_swap(action_orig)
                instruction[0] = action_new
                vm.reset()
                vm.run()
            except ExecutionCompleted:
                log_always(f"Swap {i} {action_new}->{action_orig}: Execution completed")
                log_always(f"{vm.acc}")
                break
            except ExecutionException as e:
                log_debug(f"Swap {i} {action_new}->{action_orig}: {e}")
            instruction[0] = action_orig


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
