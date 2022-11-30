#!/usr/bin/env python3

import sys
import traceback
import itertools

from common.utils import *


SPELLS = {
    # Cost, Duration. Instant spells have duration 1
    "Magic Missile": (53, 1),
    "Drain": (73, 1),
    "Shield": (113, 6),
    "Poison": (173, 6),
    "Recharge": (229, 5),
}


class State(object):
    # Generator to give each object a unique counter
    _count_gen = itertools.count()

    def __init__(self, player_hp, player_mana, boss_hp, boss_damage, mana_spent=0, spells=None, hard=False):
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.mana_spent = mana_spent
        self.spells = spells or {}
        self._hard = hard
        self._counter = next(self._count_gen)

    def __str__(self):
        return " ".join((f"{k}:{v}" for k, v in vars(self).items() if not k.startswith("_")))

    def __eq__(self, other):
        """ Comparator: Check all attribues are the same """
        if not isinstance(other, State):
            return NotImplemented
        return all((v == getattr(other, k) for k, v in vars(self).items() if not k.startswith("_")))

    def __lt__(self, other):
        """ Comparator: compare using mana_cost """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.mana_spent < other.mana_spent or (self.mana_spent == other.mana_spent and self._counter < other._counter)

    def __hash__(self):
        """ Make object hashable """
        return full_hash({k: v for k, v in vars(self).items() if not k.startswith("_")})

    def copy(self, new_spell=None):
        """ Return another copy of self
            Apply new_spell if given, raise StopIteration if new_spell cannot be applied.
        """
        player_mana = self.player_mana
        mana_spent = self.mana_spent
        spells = self.spells.copy()
        if new_spell is not None:
            if new_spell in spells:
                raise StopIteration(f"Spell {new_spell} currently active")
            cost, duration = SPELLS[new_spell]
            player_mana -= cost
            mana_spent += cost
            spells[new_spell] = duration
            if player_mana < 0:
                raise StopIteration(f"Not enough mana to cast {new_spell}")
        return self.__class__(self.player_hp, player_mana, self.boss_hp, self.boss_damage, mana_spent, spells, self._hard)

    def _process_spells(self):
        """ Apply affects of active spells. Decrements spell timer """
        for spell, timer in self.spells.items():
            if spell == "Magic Missile":
                self.boss_hp -= 4
            elif spell == "Drain":
                self.boss_hp -= 2
                self.player_hp += 2
            elif spell == "Shield":
                # Not actioned, checked at boss_turn time
                pass
            elif spell == "Poison":
                self.boss_hp -= 3
            elif spell == "Recharge":
                self.player_mana += 101
            else:
                raise ValueError(f"Unknown spell: {spell}")
        # Decrement timer for all spells, only keep active spells
        self.spells = {spell: timer - 1 for spell, timer in self.spells.items() if timer > 1}

    def transitions(self):
        """ Yield all possible new states from current state. Apply 1 player turn and 1 boss turn """
        _state = self.copy()
        if _state._hard:
            _state.player_hp -= 1
            if _state.player_hp <= 0:
                return
        # Perform player turn
        _state._process_spells()
        for spell in SPELLS:
            try:
                new_state = _state.copy(new_spell=spell)
            except StopIteration:
                continue
            armor = 7 if "Shield" in new_state.spells else 0
            # Apply all spells
            new_state._process_spells()
            # Boss can only attack if alive
            if new_state.boss_hp > 0:
                new_state.player_hp -= max(1, new_state.boss_damage - armor)
            # Only follow states where player is alive
            if new_state.player_hp > 0:
                yield new_state


def solve(data, hard=False):
    start = State(player_hp=50, player_mana=500, boss_hp=data["hit points"], boss_damage=data["damage"], hard=hard)
    explored = set()
    q = SetHeapQ([start])
    while q:
        state = q.pop()
        if state.boss_hp <= 0:
            return state.mana_spent
        explored.add(state)
        for _state in state.transitions():
            if _state in explored or _state in q:
                continue
            q.push(_state)


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    data = {k.lower(): int(v) for k, v in [line.split(": ") for line in lines]}

    log.always("Part 1")
    result = solve(data)
    log.always(result)

    log.always("Part 2")
    result = solve(data, hard=True)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
