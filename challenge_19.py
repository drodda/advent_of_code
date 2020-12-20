#!/usr/bin/env python3
import traceback
import operator
import collections

from utils import *


class InvalidRule(Exception):
    pass


class RuleCheckFailed(Exception):
    pass


class Rule:
    def __init__(self, rule_text):
        self.condition = self.parse_rule(rule_text)

    def parse_rule(self, rule_text):
        raise NotImplemented

    def validate_partial(self, rules, text):
        """ Check text against rule
            Returns the remainder of text after validating rule if valid, or raises RuleCheckFailed if invalid
        """
        raise NotImplemented

    def validate(self, rules, text):
        try:
            return self.validate_partial(rules, text) == ""
        except RuleCheckFailed:
            return False

    def __repr__(self):
        return f"<{self.condition}>"


class LiteralRule(Rule):
    def parse_rule(self, rule_text):
        result = rule_text.strip("\"")
        return result

    def validate_partial(self, rules, text):
        if not text.startswith(self.condition):
            raise RuleCheckFailed(text)
        return text[len(self.condition):]


class CombinationRule(Rule):
    def parse_rule(self, rule_text):
        result = []
        for combo in rule_text.split(" | "):
            result.append(list(map(int, combo.split())))
        return result

    def validate_partial(self, rules, text):
        for condition in self.condition:
            try:
                _text = text
                for rule_num in condition:
                    # if rule_num not in self._rules:
                    #     raise InvalidRule
                    rule = rules[rule_num]
                    _text = rule.validate_partial(rules, _text)
                return _text
            except RuleCheckFailed:
                pass
        raise RuleCheckFailed


def parse_rules(lines):
    rules = {}

    for line in lines:
        n_str, rule_text = line.split(": ")
        n = int(n_str)
        if rule_text.startswith("\"") and rule_text.endswith("\""):
            rule = LiteralRule(rule_text)
        else:
            rule = CombinationRule(rule_text)
        rules[n] = rule
    return rules


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines_rules, lines_test = read_multilines(data_file)

    # Build rules
    rules = parse_rules(lines_rules)
    rule = rules[0]
    print("Part 1")
    valid_count = 0
    for line in lines_test:
        valid = rule.validate(rules, line)
        print_debug(f"{line}: {valid}")
        valid_count += int(valid)
    print(valid_count)

    print("Part 2")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
