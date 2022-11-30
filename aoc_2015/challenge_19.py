#!/usr/bin/env python3

import collections
import re
import sys
import traceback

from common.utils import *


def parse_replacements(lines):
    result = collections.defaultdict(list)
    for line in lines:
        atom, replacement = line.split(" => ")
        result[atom].append(replacement)
    return dict(result)


def reverse_replacements(replacements):
    result_dict = collections.defaultdict(list)
    for atom, _replacements in replacements.items():
        for replacement in _replacements:
            result_dict[replacement].append(atom)
    # Convert to list of (replacement, (atom, atom, ...))
    result = sorted(result_dict.items(), key=lambda k: len(k[0]), reverse=True)
    return result


def find_all(s, substr):
    """ Find all occurances of substr in s. Return indexes in order """
    for match in re.finditer(substr, s):
        yield match.start()


def mutate(molecule, replacements):
    """ Apply a single mutation of molecule. Return all possible mutations """
    result = set()
    for atom, replacements in replacements.items():
        for i in find_all(molecule, atom):
            for replacement in replacements:
                _molecule = molecule[:i] + replacement + molecule[i + len(atom):]
                result.add(_molecule)
    return result


def reverse_mutate(molecule, reversed_replacements, explored=None):
    """ Reverse mutate molecule until start atom e'. Return number of mutations required """
    if explored is None:
        explored = set()
    explored.add(molecule)
    if molecule == "e":
        return 0

    # Greedily apply longest replacement first
    for replacement, atoms in reversed_replacements:
        for i in find_all(molecule, replacement):
            # Try all replacement atoms
            for atom in atoms:
                _molecule = molecule[:i] + atom + molecule[i + len(replacement):]
                if _molecule not in explored:
                    result = reverse_mutate(_molecule, reversed_replacements, explored)
                    if result is not None:
                        return result + 1
    return None


def main():
    args = parse_args()
    replacements_lines, molecule_lines = read_multilines(data_file_path_main(test=args.test))
    replacements = parse_replacements(replacements_lines)
    molecule = molecule_lines[0]

    log.always("Part 1")
    mutations = mutate(molecule, replacements)
    log.verbose(mutations)
    result = len(mutations)
    log.always(result)

    log.always("Part 2")
    reversed_replacements = reverse_replacements(replacements)
    result = reverse_mutate(molecule, reversed_replacements)
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
