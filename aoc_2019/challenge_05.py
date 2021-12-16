#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import VM


###############################################################################


def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=args.test), to_list=True)

    log_always("Part 1")
    vm = VM(data, input_queue=[1])
    vm.run()
    log_always(list(vm.output.queue))

    log_always("Part 2")
    vm = VM(data, input_queue=[5])
    vm.run()
    log_always(list(vm.output.queue))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
