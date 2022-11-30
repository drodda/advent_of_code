#!/usr/bin/env python3

import sys
import traceback
from collections import defaultdict

from common.utils import *


class SolutionError(Exception):
    """ Raised when problem has no solution. Usually indicated bad input data """
    pass


def str_sort(val):
    """ Sort a string, return a sorted string """
    return "".join(sorted(val))


def list_pop_by_condition(lst, condition):
    """ Pop first item from lst that matches condition, return item """
    def _find_item_by_condition():
        for item in lst:
            if condition(item):
                return item
        raise SolutionError(f"Condition {condition} not met by any item in {lst}")
    result = _find_item_by_condition()
    # Remove result from lst
    lst.remove(result)
    return result


def lists_pop_by_condition(lst1, lst2, condition):
    """ Pop first item from each of lst1 and lst2 that matches condition, return items """
    def _find_item_by_condition():
        for _item1 in lst1:
            for _item2 in lst2:
                if condition(_item1, _item2):
                    return _item1, _item2
        raise SolutionError(f"Condition {condition} not met by any item in {lst1}, {lst2}")
    item1, item2 = _find_item_by_condition()
    # Remove result from lst1, lst2
    lst1.remove(item1)
    lst2.remove(item2)
    return item1, item2


def solve(input_values, output_values):
    # Sort signals
    input_values = [str_sort(item) for item in input_values]
    output_values = [str_sort(item) for item in output_values]
    # Group input_values by length
    input_values_by_len = defaultdict(list)
    for item in input_values:
        input_values_by_len[len(item)].append(item)
    if not all([
        len(input_values_by_len[2]) == 1,
        len(input_values_by_len[3]) == 1,
        len(input_values_by_len[4]) == 1,
        len(input_values_by_len[5]) == 3,
        len(input_values_by_len[6]) == 3,
        len(input_values_by_len[7]) == 1,
    ]):
        raise SolutionError("Incorrect lengths of input values")

    numbers = {}  # Store signals for each number identified

    # Identify easy values
    numbers[1] = input_values_by_len[2].pop()
    numbers[7] = input_values_by_len[3].pop()
    numbers[4] = input_values_by_len[4].pop()
    numbers[8] = input_values_by_len[7].pop()
    # 3: superset of 7
    numbers[3] = list_pop_by_condition(input_values_by_len[5], lambda x: set(numbers[7]).issubset(set(x)))
    # 6: NOT superset of 7
    numbers[6] = list_pop_by_condition(input_values_by_len[6], lambda x: not set(numbers[7]).issubset(set(x)))
    # 5 is a subset of 9
    numbers[5], numbers[9] = lists_pop_by_condition(input_values_by_len[5], input_values_by_len[6], lambda item_5, item_6: set(item_5).issubset(set(item_6)))
    # Remaining items are now known
    numbers[2] = input_values_by_len[5].pop()
    numbers[0] = input_values_by_len[6].pop()

    # Create lookup to convert signals to numbers. Signals need to be sorted
    signals = {signal: num for num, signal in numbers.items()}

    # Identify output values from their signals
    result = 0
    for item in output_values:
        result = result * 10 + signals[item]
    return result


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = 0
    for i, line in enumerate(data):
        output_values = line.split(" | ")[1].split(" ")
        _result = 0
        for item in output_values:
            if len(item) in [2, 3, 4, 7]:
                _result += 1
        log.info(f"{i}: {_result}")
        result += _result
    log.always(result)

    log.always("Part 2:")
    result = 0
    for i, line in enumerate(data):
        input_line, output_line = line.split(" | ")
        input_values = [item for item in input_line.split(" ")]
        output_values = [item for item in output_line.split(" ")]
        _result = solve(input_values, output_values)
        log.info(f"{i}: {_result}")
        result += _result
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
