#!/usr/bin/env python3
import collections
import sys
import traceback
from common.utils import *

SYM_START = "S"

DIRS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

REV_DIRS = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}

SYM_DIRS = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
}

SYM_NEXT_DIRS = {
    "N": {"|": "N", "7": "W", "F": "E"},
    "E": {"-": "E", "J": "N", "7": "S"},
    "S": {"|": "S", "J": "W", "L": "E"},
    "W": {"-": "W", "L": "N", "F": "S"},
}

LEFT_NEIGHBOURS = {
    "|": {"N": "W", "S": "E"},
    "-": {"E": "N", "W": "S"},
    "L": {"W": "SW", "S": ""},
    "J": {"S": "ES", "E": ""},
    "7": {"E": "", "N": ""},
    "F": {"N": "WN", "W": ""},
}


def find_start(data):
    # Find start
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == SYM_START:
                return y, x
    raise ValueError(f"Symbol {SYM_START} not found")


def move(data, y, x, _dir):
    dy, dx = DIRS[_dir]
    _y = y + dy
    _x = x + dx
    if not ((0 <= _y < len(data)) and (0 <= _x < len(data[_y]))):
        raise ValueError(f"Out of bounds: {_y},{_x} ({_dir} from {y},{x})")
    return _y, _x


def find_next(data, y, x, _dir):
    """ Calculate the next position and facing direction after entering (y, x) from _dir
    """
    sym = None
    try:
        sym = data[y][x]
        next_dir = SYM_NEXT_DIRS[_dir][sym]
        y, x = move(data, y, x, next_dir)
        return y, x, next_dir
    except KeyError:
        raise ValueError(f"Invalid move: {sym}")


def find_path(data):
    start_y, start_x = find_start(data)
    log.info(f"Start: {start_y, start_x}")
    for start_dir in DIRS:
        result = [(start_y, start_x)]
        log.info(f"Trying: {start_dir}")
        _dir = start_dir
        try:
            _len = 1
            y, x = move(data, start_y, start_x, start_dir)
            while (y, x) != (start_y, start_x):
                log.info(f"{_len}: {y},{x} {_dir} = {data[y][x]}")
                result.append((y, x))
                y, x, _dir = find_next(data, y, x, _dir)
                _len += 1
            return result
        except ValueError as e:
            log.info(f"Path {start_dir} failed: {e}")


def calculate_dir(y1, x1, y2, x2):
    dy = y2 - y1
    dx = x2 - x1
    for _dir, _dir_xy in DIRS.items():
        if (dy, dx) == _dir_xy:
            return _dir


def patch_start_position(data, path):
    data = data.copy()
    y, x = path[0]
    dir1 = calculate_dir(y, x, *path[1])
    dir2 = calculate_dir(y, x, *path[-1])
    dirs = sorted(dir1 + dir2)
    for _sym, _dirs in SYM_DIRS.items():
        if sorted(_dirs) == dirs:
            sym = _sym
            break
    else:
        raise ValueError(f"Unable to find start symbol for {dirs}")
    data[y] = "".join([sym if i == x else c for i, c in enumerate(data[y])])
    return data


def calculate_enclosed_region(data, path):
    # Find the north-most + west-most tile in path: this must be a "F"
    ind = path.index(min(path))
    y, x = path[ind]
    if data[y][x] != "F":
        log.error(f"ERROR: Expected start tile to be 'F', got {data[y][x]}")
        return None
    # Rearrange path to be (initially) counter-clockwise around north-west most point
    if path[(ind + 1) % len(path)] != (y + 1, x):
        path = list(reversed(path))

    # For tile element in path, check tiles to the left
    _y, _x = path[-1]
    area = set()
    for y, x in path:
        _dir = calculate_dir(_y, _x, y, x)
        for neighbour_dir in LEFT_NEIGHBOURS[data[y][x]][_dir]:
            neighbour = move(data, y, x, neighbour_dir)
            # Add to enclosed area if neighbour tile is not in path
            if neighbour not in path:
                area.add(neighbour)
        _y = y
        _x = x
    # Flood fill around known enclosed tiles up to path
    to_explore = collections.deque(area)
    while to_explore:
        pos = to_explore.pop()
        for _dir in DIRS:
            _pos = move(data, *pos, _dir)
            if _pos not in area and _pos not in path:
                area.add(_pos)
                to_explore.append(_pos)
    return len(area)


def main():
    args = parse_args()
    data = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    path = find_path(data)
    result = int(len(path)/2)
    log.always(result)

    data = patch_start_position(data, path)

    log.always("Part 2:")
    result = calculate_enclosed_region(data, path)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
