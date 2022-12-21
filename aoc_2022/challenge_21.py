#!/usr/bin/env python3

from collections import deque
import sys
import traceback
from common.utils import *


"""
Each line of the input is in the form:
    cczh: sllz + lgvd
or
    dbpl: 5

These can be considered equations of the form
    r = expr
Where expr is an expression that may be a constant, or may be and operation (+-*/) applied to two variables
    r = a op b
"""


INVERSE_OPS = {
    "*": "/",
    "/": "*",
    "+": "-",
    "-": "+",
}


def solve_part1(data):
    q = deque(data)
    vals = {}
    while q:
        line = q.popleft()
        r, expr = line.split(": ")
        try:
            vals[r] = eval(expr, None, vals)
            log.debug(f"solved: {line}")
        except NameError:
            # Can't solve, push onto unsolved queue to try again next time
            q.append(line)
    return int(vals["root"])


def solve_part2(data):
    vals = {}
    unsolved = set([line for line in data if not line[:4] in ["root", "humn"]])
    while True:
        # Try so solve as many as possible
        _unsolved = set()
        blocked = True
        for line in unsolved:
            r, expr = line.split(": ")
            try:
                vals[r] = eval(expr, None, vals)
                log.debug(f"solved: {line}")
                blocked = False
            except NameError:
                # Can't solve, push onto unsolved queue to try again next time
                _unsolved.add(line)
        if blocked:
            break
        unsolved = _unsolved
    # Reverse root: both components are equal
    root_line = [line for line in data if line.startswith("root")][0]
    a, _, b = root_line.split(": ")[-1].split(" ")
    if a in vals:
        vals[b] = vals[a]
    else:
        vals[a] = vals[b]
    # Solve the remaining unsolved equations in reverse
    q = deque(unsolved)
    while q:
        line = q.popleft()
        r, expr = line.split(": ")
        a, op, b = expr.split(" ")
        # Check if reverse equation is solvable
        if r in vals and (a in vals or b in vals):
            # Reverse the equation
            _op = INVERSE_OPS[op]
            if b in vals:  # Solve for a
                _r = a
                _val = f"{r} {_op} {b}"
            else:  # a in vals, solve for b
                _r = b
                if op in ["*", "+"]:
                    _val = f"{r} {_op} {a}"
                else:
                    _val = f"{a} {op} {r}"
            # Solve
            vals[_r] = eval(_val, None, vals)
        else:
            # Can't solve now, try later
            q.append(line)
    return int(vals["humn"])


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
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
