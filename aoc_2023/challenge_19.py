#!/usr/bin/env python3

import re
import sys
import traceback
from common.utils import *


def evaluate(rule, parts):
    result = None
    for _rule in rule:
        if ":" in _rule:
            name, comparator, val_str, dest = re.split(r"([><])(\d+):", _rule)
            val = int(val_str)
            compared = parts[name]
            if (comparator == ">" and compared > val) or (comparator == "<" and compared < val):
                result = dest
                break
        else:
            result = _rule
            break
    if result == "A":
        return True
    elif result == "R":
        return False
    return result


def solve(rules, parts):
    result = 0
    for part in parts:
        _result = "in"
        while _result not in [True, False]:
            if _result not in rules:
                log.error(f"Rule {_result} doesnt exist")
                _result = None
                break
            _result = evaluate(rules[_result], part)
        if _result:
            result += sum(part.values())
    return result


def main():
    args = parse_args()
    rules_lines, parts_lines = list(read_multilines(data_file_path_main(test=args.test)))
    rules = {
        k: v.split(",")
        for k, v in [line.strip("}").split("{") for line in rules_lines]
    }

    parts = [
        {k: int(v) for k, v in [s.split("=") for s in line.strip("{}").split(",")]}
        for line in parts_lines
    ]

    log.always("Part 1:")
    result = solve(rules, parts)
    log.always(result)

    # log.always("Part 2:")
    # result = solve(data)
    # log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
