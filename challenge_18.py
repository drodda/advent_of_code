#!/usr/bin/env python3
import traceback

from utils import *


def split_expression(expr):
    """ Extract symbols between parenthesis and convert into a sub-list of symbols """
    while "(" in expr:
        expr = group_parenthesis(expr)
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
    # Make expr_between its own expression. Recursively group expr_before and expr_after
    return expr_before + [expr_between] + expr_after


def split_tokens(expr_str):
    """ Split an expression into tokens """
    return expr_str.replace("(", " ( ").replace(")", " ) ").replace("+", " + ").replace("*", " * ").split()


def evaluate_expression(expr_str, priority_operation=None):
    """ Evaluate an expression from a string
        If priority_operation is supplied, evaluate that operation first
    """
    expr_tokens = split_tokens(expr_str)
    expr = split_expression(expr_tokens)
    result = _evaluate_expression(expr, priority_operation)
    return result


def _evaluate_expression(expr, priority_operation=None):
    """ Recursively evaluate elements from an expression """
    if isinstance(expr, int):
        return expr
    if isinstance(expr, str):
        # Literal
        return int(expr)
    if len(expr) == 1:
        # Literal OR sub-expression: evaluate
        return _evaluate_expression(expr[0], priority_operation)
    # print(f"EVAL: {_expr} for {priority_operation}")

    if priority_operation is not None:
        while len(expr) > 3 and priority_operation in expr:
            index = expr.index(priority_operation)
            before = expr[:index - 1]
            first = expr[index - 1]
            second = expr[index + 1]
            after = expr[index + 2:]
            priority_result = _evaluate(first, second, priority_operation, priority_operation)
            expr = before + [priority_result] + after

    # No priorities left: evaluate left to right
    while len(expr) >= 3:
        first, operation, second, *rest = expr
        partial_result = _evaluate(first, second, operation, priority_operation)
        expr = [partial_result] + rest
    # expr is now a single element - return it
    return expr[0]


def _evaluate(first, second, operation, priority_operation=None):
    """ Evaluate a single operation between first and second params """
    # Evaluate first and second params
    first = _evaluate_expression(first, priority_operation)
    second = _evaluate_expression(second, priority_operation)

    # Perform operation on (evaluated) first and second
    if operation == "+":
        return first + second
    elif operation == "*":
        return first * second
    raise ValueError(f"Unknown operation: {operation}")


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file, to_list=True)

    # import ipdb; ipdb.set_trace()
    print("Part 1")
    part1_result = 0
    for line in lines:
        result = evaluate_expression(line)
        print_debug(f"{line} = {result}")
        part1_result += result
    print(part1_result)

    print()
    print("Part 2")
    part2_result = 0
    for line in lines:
        result = evaluate_expression(line, "+")
        print_debug(f"{line} = {result}")
        part2_result += result
    print(part2_result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
