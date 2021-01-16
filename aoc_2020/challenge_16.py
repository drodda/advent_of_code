#!/usr/bin/env python3
import traceback

from utils import *


class Condition:
    """ Checks is a number is in a range. Range is presented as a string: '1-3' """
    def __init__(self, cond_str):
        min_str, max_str = cond_str.split("-")
        self.min = int(min_str)
        self.max = int(max_str)

    def valid(self, val):
        return self.min <= val <= self.max

    def __str__(self):
        return f"{self.min}-{self.max}"

    def __repr__(self):
        return str(self)


class Rule:
    """ Checks if a number is in a range. Constructed with a string with name and conditions: 'class: 1-3 or 5-7' """
    def __init__(self, rule_str, index):
        name, conditions_str = rule_str.split(": ")
        self.name = name
        self.index = index
        self.conditions = [Condition(condition_str) for condition_str in conditions_str.split(" or ")]

    def valid(self, val):
        return any([condition.valid(val) for condition in self.conditions])

    def __str__(self):
        condition_str = " or ".join([str(c) for c in self.conditions])
        return f"{self.index}|{self.name}: {condition_str}"

    def __repr__(self):
        return str(self)


def valid_rules(rules, val):
    """ Return a list of rules that are valid for val """
    return [rule for rule in rules if rule.valid(val)]


def valid_rules_from_list(rules, values):
    """ Return a list of rules that are valid for all values """
    for val in values:
        if not rules:
            break
        rules = valid_rules(rules, val)
    return rules


class InvalidRuleOrder(Exception):
    """ Raised when a rule combination is not valid """
    pass


def find_rules_order(valid_rules_per_col, used_rules=None):
    """ For a list of (list of rules valid per column), find a valid order of unique rules valid for each column """

    if used_rules is None:
        used_rules = []

    i = len(used_rules)
    if i >= len(valid_rules_per_col):
        # All columns have been assigned a rule - success!
        return []

    for rule in valid_rules_per_col[i]:
        try:
            if rule not in used_rules:
                # Rule has not yet been used - check if the rest of the chain is valid with this rule in place i
                return [rule] + find_rules_order(valid_rules_per_col, used_rules + [rule])
        except InvalidRuleOrder:
            # The rest of the chain was not valid - keep searching
            pass
    # A not valid combination has been reached
    raise InvalidRuleOrder


def parse_ticket(line):
    """ Split a string of comma-separated numbers and cast to int """
    return list(map(int, line.split(",")))


def main():
    args = parse_args()
    data_file = data_file_path_main(test=False) if not args.test else data_file_path("test", args.var)
    rule_lines, own_ticket_lines, other_ticket_lines = read_multilines(data_file)
    rules = [Rule(line, i) for i, line in enumerate(rule_lines)]

    own_ticket = parse_ticket(own_ticket_lines[1])
    other_tickets = list(map(parse_ticket, other_ticket_lines[1:]))
    cols = len(own_ticket)

    print("Part 1")
    invalid_sum = 0
    valid_tickets = []
    for ticket in other_tickets:
        valid = True
        for val in ticket:
            if not valid_rules(rules, val):
                print_verbose(f"Invalid: {val}")
                invalid_sum += val
                valid = False
        if valid:
            valid_tickets.append(ticket)
    print(invalid_sum)

    print("Part 2")
    # Iterate through value column finding all rules that are valid for each column
    valid_rules_per_col = [[]] * cols
    print_debug("Valid rules per column:")
    for i in range(cols):
        col_values = [ticket[i] for ticket in valid_tickets]
        col_valid_rules = valid_rules_from_list(rules, col_values)
        print_debug("")
        print_debug(f"{i}: {col_valid_rules}")
        valid_rules_per_col[i] = col_valid_rules
    # Find the order of rules from the valid combinations
    col_rules = find_rules_order(valid_rules_per_col)
    print_debug("")
    print_debug("Ordered rules:")
    print_debug(col_rules)

    part2_result = 1
    print_debug("")
    print_debug("Own ticket:")
    for i, rule in enumerate(col_rules):
        if rule.name.startswith("departure "):
            print_debug(f"{i}: {rule}, {own_ticket[i]}")
            part2_result *= own_ticket[i]
    print_debug("")
    print(part2_result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
