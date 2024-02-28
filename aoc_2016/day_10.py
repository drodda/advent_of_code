#!/usr/bin/env python3

import collections
import re
import sys
import traceback
from common.utils import *


RE_INITIAL = re.compile(r"value (\d+) goes to bot (\d+)")
RE_ACTION = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")


def solve(lines, target_tokens):
    state = collections.defaultdict(set)
    instructions = {}
    outputs = collections.defaultdict(list)
    for line in lines:
        if RE_INITIAL.fullmatch(line):
            value, bot = RE_INITIAL.fullmatch(line).groups()
            state[int(bot)].add(int(value))
        elif RE_ACTION.fullmatch(line):
            bot, dest_type_low, dest_low, dest_type_high, dest_high = RE_ACTION.fullmatch(line).groups()
            instructions[int(bot)] = [(dest_type_low, int(dest_low)), (dest_type_high, int(dest_high))]
        else:
            log.error(f"Unable to process: {line}")

    result1 = None
    while True:
        for bot, tokens in state.items():
            if len(tokens) == 2:
                if tokens == target_tokens and result1 is None:
                    log.info(f"Part 1: {bot} compares {target_tokens}")
                    result1 = bot
                for (dest_type, dest), token in zip(instructions[bot], sorted(tokens)):
                    if dest_type == "bot":
                        state[dest].add(token)
                    else:
                        outputs[dest].append(token)
                state[bot] = set()
                break
        else:
            # No more tokens to process
            break
    result2 = 1
    for output_name in range(3):
        for val in outputs[output_name]:
            result2 *= val
    return result1, result2


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    result1, result2 = solve(lines, {5, 2} if args.test else {61, 17})

    log.always("Part 1:")
    log.always(result1)

    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
