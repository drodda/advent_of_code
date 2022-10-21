#!/usr/bin/env python3

import ast
import sys
import traceback

from common.utils import *


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)

    log_always("Part 1")
    result = 0
    for line in lines:
        _line = ast.literal_eval(line)
        result += len(line) - len(_line)
        # result += line.count("\\") - line.count("\\\\") + 2
    log_always(result)

    log_always("Part 2")
    result = 0
    for line in lines:
        result += line.count("\"") + line.count("\\") + 2
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
