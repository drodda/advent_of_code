#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


RECURSIVE_RULES = [
    "8: 42 | 42 8",
    "11: 42 31 | 42 11 31"
]


def test_message(rules, message, rule_list):
    """ Test if message can be produced using rule_list """
    if not message and not rule_list:
        return True
    if not message or not rule_list:
        return False
    rule = rules[rule_list[0]]
    if isinstance(rule, str):
        # Literal: check
        if message[0] != rule:
            return False
        return test_message(rules, message[1:], rule_list[1:])
    else:
        # List of rules
        for _rule_list in rule:
            if test_message(rules, message, _rule_list + rule_list[1:]):
                return True
        return False


def parse_rules(lines):
    rules = {}
    for line in lines:
        n_str, rule_text = line.split(": ")
        n = int(n_str)
        if rule_text.startswith("\"") and rule_text.endswith("\""):
            rule = rule_text.strip("\"")
        else:
            rule = [list(map(int, combo.split())) for combo in rule_text.split(" | ")]
        rules[n] = rule
    return rules


def test_rules(rules, lines):
    count = 0
    for line in lines:
        if test_message(rules, line, [0]):
            count += 1
    return count



def main():
    args = parse_args()
    data_file = args.input
    # data_file = "data/challenge_19b_test.txt"
    lines_rules, lines_test = read_multilines(data_file)

    log.always("Part 1")
    rules = parse_rules(lines_rules)
    log.always(test_rules(rules, lines_test))

    log.always("Part 2")
    rules = parse_rules(lines_rules + RECURSIVE_RULES)
    log.always(test_rules(rules, lines_test))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
