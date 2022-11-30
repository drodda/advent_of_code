#!/usr/bin/env python3
import itertools
import sys
import traceback
import queue

from common.utils import *

import intcode_vm
from intcode_vm import *

# Disable verbose logging from intcode_vm
intcode_vm.log.verbose = log.never
intcode_vm.log.debug = log.never


PHASES_LEN = 5


def run_simulation(data, phases, feedback=False):
    vms = []
    if feedback:
        queues = [queue.Queue() for i in range(len(phases))]
        final_queue = queues[0]
        queues.append(final_queue)
    else:
        queues = [queue.Queue() for i in range(len(phases) + 1)]
        final_queue = queues[-1]
    # Load phases
    for i, phase in enumerate(phases):
        queues[i].put(phase)
    # Load initial power
    queues[0].put(0)
    for i, phase in enumerate(phases):
        vm = VMThread(data, input_queue=queues[i], output_queue=queues[i+1])
        vms.append(vm)
    for vm in vms:
        vm.start()
    for vm in vms:
        vm.join()
    if final_queue.empty():
        log.error(f"Warning: No output from from {phases}")
        return None
    return final_queue.get()


def solve(data_file, phases, feedback=False):
    result = None
    for i, data in enumerate(read_csv_int_multiline(data_file, to_list=True)):
        log.always(f"{i}: {list_pretty(data)}")

        phase_permutations = itertools.permutations(phases)
        result_max = None
        result_phases = None
        for phases in phase_permutations:
            log.debug(phases)
            result_sim = run_simulation(data, phases, feedback)
            if result_max is None or result_sim > result_max:
                result_max = result_sim
                result_phases = phases
        log.always(f"{result_max} from phases {result_phases}")
        if result is None or result_max > result:
            result = result_max
    return result


def main():
    args = parse_args()
    log.always("Part 1:")
    phases = list(range(PHASES_LEN))
    result = solve(data_file_path_main(test=args.test), phases, False)
    log.always(result)
    log.always("Part 2:")
    data_file = data_file_path_main(test=args.test)
    if args.test:
        data_file = data_file_path("test", "b")
    phases = list(range(5, 5+PHASES_LEN))
    result = solve(data_file, phases, True)
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
