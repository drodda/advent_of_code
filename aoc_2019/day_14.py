#!/usr/bin/env python3

import math
import sys
import traceback
from collections import defaultdict

from common.utils import *


def parse_item(text):
    n, t = text.split(" ")
    return int(n), t


def parse_line(line):
    inputs_str, output_str = line.split(" => ")
    qtty_made, resource_made = parse_item(output_str)
    inputs = {}
    for item in inputs_str.split(", "):
        qtty_required, resource_required = parse_item(item)
        inputs[resource_required] = qtty_required
    return resource_made, qtty_made, inputs


def calculate_cost(resource_map, resource, qtty_required=1, extra_resources=None):
    if resource == "ORE":
        return qtty_required
    if extra_resources is None:
        extra_resources = defaultdict(int)
    qtty_available = extra_resources[resource]
    qtty_used = min(qtty_required, qtty_available)
    extra_resources[resource] -= qtty_used
    qtty_required -= qtty_used
    if qtty_required == 0:
        return 0

    qtty_per_batch, requirements = resource_map[resource]
    batches = math.ceil(qtty_required / qtty_per_batch)
    # Calculate and store excess
    extra_resources[resource] += (batches * qtty_per_batch) - qtty_required

    result = 0
    for resource_required, _qtty_required in requirements.items():
        result += calculate_cost(resource_map, resource_required, batches * _qtty_required, extra_resources)
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))
    resource_map = {}
    for line in lines:
        _resource, _qtty_made, _inputs = parse_line(line)
        resource_map[_resource] = (_qtty_made, _inputs)

    log.always("Part 1")
    cost = calculate_cost(resource_map, "FUEL")
    log.always(cost)

    log.always("Part 2")
    ore_limit = 1000000000000
    qtty_best = 1
    while True:
        # Calculae the cost to build based on current cost and qtty, or at least 1 more than the previous
        qtty = max(math.floor(ore_limit / cost * qtty_best), qtty_best + 1)
        cost = calculate_cost(resource_map, "FUEL", qtty, None)
        log.info(f"Cost to build {qtty} fuel: {cost}")
        if cost > ore_limit:
            break
        qtty_best = qtty
    log.always(qtty_best)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
