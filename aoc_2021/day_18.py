#!/usr/bin/env python3

import math
import sys
import traceback

from common.utils import *


def tokenise(text):
    """ Parse string into tokens. Numbers are converted to int, braces remain, commas removed """
    def tokenise_gen():
        val_str = ""
        for c in text:
            if c.isnumeric():
                val_str += c
            else:
                if val_str:
                    yield int(val_str)
                    val_str = ""
                if c in ["[", "]"]:
                    yield c
    return list(tokenise_gen())


def reduce_explode(tokens):
    """ Search tokens for first item that needs to be exploded, and explode.
        Returns True if an item was exploded
    """
    depth = 0
    explode_index = None
    last_num_index = None
    # Search for pair to be exploded
    for i, item in enumerate(tokens):
        if item == "[":
            depth += 1
            if depth > 4:
                explode_index = i
                break
        elif item == "]":
            depth -= 1
        else:
            last_num_index = i

    # Explode pair at explode_index
    if explode_index is not None:
        a = tokens[explode_index + 1]
        b = tokens[explode_index + 2]
        # Remove / replace exploded pair
        del tokens[explode_index:explode_index + 3]
        tokens[explode_index] = 0
        # Add a and b to left- and right- numbers
        if last_num_index is not None:
            tokens[last_num_index] += a
        for i in range(explode_index + 1, len(tokens)):
            if isinstance(tokens[i], int):
                tokens[i] += b
                break
        return True
    return False


def reduce_split(tokens):
    """ Search tokens for first item that needs to be split, and split.
        Returns True if an item was split
    """
    split_index = None
    split_value = None
    # Search for item to be split
    for i, item in enumerate(tokens):
        if isinstance(item, int) and item >= 10:
            split_index = i
            split_value = item
            break
    # Split number at split_index
    if split_index is not None:
        # Insert symbols in reverse order
        tokens[split_index] = "]"
        tokens.insert(split_index, math.ceil(split_value / 2))
        tokens.insert(split_index, math.floor(split_value / 2))
        tokens.insert(split_index, "[")
        return True
    return False


def reduce(tokens):
    """ Reduce tokens with explode and split until no more reductions are required """
    while True:
        if reduce_explode(tokens):
            continue
        if reduce_split(tokens):
            continue
        break


def calculate_value(tokens):
    """ Evaluate Snailfish expression from tokens """
    def calculate_value_iter(_iter):
        a = next(_iter)
        if a == "[":
            a = calculate_value_iter(_iter)
        b = next(_iter)
        if b == "[":
            b = calculate_value_iter(_iter)
        # Consume close bracket
        next(_iter)
        return 3 * a + 2 * b
    # Call recursive calculation. Skip first token (open bracket)
    return calculate_value_iter(iter(tokens[1:]))


def add_tokens(tokens_list):
    """ Add 2 or more Snailfish expressions """
    tokens = tokens_list[0]
    reduce(tokens)
    for tokens_b in tokens_list[1:]:
        tokens_a = tokens
        reduce(tokens_b)
        tokens = ["["] + tokens_a + tokens_b + ["]"]
        reduce(tokens)
    return calculate_value(tokens)


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)
    tokens_list = [tokenise(line) for line in lines]

    log.always("Part 1:")
    log.always(add_tokens(tokens_list))

    log.always("Part 2:")
    result_best = None
    for i, line_i in enumerate(tokens_list):
        for j, line_j in enumerate(tokens_list):
            if i != j:
                result = add_tokens([line_i, line_j])
                if result_best is None or result > result_best:
                    result_best = result
                result = add_tokens([line_j, line_i])
                if result_best is None or result > result_best:
                    result_best = result
    log.always(result_best)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
