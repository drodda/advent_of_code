import operator
import copy
import threading
import queue
from collections import defaultdict

from utils import *


__all__ = [
    "VM", "VMThread",
    "list_pretty",
]


def list_pretty(data, max_len=6):
    """ String-ify a list. If list has more than max_lem elements, truncate """
    if len(data) < max_len:
        return " ".join(map(str, data))
    return "{} ... {}".format(" ".join(map(str, data[:3])), " ".join(map(str, data[-3:])))


class VM:
    class MODE:
        POSITION = 0
        IMMEDIATE = 1
        RELATIVE = 2

    def __init__(self, mem, input_queue=None, input_timeout=5, output_queue=None, tid=None):
        # Memory can be infinite and defaults to 0
        self.mem = defaultdict(int)
        self.mem.update(enumerate(mem))
        self.ip = 0
        self.relative_base = 0
        self.output = output_queue if output_queue is not None else queue.Queue()
        if isinstance(input_queue, queue.Queue):
            self.input = input_queue
        else:
            self.input = queue.Queue()
            if input_queue is not None:
                for v in input_queue:
                    self.input.put(v)
        self._input_timeout = input_timeout
        self._tid = tid

    def decode_instruction(self):
        """ Decode instruction at self.ip and return opcode and modes """
        # Convert to str and pad
        instruction_str = str(self.mem_load(self.ip)).zfill(5)
        # Extract digits
        mode_3 = int(instruction_str[0])
        mode_2 = int(instruction_str[1])
        mode_1 = int(instruction_str[2])
        opcode = int(instruction_str[3:])
        return opcode, mode_1, mode_2, mode_3

    def operand(self, n):
        """ Get the nth operand """
        return self.mem_load(self.ip + n)

    def mem_load(self, addr):
        if addr < 0:
            raise RuntimeError(f"Access negative memory: {self.ip}")
        return self.mem[addr]

    def mem_put(self, addr, val):
        if addr < 0:
            raise RuntimeError(f"Access negative memory: {self.ip}")
        self.mem[addr] = val

    def load(self, mode, operand):
        """ Load value based on mode: 0 = address, 1 = literal, 2 = relative address """
        if mode == self.MODE.IMMEDIATE:
            return operand
        elif mode == self.MODE.POSITION:
            return self.mem_load(operand)
        elif mode == self.MODE.RELATIVE:
            return self.mem_load(self.relative_base + operand)
        else:
            raise RuntimeError(f"Bad mode {mode}")

    def put(self, mode, operand, val):
        """ Store value based on mode: 0 = address, 2 = relative address """
        if mode == self.MODE.IMMEDIATE:
            raise RuntimeError("Can not put in immediate mode")
        elif mode == self.MODE.POSITION:
            self.mem_put(operand, val)
        elif mode == self.MODE.RELATIVE:
            self.mem_put(self.relative_base + operand, val)
        else:
            raise RuntimeError(f"Bad mode {mode}")

    OPERATIONS_LLS = {
        # Load-Load-Store operations that take 3 params: p3 = operator(p1, p2)
        1: operator.add,
        2: operator.mul,
        7: lambda v1, v2: int(operator.lt(v1, v2)),
        8: lambda v1, v2: int(operator.eq(v1, v2)),
    }
    OPERATORS_EVAL_JUMP = {
        # Condition for EVAL_JUMP operations
        5: bool,
        6: lambda c: not bool(c),
    }

    def step(self):
        opcode, mode_1, mode_2, mode_3 = self.decode_instruction()
        next_ip = self.ip + 1
        if opcode == 99:
            raise StopIteration
        elif opcode in self.OPERATIONS_LLS:
            # Load-Load-Store operations that take 3 params: p3 = operator(p1, p2)
            next_ip += 3
            operation = self.OPERATIONS_LLS[opcode]
            p1 = self.load(mode_1, self.operand(1))
            p2 = self.load(mode_2, self.operand(2))
            p3 = self.operand(3)
            result = operation(p1, p2)
            self.put(mode_3, p3, result)
        elif opcode == 3:
            # Input -> p1
            next_ip += 1
            if self.input.empty():
                log_debug(f"VM {self.tid}: Waiting for input - timeout {self._input_timeout}")
            input_value = self.input.get(timeout=self._input_timeout, block=True)
            self.put(mode_1, self.operand(1), input_value)
        elif opcode == 4:
            # p1 -> Output
            next_ip += 1
            p1 = self.operand(1)
            v = self.load(mode_1, p1)
            self.output.put(v)
            log_debug(f"VM {self.tid}: OUTPUT: ip {self.ip} addr {p1} val {v}")
        elif opcode in self.OPERATORS_EVAL_JUMP:
            # Load+Eval?Jump operations: Evaluate condition on p1 and (conditionally) jump to p2
            next_ip += 2
            condition = self.OPERATORS_EVAL_JUMP[opcode]
            p1 = self.load(mode_1, self.operand(1))
            p2 = self.load(mode_2, self.operand(2))
            if condition(p1):
                next_ip = p2
        elif opcode == 9:
            # Adjust relative base by p1
            next_ip += 1
            self.relative_base += self.load(mode_1, self.operand(1))
        else:
            raise RuntimeError(f"Invalid instruction: {self.mem[self.ip]} at {self.ip}")
        self.ip = next_ip

    def run(self):
        try:
            log_verbose(f"VM {self.tid}: {self.ip} - {self.mem}")
            while True:
                self.step()
                log_verbose(f"VM {self.tid}: {self.ip} - {self.mem}")
        except StopIteration:
            pass
        return

    @property
    def tid(self):
        return self._tid


class VMThread(VM, threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        threading.Thread.__init__(self)

    @property
    def tid(self):
        return self._tid if self._tid is not None else self.ident
