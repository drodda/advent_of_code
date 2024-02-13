#!/usr/bin/env python3

import collections
import itertools
import re
import sys
import traceback

from common.utils import *


RE = re.compile(r"(\S+) would (gain|lose) (\d+) happiness units by sitting next to (\S+).")


def parse_input(lines):
    result = collections.defaultdict(lambda: collections.defaultdict(int))
    for line in lines:
        m = RE.match(line)
        if m:
            name1, action, val, name2 = m.groups()
            val = int(val)
            if action == "lose":
                val = -val
            result[name1][name2] = val
        else:
            log.error(f"Bad line: {line}")
    return result


def score_arrangement(arrangement, scores):
    _arrangement = arrangement[1:] + (arrangement[0], )
    result = 0
    for name1, name2 in zip(arrangement, _arrangement):
        result += scores[name1][name2] + scores[name2][name1]
    return result


def find_best_arrangement(all_names, scores):
    result = None
    beat_arrangement = None
    for arrangement in itertools.permutations(all_names):
        score = score_arrangement(arrangement, scores)
        if result is None or score > result:
            result = score
            beat_arrangement = arrangement
        log.debug(f"{arrangement}: {score}")
    return result, beat_arrangement


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)
    scores = parse_input(lines)
    all_names = list(scores.keys())

    log.always("Part 1")
    result, *_ = find_best_arrangement(all_names, scores)
    log.always(result)

    log.always("Part 2")
    result, *_ = find_best_arrangement(all_names + ["self"], scores)
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
