#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb
import re
import json

from utils import *


FIELDS_REQUIRED = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
FIELDS_OPTIONAL = ["cid"]
FIELDS_ALL = FIELDS_REQUIRED + FIELDS_OPTIONAL


class MissingField(Exception):
    def __init__(self, field):
        msg = f"Missing field '{field}'"
        super().__init__(msg)


class InvalidField(Exception):
    def __init__(self, field, val):
        msg = f"Bad field '{field}': '{val}'"
        super().__init__(msg)


def parse_input(filename):
    lines = read_lines(filename, strip_empty=False)
    entries = []
    entry = {}
    for line in lines:
        if not line:
            # Flush entry
            if entry:
                entries.append(entry)
            entry = {}
        fields = line.split()
        for field in fields:
            if field:
                k, v = field.split(":")
                entry[k] = v
    return entries


def validate_int(val_str, field, val_min=None, val_max=None):
    if not val_str.isnumeric():
        raise InvalidField(field, val_str)
    val = int(val_str)
    if val_min:
        if val_min > val:
            raise InvalidField(field, val_str)
    if val_max:
        if val_max < val:
            raise InvalidField(field, val_str)


def validate_int_field(entry, field, val_min=None, val_max=None):
    try:
        val_str = entry[field]
        validate_int(val_str, field, val_min, val_max)
    except KeyError:
        raise MissingField(field)


def validate_entry(entry):
    try:
        validate_int_field(entry, "byr", 1920, 2002)
        validate_int_field(entry, "iyr", 2010, 2020)
        validate_int_field(entry, "eyr", 2020, 2030)

        hgt = entry["hgt"]
        if hgt.endswith("cm"):
            validate_int(hgt[:-2], "hgt", 150, 193)
        elif hgt.endswith("in"):
            validate_int(hgt[:-2], "hgt", 59, 76)
        else:
            raise InvalidField("hgt", hgt)

        hcl = entry["hcl"]
        if not re.match("#[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]", hcl):
            raise InvalidField("hcl", hcl)

        ecl = entry["ecl"]
        if ecl not in "amb blu brn gry grn hzl oth".split():
            raise InvalidField("ecl", ecl)

        pid = entry["pid"]
        if not pid.isnumeric() or len(pid) != 9:
            raise InvalidField("pid", pid)

    except KeyError as e:
        raise MissingField(e.args[0])
    log_debug(f"Valid: {entry}")


def main():
    args = parse_args()
    entries = parse_input(data_file_path_main(test=args.test))

    log_always("Part 1:")
    valid = 0
    for entry in entries:
        try:
            for field in FIELDS_REQUIRED:
                if field not in entry:
                    raise MissingField(field)
        except MissingField as e:
            pass
        else:
            valid += 1
    log_always(valid)

    log_always("Part 2:")
    # entries = parse_input(data_file_path(suffix="valid", var="b"))
    # entries = parse_input(data_file_path(suffix="invalid", var="b"))
    valid = 0
    for entry in entries:
        try:
            validate_entry(entry)
        except MissingField as e:
            log_debug(entry)
            log_debug(e)
        except InvalidField as e:
            log_debug(entry)
            log_debug(e)
        else:
            valid += 1
    log_always(valid)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
