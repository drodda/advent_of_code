#!/usr/bin/env python3

import sys
import queue
import traceback

from common.utils import *
from common.pygame_visualise import *
from intcode_vm import *


OBJECT_EMPTY = 0
OBJECT_WALL = 1
OBJECT_BLOCK = 2
OBJECT_HORIZONTAL_PADDLE = 3
OBJECT_BALL = 4

INPUT_NONE = 0
INPUT_LEFT = -1
INPUT_RIGHT = 1


class Visualiser(PyGameVisualise):
    color_map = {
        OBJECT_EMPTY: Color.GREY,
        OBJECT_WALL: Color.BLACK,
        OBJECT_BLOCK: Color.ORANGE,
        OBJECT_HORIZONTAL_PADDLE: Color.BROWN,
        OBJECT_BALL: Color.GREEN,
    }

    def __init__(self, x_max, y_max):
        super().__init__(x_max, y_max, 20, Color.GREY)

    def visualise(self, screen_data):
        self.fill(Color.GREY)
        for (x, y), val in screen_data.items():
            self.draw_block(x, y, self.color_map[val], gap=1)
        self.draw(60)


def parse_output(vm):
    """ Read all output from VM, and parse """
    screen_data = {}
    score = None
    ball_x = None
    ball_y = None
    paddle_x = None
    try:
        while not vm.output.empty():
            x = vm.output.get()
            y = vm.output.get()
            val = vm.output.get()
            if val == OBJECT_BALL:
                ball_x = x
                ball_y = y
            elif val == OBJECT_HORIZONTAL_PADDLE:
                paddle_x = x
            if x == -1 and y == 0:
                score = val
            else:
                screen_data[(x, y)] = val
    except queue.Empty:
        log_error("VM output ended unexpectedly")
    return screen_data, score, ball_x, ball_y, paddle_x


def simulate_part_1(data):
    vm = VM(data)
    vm.run()
    screen_data, *_ = parse_output(vm)
    result = sum([val == OBJECT_BLOCK for val in screen_data.values()])
    x_max = max([coord[0] for coord in screen_data.keys()])
    y_max = max([coord[1] for coord in screen_data.keys()])
    return x_max, y_max, result


def simulate_part_2(data, x_max, y_max, show_visualisation=False):
    vm = VM(data)
    vm.mem_put(0, 2)
    screen_data = {}
    score = 0
    ball_x = None
    paddle_x = None
    visualiser = None
    if show_visualisation:
        visualiser = Visualiser(x_max, y_max)
    while True:
        if show_visualisation:
            # Quit if the pygame window is closed
            if visualiser.check_quit():
                log_always("Exiting because window has quit")
                break
        _quit = False
        # Run until VM asks for input
        try:
            vm.run_until_input()
        except StopIteration:
            log.info("VM exited")
            _quit = True
        # Read output from VM
        _screen_data, _score, _ball_x, _ball_y, _paddle_x = parse_output(vm)
        screen_data.update(_screen_data)
        score = _score if _score is not None else score
        paddle_x = _paddle_x if _paddle_x is not None else paddle_x
        ball_x = _ball_x if _ball_x is not None else ball_x
        if show_visualisation:
            # Draw to screen
            visualiser.visualise(screen_data)
        if _quit:
            break
        # Send input to VM
        if ball_x is not None and paddle_x is not None:
            if ball_x > paddle_x:
                vm.input.put(INPUT_RIGHT)
            elif ball_x < paddle_x:
                vm.input.put(INPUT_LEFT)
            else:
                vm.input.put(INPUT_NONE)
        else:
            # Need to send input every loop - send nothing
            vm.input.put(INPUT_NONE)

    # If visualising, on end keep screen open
    if show_visualisation:
        visualiser.check_quit(3)
    return score


def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)

    # Part 1: Run with no input, read screen data
    log_always("Part 1")
    x_max, y_max, result = simulate_part_1(data)
    log_always(result)

    # Part 2: Run simulation
    log_always("Part 2")
    result = simulate_part_2(data, x_max, y_max, show_visualisation=args.verbose)
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
