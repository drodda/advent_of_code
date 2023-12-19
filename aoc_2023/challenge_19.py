#!/usr/bin/env python3

import collections
import math
import re
import sys
import traceback
from common.utils import *


SYMBOLS = "xmas"
PART_MIN = 1
PART_MAX = 4000
WORKFLOW_INITIAL = "in"
WORKFLOW_ACCEPT = "A"


def parse_workflows(lines):
    workflows = {}
    for line in lines:
        name, ruls_defn = line.strip("}").split("{")
        rules = []
        rule_strs = ruls_defn.split(",")
        for rule_str in rule_strs[:-1]:
            sym, operation, value_str, dest_workflow = re.split(r"([><])(\d+):", rule_str)
            value = int(value_str)
            if operation == "<":
                _range = range(PART_MIN, value)
            elif operation == ">":
                _range = range(value + 1, PART_MAX + 1)
            else:
                log.info(f"Workflow {line} Invalid operation: {operation}")
                _range = range(0)
            rules.append((sym, _range, dest_workflow))
        workflows[name] = (rules, rule_strs[-1])
    return workflows


def solve_part1(workflows, parts):
    result = 0
    for part in parts:
        workflow_name = WORKFLOW_INITIAL
        while workflow_name in workflows:
            rules, next_workflow_name = workflows[workflow_name]
            for rule in rules:
                sym, _range, dest_workflow_name = rule
                if part[sym] in _range:
                    next_workflow_name = dest_workflow_name
                    break
            workflow_name = next_workflow_name
        if workflow_name in WORKFLOW_ACCEPT:
            result += sum(part.values())
    return result


def range_invert(_range):
    if _range.start > 1:
        return range(1, _range.start)
    return range(_range.stop, PART_MAX + 1)


def range_intersect(_range1, _range2):
    return range(max(_range1.start, _range2.start), min(_range1.stop, _range2.stop))


def solve_part2(workflows):
    result = 0
    queue = collections.deque([("in",  {sym: range(PART_MIN, PART_MAX + 1) for sym in SYMBOLS})])
    while queue:
        workflow_name, part_range = queue.pop()
        if workflow_name == WORKFLOW_ACCEPT:
            # Accepted
            result += math.prod(len(_range) for _range in part_range.values())
        elif workflow_name in workflows:
            rules, default_workflow_name = workflows[workflow_name]
            for sym, _range, next_workflow_name in rules:
                syn_new_range = range_intersect(_range, part_range[sym])
                if syn_new_range:
                    new_part_range = part_range.copy()
                    new_part_range[sym] = syn_new_range
                    queue.append((next_workflow_name, new_part_range))
                sym_range_remaining = range_intersect(range_invert(_range), part_range[sym])
                if not sym_range_remaining:
                    break
                part_range[sym] = sym_range_remaining
            else:
                queue.append((default_workflow_name, part_range))
    return result


def main():
    args = parse_args()
    workflow_lines, part_lines = list(read_multilines(data_file_path_main(test=args.test)))
    workflows = parse_workflows(workflow_lines)
    parts = [
        {k: int(v) for k, v in [s.split("=") for s in line.strip("{}").split(",")]}
        for line in part_lines
    ]

    log.always("Part 1:")
    result = solve_part1(workflows, parts)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(workflows)
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
