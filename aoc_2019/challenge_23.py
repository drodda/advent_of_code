#!/usr/bin/env python3
import sys
import traceback
import queue
import threading

from common.utils import *
from intcode_vm import *


###############################################################################


N_VMS = 50


IDLE_SENTINEL = "is idle"


class NicVM(VMThread):
    def __init__(self, mem, vm_id, router):
        super().__init__(mem)
        self.vm_id = vm_id
        self.router = router
        # Replace output queue
        self.output = []
        self.is_idle = False

    def step(self):
        if self.router.stopped:
            raise StopIteration
        super().step()

    def send_packet(self, x, y):
        self.input.put(x)
        self.input.put(y)
        self.is_idle = False

    def _input(self):
        # Read input, or -1
        try:
            return self.input.get(block=False)
        except Empty:
            if not self.is_idle:
                self.router.route_for_vm(self.vm_id, IDLE_SENTINEL)
                log_debug(f"VM {self.vm_id} is going idle")
            self.is_idle = True
            return -1

    def _output(self, item):
        self.output.append(item)
        if len(self.output) == 3:
            # Received a complete output
            self.router.route_for_vm(self.vm_id, self.output)
            self.output = []


class VMRouter:
    def __init__(self, mem, n):
        self.stopped = False
        self.queue = queue.Queue()
        self.last_x = None
        self.last_y = None
        self.last_y_sent = None
        self.vms = {}
        for i in range(n):
            vm = NicVM(mem, i, self)
            vm.input.put(i)
            self.vms[i] = vm

    def route_for_vm(self, vm_id, data):
        self.queue.put((vm_id, data))

    def run(self):
        for vm in self.vms.values():
            vm.start()
        log_debug("Waiting for result ...")
        while True:
            vm_id, data = self.queue.get()
            if data is IDLE_SENTINEL:
                if self.queue.empty():
                    # C heck if all VMs are idle
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
                            vm.send_packet(self.last_x, self.last_y)
                        else:
                            log_error("Error: NAT has no stored data")
            else:
                log_debug(f"Routing {vm_id} => {data}")
                addr, x, y = data
                vm = self.vms.get(addr)
                if vm is not None:
                    vm.send_packet(x, y)
                elif addr == 255:
                    # Packet to NAT
                    log_info(f"NAT: received {x}, {y}")
                    if self.last_y is None:
                        log_always("Part 1")
                        log_always(y)
                    self.last_x = x
                    self.last_y = y
                else:
                    log_error(f"route: bad address {addr}")

        # Stop all VMs
        self.stopped = True
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
