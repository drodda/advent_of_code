#!/usr/bin/env python3

import sys
import traceback
import queue

from common.utils import *


SYM_MAP = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

PART1_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

PART2_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))

    result1 = 0
    part2_scores = []
    for i, line in enumerate(lines):
        stack = queue.LifoQueue()
        valid = True
        for j, sym in enumerate(line):
            if sym in SYM_MAP:
                # Push close symbol to stack
                stack.put(SYM_MAP[sym])
            else:
                if stack.empty():
                    log_info(f"{i}- {j}: Got symbol {sym}. Stack is empty")
                    valid = False
                    break
                _sym = stack.get()
                if _sym != sym:
                    log_info(f"{i} - {j}: Expected {_sym}, but found {sym} instead.")
                    result1 += PART1_SCORE[sym]
                    valid = False
                    break
        if valid:
            missing = "".join(reversed(list(stack.queue)))
            log_info(f"{i}: Incomplete. Missing {missing}")
            part2_score = 0
            while not stack.empty():
                sym = stack.get()
                part2_score = part2_score * 5 + PART2_SCORE[sym]
            part2_scores.append(part2_score)
    log_always("Part 1:")
    log_always(result1)
    log_always("Part 2:")
    log_always(sorted(part2_scores)[round(len(part2_scores)/2)])


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
