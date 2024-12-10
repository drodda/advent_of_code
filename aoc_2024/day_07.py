#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(input_path):
    result = []
    for line in read_lines(input_path):
        total, inputs = line.split(": ", 1)
        result.append((int(total), list(map(int, inputs.split()))))
    return result


def evaluate(inputs, concat=False):
    *head, tail = inputs
    if len(head) != 1:
        head = evaluate(head, concat=concat)
    for _result in head:
        yield _result + tail
        yield _result * tail
        if concat:
            yield int(str(_result) + str(tail))


def solve(data, concat=False):
    result = 0
    for total, inputs in data:
        for _total in evaluate(inputs, concat=concat):
            if total == _total:
                result += total
                break
    return result


def main():
    args = parse_args()
    data = parse_input(args.input)

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, concat=True)
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
