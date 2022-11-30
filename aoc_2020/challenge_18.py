#!/usr/bin/env python3

import sys
import traceback
import operator
import collections

from common.utils import *


# Mapping between operation symbol and operation
OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "^": operator.pow,
}


# Operation precedence: higher precedence operations happen first
PREC_DEFAULT = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "^": 2,
}
PREC_NONE = collections.defaultdict(int)
PREC_PLUS = collections.defaultdict(int, {"+": 1})


def parse_expression_reverse_polish(expr_str, prec=None):
    """ Convert an infix expression string expr_str to reverse polish. Apply operator ordering from prec """
    # Split sting into a list of tokens
    expr = split_tokens(expr_str)
    # Extract symbols between inner-most parenthesis and convert into a sub-list of symbols
    while "(" in expr:
        expr = group_parenthesis(expr)
    rp_expr = to_reverse_polish(expr, prec)
    return rp_expr


def split_tokens(expr_str):
    """ Split an expression into tokens """
    expr = expr_str.replace("(", " ( ").replace(")", " ) ").replace("+", " + ").replace("*", " * ").split()
    expr = [int(v) if v.isnumeric() else v for v in expr]
    return expr


def group_parenthesis(expr):
    """ Group the first inner-most symbols between parenthesis into a sub-list of symbols """
    # Find the last close parenthesis
    paren_end = expr.index(")")
    # The corresponding open is the last open before the first close
    paren_start = max([i for i in range(paren_end) if expr[i] == "("])
    # Extract the expression before, between, and after chosen parenthesis
    expr_between = expr[(paren_start + 1):paren_end]
    expr_before = expr[:paren_start]
    expr_after = expr[paren_end + 1:]
    # Make expr_between its own expression
    return expr_before + [expr_between] + expr_after


def to_reverse_polish(expr, prec=None):
    """ Convert an expression to reverse polish, using precedence rules in prec """
    if prec is None:
        prec = PREC_DEFAULT

    operation_stack = []
    result = []
    for token in expr:
        if isinstance(token, str):
            # Operation:
            if token not in OPERATIONS:
                raise RuntimeError(f"Invalid token: {token}")
            # Move operations that should already have been performed to result
            while operation_stack:
                if prec[operation_stack[-1]] < prec[token]:
                    break
                result.append(operation_stack.pop())
            # Add operation to pending operations
            operation_stack.append(token)
        else:
            # Literal, or sub-expression: add straight to result
            if isinstance(token, list):
                token = to_reverse_polish(token, prec)
            result.append(token)

    while operation_stack:
        result.append(operation_stack.pop())

    return result


def reverse_polish_calculator(rp_expr):
    """ Evaluate reverse polish expression rp_expr """
    stack = []
    # log.always(f"reverse_polish_calculator({rp_expr})")
    for token in rp_expr:
        if isinstance(token, int):
            stack.append(token)
        elif isinstance(token, list):
            # A sub-expression: evaluate it
            stack.append(reverse_polish_calculator(token))
        elif token in OPERATIONS:
            x = stack.pop()
            y = stack.pop()
            result = do_operate(x, y, token)
            stack.append(result)
    if len(stack) != 1:
        raise RuntimeError(f"Bad expression: {rp_expr} results in {stack}")
    return stack[0]


def do_operate(x, y, operation):
    """ Apply operation to x and y """
    return OPERATIONS[operation](x, y)


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file, to_list=True)

    # import ipdb; ipdb.set_trace()
    log.always("Part 1")
    part1_result = 0
    for line in lines:
        rp_expr = parse_expression_reverse_polish(line, PREC_NONE)
        result = reverse_polish_calculator(rp_expr)
        log.debug(f"{line} = {result}")
        part1_result += result
    log.always(part1_result)

    log.always()
    log.always("Part 2")
    part2_result = 0
    for line in lines:
        rp_expr = parse_expression_reverse_polish(line, PREC_PLUS)
        result = reverse_polish_calculator(rp_expr)
        log.debug(f"{line} = {result}")
        part2_result += result
    log.always(part2_result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
