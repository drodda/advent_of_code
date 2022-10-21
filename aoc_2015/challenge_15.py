#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *

RE = re.compile(r"(\S+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)")


def parse_input(lines):
    result = []
    for line in lines:
        m = RE.match(line)
        if m:
            name, *vals = m.groups()
            result.append((name, tuple(map(int, vals))))
        else:
            log_error(f"Bad line: {line}")
    return result


def combinations(n_vals, max_v):
    """ Return tuple of all combinations of n_vals integers that add to max_v """
    if n_vals > 2:
        for i in range(max_v + 1):
            for _v in combinations(n_vals - 1, max_v - i):
                yield (i, ) + _v
    elif n_vals == 2:
        for i in range(max_v + 1):
            yield i, max_v - i
    else:
        raise ValueError("n_vals must be >= 2")


def calculate_score(ingredients, mix, mask):
    """ Calculate score of mix of ingredients masked by mask """
    result = 1
    for i, v in enumerate(mask):
        if v:
            result *= max(sum([ingredients[j][i] * qtty for j, qtty in enumerate(mix)]), 0)
    return result


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    ingredients = parse_input(lines)
    ingredient_vals = [vals for name, vals in ingredients]
    log_info(ingredients)

    n_vals = len(ingredients)

    result_1 = 0
    result_2 = 0
    for combination in combinations(n_vals, 100):
        score = calculate_score(ingredient_vals, combination, (True, True, True, True))
        calories = calculate_score(ingredient_vals, combination, (False, False, False, False, True))
        log_debug(f"{combination}: {score}")
        result_1 = max(result_1, score)
        if calories == 500:
            result_2 = max(result_2, score)

    log_always("Part 1")
    log_always(result_1)

    log_always("Part 2")
    log_always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
