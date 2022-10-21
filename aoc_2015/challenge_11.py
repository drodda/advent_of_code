#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def validate(plst):
    # Passwords may not contain the letters i, o, or l
    if ord("i") in plst or ord("o") in plst or ord("l") in plst:
        return False

    # Passwords must include one increasing straight of at least three letters
    _result = False
    for i in range(len(plst) - 2):
        if plst[i] + 1 == plst[i + 1] and plst[i + 1] + 1 == plst[i + 2]:
            _result = True
    if not _result:
        return False

    # Passwords must contain at least two different, non-overlapping pairs of letters
    _result = False
    _index = None
    for i in range(len(plst) - 1):
        if plst[i] == plst[i + 1]:
            if _index is None:
                _index = i
            elif _index < i - 1:
                _result = True
    if not _result:
        return False

    return True


def password_gen(plst=None):
    if plst is None:
        plst = [ord("a")] * 8
        yield plst.copy()
    else:
        plst = plst.copy()
    while True:
        for i in range(7, -1, -1):
            plst[i] += 1
            if plst[i] <= ord("z"):
                break
            plst[i] = ord("a")
        yield plst.copy()


def plst_to_str(plst):
    return "".join(map(chr, plst))


def main():
    args = parse_args()
    password = open(data_file_path_main(test=args.test)).read().strip()
    plst = list(map(ord, password))

    log_always("Part 1")
    for _plst in password_gen(plst):
        log_debug(f"Evaluating: {plst_to_str(_plst)}")
        if validate(_plst):
            break
    log_always(plst_to_str(_plst))

    log_always("Part 2")
    for _plst in password_gen(_plst):
        log_debug(f"Evaluating: {plst_to_str(_plst)}")
        if validate(_plst):
            break
    log_always(plst_to_str(_plst))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
