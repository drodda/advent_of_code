#!/usr/bin/env python3
import os
import queue
import time
import traceback

from utils import *
from intcode_vm import *

try:
    # Import pygame for to visualise output if it is installed
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
except ImportError:
    pygame = None


OBJECT_EMPTY = 0
OBJECT_WALL = 1
OBJECT_BLOCK = 2
OBJECT_HORIZONTAL_PADDLE = 3
OBJECT_BALL = 4

INPUT_NONE = 0
INPUT_LEFT = -1
INPUT_RIGHT = 1


COLOR_BLANK = (64, 64, 64)  # Grey
COLOR_MAP = {
    OBJECT_EMPTY: COLOR_BLANK,
    OBJECT_WALL: (0, 0, 0),  # Black
    OBJECT_BLOCK: (252, 186, 3),  # Orange
    OBJECT_HORIZONTAL_PADDLE: (150, 117, 60),  # Brown
    OBJECT_BALL: (9, 181, 66),  # Green
}
DISPLAY_SCALE = 20


def display_scale(v):
    """ Scale coordinate to display """
    return v * DISPLAY_SCALE


def visualise_init(x_max, y_max):
    """ Init pygame. Return screen object """
    pygame.init()
    screen = pygame.display.set_mode(((x_max + 1) * DISPLAY_SCALE, (y_max + 1) * DISPLAY_SCALE))
    screen.fill(COLOR_BLANK)
    return screen


def visualise(screen, screen_data):
    """ Draw to screen """
    screen.fill(COLOR_BLANK)
    for (x, y), val in screen_data.items():
        _rect = pygame.draw.rect(
            screen,
            COLOR_MAP[val],
            [display_scale(x), display_scale(y), DISPLAY_SCALE - 1, DISPLAY_SCALE - 1]
        )
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def visualise_check_quit(timeout=None):
    """ Check if pygame window has quit. Wait up to timeout seconds, if supplied """
    # Initialise static function variable
    visualise_check_quit._quit = getattr(visualise_check_quit, "_quit", False)
    start = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visualise_check_quit._quit = True
        if visualise_check_quit._quit:
            return True
        if timeout is None or (time.time() - start) > timeout:
            return False


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
    if show_visualisation and pygame is not None:
        screen = visualise_init(x_max, y_max)
    else:
        screen = None
    while True:
        if pygame is not None and show_visualisation:
            # Quit if the pygame window is closed
            if visualise_check_quit():
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
        # Draw to screen
        if show_visualisation and pygame is not None:
            visualise(screen, screen_data)
            time.sleep(1 / 1000)
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
    if show_visualisation and pygame is not None:
        visualise(screen, screen_data)
        visualise_check_quit(3)
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
