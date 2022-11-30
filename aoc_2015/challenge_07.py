#!/usr/bin/env python3

import collections
import sys
import traceback

from common.utils import *


def evaluate(operand, values):
    if operand.isnumeric():
        return int(operand)
    return values[operand]


class Instruction:
    def __init__(self, s):
        self.str = s
        _input, self.output = s.split(" -> ")
        self.input = _input.split(" ")
        self.requires = set([item for item in self.input if item.islower() and not item.isnumeric()])

    def satisfied(self, values=None):
        known = set() if values is None else set(values.keys())
        return self.requires.issubset(known)

    def solve(self, values):
        result = None
        if len(self.input) == 1:
            result = evaluate(self.input[0], values)
        elif len(self.input) == 2:
            if self.input[0] == "NOT":
                result = ~evaluate(self.input[1], values)
        elif len(self.input) == 3:
            if self.input[1] == "AND":
                result = evaluate(self.input[0], values) & evaluate(self.input[2], values)
            elif self.input[1] == "OR":
                result = evaluate(self.input[0], values) | evaluate(self.input[2], values)
            elif self.input[1] == "RSHIFT":
                result = evaluate(self.input[0], values) >> evaluate(self.input[2], values)
            elif self.input[1] == "LSHIFT":
                result = evaluate(self.input[0], values) << evaluate(self.input[2], values)
        if result is None:
            raise ValueError(f"Bad instruction: {self.str}")
        return result & 65535

    def __str__(self):
        return self.str

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.str}>"


def run(instructions, values=None):
    values = {} if values is None else values.copy()
    satisfied = set()
    unsatisfied = set()
    depends = collections.defaultdict(set)
    for instruction in instructions:
        if instruction.output in values:
            log.debug(f"Skipping: {instruction}")
            continue
        if instruction.satisfied(values):
            satisfied.add(instruction)
        else:
            unsatisfied.add(instruction)
            for k in instruction.requires:
                depends[k].add(instruction)

    # Solve
    while satisfied:
        instruction = satisfied.pop()
        log.debug(f"Satisfiable: {instruction}")
        k = instruction.output
        values[k] = instruction.solve(values)
        log.debug(f"Values: {values}")
        for _instruction in depends[k]:
            if _instruction in unsatisfied and _instruction.satisfied(values):
                log.debug(f"\tCan now be solved: {_instruction}")
                unsatisfied.remove(_instruction)
                satisfied.add(_instruction)

    return values


def solve(lines):
    instructions = [Instruction(line) for line in lines]
    values = run(instructions)
    result_1 = values.get("a")
    _values = None
    if result_1 is not None:
        _values = {"b": result_1}
    values = run(instructions, _values)
    result_2 = values.get("a")
    return result_1, result_2


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))

    result_1, result_2 = solve(lines)

    log.always("Part 1")
    log.always(result_1)

    log.always("Part 2")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
