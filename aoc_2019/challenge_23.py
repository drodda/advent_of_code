#!/usr/bin/env python3
import sys
import traceback
import queue
import threading

from common.utils import *
from intcode_vm import *


###############################################################################


N_VMS = 50


class NicVM(VMThread):
    def __init__(self, mem, vm_id, router):
        super().__init__(mem)
        self.stopped = False
        self.vm_id = vm_id
        self.router = router
        # Synchronisation to ensure writes to a VM's input queue are atomic
        self.input_lock = threading.Lock()
        # replace output queue
        self.output = []
        self.is_idle = False

    def stop(self):
        self.stopped = True

    def step(self):
        if self.stopped:
            raise StopIteration
        super().step()

    def _input(self):
        # Read input, or -1
        try:
            return self.input.get(block=False)
        except Empty:
            self.is_idle = True
            return -1

    def _output(self, item):
        self.output.append(item)
        if len(self.output) == 3:
            # Received a complete output
            addr, x, y = self.output
            self.output = []
            self.router.route(addr, x, y)


class VMRouter:
    def __init__(self, mem, n):
        self.result = queue.Queue()
        self.last_x = None
        self.last_y = None
        self.last_y_sent = None
        self.vms = {}
        for i in range(n):
            vm = NicVM(mem, i, self)
            vm.input.put(i)
            self.vms[i] = vm

    def route(self, addr, x, y):
        log_debug(f"Routing: {addr} => {x} {y}")
        vm = self.vms.get(addr)
        if vm is not None:
            with vm.input_lock:
                vm.input.put(x)
                vm.input.put(y)
                vm.is_idle = False
        else:
            if addr == 255:
                self.result.put((x, y))
            else:
                log_error(f"route: bad address {addr}")

    def run(self):
        for vm in self.vms.values():
            vm.start()
        log_debug("Waiting for result ...")
        while True:
            try:
                x, y = self.result.get(timeout=1)
                log_info(f"NAT: received {x}, {y}")
                if self.last_y is None:
                    log_always("Part 1")
                    log_always(y)
                self.last_x = x
                self.last_y = y
            except Empty:
                # Check if all VMs are idle
                if all([vm.is_idle for vm in self.vms.values()]):
                    log_info("VMs are idle")
                    if self.last_x is not None:
                        if self.last_y_sent == self.last_y:
                            log_always("Part 2")
                            log_always(self.last_y)
                            break
                        self.last_y_sent = self.last_y
                        vm = self.vms[0]
                        log_info(f"NAT: sending {self.last_x}, {self.last_y}")
                        vm.input.put(self.last_x)
                        vm.input.put(self.last_y)
                        vm.is_idle = False
                    else:
                        log_error("Error: NAT has no stored data")

                # if all()
                pass
        # Stop all VMs
        for vm in self.vms.values():
            vm.stop()
        for vm in self.vms.values():
            vm.join()


def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)

    router = VMRouter(data, N_VMS)
    router.run()


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
