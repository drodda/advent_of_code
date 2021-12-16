#!/usr/bin/env python3

import sys
import traceback
import collections

from common.utils import *


def parse_line(line):
    ingredients_str, allergens_str = line.rstrip(")").split(" (contains ")
    ingredients = ingredients_str.split(" ")
    allergens = allergens_str.split(", ")
    return ingredients, allergens


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file)

    # All, as set (unique) and list (with duplicates)
    ingredients_all = set()
    ingredients_total = []
    allergens_all = set()
    # Identified
    allergens = {}
    # Map data into possible ingredients and allergens
    allergens_to_ingredients = collections.defaultdict(list)
    # Possible ingredients per allergen
    allergens_possible = {}

    for line in lines:
        _ingredients, _allergens = parse_line(line)
        ingredients_all.update(_ingredients)
        allergens_all.update(_allergens)
        ingredients_total.extend(_ingredients)
        for _allergen in _allergens:
            allergens_to_ingredients[_allergen].append(set(_ingredients))

    # Refine data: If an allergen is listed the corresponding ingredient will be present.
    # Refine allergens_to_ingredients to include only ingredients that are in all lists
    for allergen, lists_of_ingredients in allergens_to_ingredients.items():
        allergens_possible[allergen] = set.intersection(*lists_of_ingredients)

    ingredients_with_allergens = set.union(*allergens_possible.values())
    ingredients_without_allergens = ingredients_all.difference(ingredients_with_allergens)

    # Count occurrences of ingredients_without_allergens
    total = 0
    for ingredient in ingredients_without_allergens:
        count = ingredients_total.count(ingredient)
        log_debug(f"{ingredient}: {count}")
        total += count
    log_debug()
    log_always("Part 1")
    log_always(total)
    log_always()

    # Find the only possible combination of ingredients for allergens
    while allergens_possible:
        for allergen, ingredients in allergens_possible.items():
            if len(ingredients) == 1:
                # Found an allergen with only 1 possible ingredient
                # Get the only item
                ingredient = ingredients.pop()
                log_debug(f"{allergen} = {ingredient}")
                allergens[allergen] = ingredient

                # Remove from all other allergens
                for _ingredients in allergens_possible.values():
                    _ingredients.discard(ingredient)
                # Remove allergen from dict
                allergens_possible.pop(allergen)
                break
        else:
            raise RuntimeError(f"Could not find an allergen to remove? {allergens_possible}")
    log_debug()

    ingredients_sorted = collections.OrderedDict(sorted(allergens.items()))
    log_always("Part 2")
    log_always(",".join(ingredients_sorted.values()))
    log_always()


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
