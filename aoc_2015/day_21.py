#!/usr/bin/env python3

import itertools
import math
import sys
import traceback

from common.utils import *

WEAPONS = {
    "Dagger": (8, 4, 0),
    "Shortsword": (10, 5, 0),
    "Warhammer": (25, 6, 0),
    "Longsword": (40, 7, 0),
    "Greataxe": (74, 8, 0),
}

ARMOR = {
    "Leather": (13, 0, 1),
    "Chainmail": (31, 0, 2),
    "Splintmail": (53, 0, 3),
    "Bandedmail": (75, 0, 4),
    "Platemail": (102, 0, 5),
}

RINGS = {
    "Damage +1": (25, 1, 0),
    "Damage +2": (50, 2, 0),
    "Damage +3": (100, 3, 0),
    "Defense +1": (20, 0, 1),
    "Defense +2": (40, 0, 2),
    "Defense +3": (80, 0, 3),
}

PLAYER_BASE = {
    "hit points": 100,
    "damage": 0,
    "armor": 0,
}


def rounds_to_kill(attacker, defender):
    """ Calculate the number for attacker to kill defender """
    _damage = max(attacker["damage"] - defender["armor"], 1)
    return math.ceil(defender["hit points"] / _damage)


def player_wins(player, boss):
    """ Calculate if player wins against boss """
    return rounds_to_kill(player, boss) <= rounds_to_kill(boss, player)


def permutations(items, n_min, n_max):
    """ Return permutations of n_min to n_max of items """
    for n in range(n_min, n_max + 1):
        yield from itertools.permutations(items, n)


def purchase_combinations():
    """ Generate all possible purchase combinations. Return (cost, damage, armor) """
    for weapons in permutations(WEAPONS.values(), 1, 1):
        for armors in permutations(ARMOR.values(), 0, 1):
            for rings in permutations(RINGS.values(), 0, 2):
                cost = 0
                damage = 0
                armor = 0
                for _cost, _damage, _armor in (weapons + armors + rings):
                    cost += _cost
                    damage += _damage
                    armor += _armor
                yield cost, damage, armor


def solve(boss):
    min_cost = None
    max_cost = None
    for cost, damage, armor in purchase_combinations():
        player = PLAYER_BASE.copy()
        player["damage"] += damage
        player["armor"] += armor
        if player_wins(player, boss):
            if min_cost is None or cost < min_cost:
                min_cost = cost
        else:
            if max_cost is None or cost > max_cost:
                max_cost = cost
    return min_cost, max_cost


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))
    boss = {k.lower(): int(v) for k, v in [line.split(": ") for line in lines]}

    result_1, result_2 = solve(boss)

    log.always("Part 1")
    log.always(result_1)

    log.always("Part 2")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
