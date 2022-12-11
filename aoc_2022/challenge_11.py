#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


class Monkey:
    def __init__(self, lines):
        # Monkey 0:
        self.num = int(lines[0].split(" ")[1].rstrip(":"))
        #   Starting items: 79, 98
        self.items = list(map(int, lines[1].split(": ")[1].split(", ")))
        #   Operation: new = old * 19
        self.operation = lines[2].split("new = ")[-1]
        #   Test: divisible by 23
        if not lines[3].startswith("  Test: divisible by "):
            log.error(f"ERROR: Monkey Test is not divisible? {lines[3]}")
        self.divisor = int(lines[3].split(" ")[-1])
        #     If true: throw to monkey 2
        self.dest_true = int(lines[4].split(" ")[-1])
        #     If false: throw to monkey 3
        self.dest_false = int(lines[5].split(" ")[-1])
        # Count of inspected items
        self.inspected = 0

    def step(self, monkeys, decrease_worry=True, worry_mod=None):
        _items = self.items
        self.items = []
        self.inspected += len(_items)
        for worry in _items:
            # Calculate new worry level
            _worry = eval(self.operation, None, {"old": worry})
            if decrease_worry:
                _worry = int(_worry / 3)
            if worry_mod is not None:
                _worry = _worry % worry_mod
            # Send item with new worry
            dest = self.dest_true if (_worry % self.divisor == 0) else self.dest_false
            log.info(f"  {self.num}: Inspected {worry}, became {_worry}, sending to {dest}")
            monkeys[dest].items.append(_worry)

    @classmethod
    def parse(cls, data):
        monkeys = {}
        for lines in data:
            monkey = cls(lines)
            monkeys[monkey.num] = monkey
        return monkeys


def solve(data, steps, decrease_worry=True):
    monkeys = Monkey.parse(data)
    worry_mod = 1
    for monkey in monkeys.values():
        worry_mod *= monkey.divisor

    for i in range(steps):
        log.info(f"\n\nRound: {i}")
        for num in sorted(monkeys.keys()):
            log.info(f"Monkey {num}")
            monkeys[num].step(monkeys, decrease_worry=decrease_worry, worry_mod=worry_mod)

    for monkey in monkeys.values():
        log.info(f"{monkey.num}: {monkey.inspected}")
    inspected = sorted([monkey.inspected for monkey in monkeys.values()], reverse=True)
    result = inspected[0] * inspected[1]
    return result


def main():
    args = parse_args()
    data = list(read_multilines(data_file_path_main(test=args.test)))

    log.always("Part 1:")
    result = solve(data, 20)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, 10000, decrease_worry=False)
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
