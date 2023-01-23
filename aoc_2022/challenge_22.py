#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


def parse_input(test=False):
    world, path_str = read_multilines(data_file_path_main(test=test))

    path = []
    s = ""
    for line in path_str:
        for c in line:
            if c.isnumeric():
                s += c
            else:
                if s:
                    path.append(int(s))
                    s = ""
                path.append(c)
    if s:
        path.append(int(s))

    # Pad world with spaces
    line_max = max([len(line) for line in world])
    world = [line + " " * (line_max - len(line)) for line in world]

    return world, path


class FlatGrid:
    """ Interpret world as a flat plane, warp along cartesian directions """

    # Cardinal Directions
    DIRECTIONS = {
        "North": (0, -1),
        "East": (1, 0),
        "South": (0, 1),
        "West": (-1, 0),
    }

    TURNS = {
        "North": {"L": "West", "R": "East", "Straight": "North", "Reverse": "South"},
        "East": {"L": "North", "R": "South", "Straight": "East", "Reverse": "West"},
        "South": {"L": "East", "R": "West", "Straight": "South", "Reverse": "North"},
        "West": {"L": "South", "R": "North", "Straight": "West", "Reverse": "East"},
    }

    REVERSE_TURN = {
        start_dir: {end_dir: turn for turn, end_dir in turns.items()}
        for start_dir, turns in TURNS.items()
    }

    REVERSE_ROTATE = {
        "Straight": "Straight",
        "R": "L",
        "Reverse": "Reverse",
        "L": "R",
    }

    DIRECTION_VAL = {
        "East": 0,
        "South": 1,
        "West": 2,
        "North": 3,
    }

    def __init__(self, world, path):
        self.world = world
        self.path = path
        self.len_x = len(world[0])
        self.len_y = len(world)

    @classmethod
    def move(cls, pos, grid_dir):
        """ Move position 1 step in given direction """
        return pos[0] + cls.DIRECTIONS[grid_dir][0], pos[1] + cls.DIRECTIONS[grid_dir][1]

    def solve(self):
        y = 0
        x = 0
        grid_dir = "East"
        # Find start position
        while self.world[y][x] != ".":
            x, y = self.move((x, y), grid_dir)
        log.info(f"Start: {x, y}")
        for i, instr in enumerate(self.path):
            if isinstance(instr, int):
                # Move
                log.debug(f"{i: 3d}: Moving {instr} from {x, y} {grid_dir}")
                _x = x
                _y = y
                for step in range(instr):
                    # Move in current direction
                    _x, _y = self.move((x, y), grid_dir)
                    _grid_dir = grid_dir
                    if _x < 0 or _y < 0 or _x >= self.len_x or _y >= self.len_y or self.world[_y][_x] == " ":
                        # Warp
                        _x, _y, _grid_dir = self.warp(x, y, grid_dir)
                    if self.world[_y][_x] == "#":
                        # End move
                        log.debug(f"\tMove stopped")
                        break
                    # Actually move
                    x, y, grid_dir = _x, _y, _grid_dir
                    log.debug(f"\tMoved {i}/{step}: {x, y}")

                log.info(f"{i: 3d}: Moved {instr}: {x, y} {grid_dir}")
            else:
                # Turn
                grid_dir = self.TURNS[grid_dir][instr]
                log.info(f"{i: 3d}: Turned {instr}: {grid_dir}")

        return 1000 * (y + 1) + 4 * (x + 1) + self.DIRECTION_VAL[grid_dir]

    def warp(self, x, y, grid_dir):
        while True:
            x, y = self.move((x, y), grid_dir)
            x = x % self.len_x
            y = y % self.len_y
            if self.world[y][x] != " ":
                return x, y, grid_dir


class CubeGrid(FlatGrid):
    """  """

    # Map of connected pairs of edges on a cube
    _CUBE_EDGES = (
        # Horizontal plane
        (("Front", "East"), ("Right", "West")),
        (("Front", "West"), ("Left", "East")),
        (("Back", "East"), ("Left", "West")),
        (("Back", "West"), ("Right", "East")),
        # Top
        (("Front", "North"), ("Top", "South")),
        (("Right", "North"), ("Top", "East")),
        (("Back", "North"), ("Top", "North")),
        (("Left", "North"), ("Top", "West")),
        # Bottom
        (("Front", "South"), ("Bottom", "South")),
        (("Right", "South"), ("Bottom", "West")),
        (("Back", "South"), ("Bottom", "North")),
        (("Left", "South"), ("Bottom", "East")),
    )

    # Full map of all connected pairs of edges
    CUBE_EDGES = dict(_CUBE_EDGES + tuple((v, k) for k, v in _CUBE_EDGES))

    def __init__(self, world, path):
        super().__init__(world, path)
        self.face_size = int(max(len(world), len(world[0])) / 4)
        self.width = int(len(world[0]) / self.face_size)
        self.height = int(len(world) / self.face_size)
        self.is_wide = len(world[0]) > len(world)
        self.faces = set()
        for y in range(self.height):
            for x in range(self.width):
                if world[y * self.face_size][x * self.face_size] != " ":
                    self.faces.add((x, y))

        # Calculate edges
        edges_set = set()
        for face in self.faces:
            for grid_dir in self.DIRECTIONS:
                _face = self.move(face, grid_dir)
                if _face not in self.faces:
                    edges_set.add((face, grid_dir))

        # Map faces onto cube. Face (1, 1) is always a valid face: use as a starting point
        self.grid_to_cube_face_map = {(1, 1): "Front"}
        self.cube_orientations = {(1, 1): "Straight"}
        q = collections.deque(self.grid_to_cube_face_map.keys())
        while q:
            face = q.pop()
            cube_face = self.grid_to_cube_face_map[face]
            orientation = self.cube_orientations[face]
            for grid_dir in self.DIRECTIONS:
                _face = self.move(face, grid_dir)
                if _face not in self.faces:
                    continue
                if _face in self.grid_to_cube_face_map:
                    continue
                # Apply orientation to grid direction to work out cube direction
                cube_dir = self.TURNS[grid_dir][orientation]
                # Calculate new grid face and true orientation
                _cube_face, _reverse_cube_dir = self.CUBE_EDGES[(cube_face, cube_dir)]
                _cube_dir = self.TURNS[_reverse_cube_dir]["Reverse"]
                # Calculate new cube face orientation: rotation between grid direction and new face cube direction
                _orientation = self.REVERSE_TURN[grid_dir][_cube_dir]
                self.grid_to_cube_face_map[_face] = _cube_face
                self.cube_orientations[_face] = _orientation
                q.append(_face)
        self.cube_to_grid_face_map = {cube_face: face for face, cube_face in self.grid_to_cube_face_map.items()}

        # Map edges
        self.edges = {}
        for edge in sorted(edges_set):
            grid_face, grid_dir = edge
            # Identify cube face and orientation
            cube_face = self.grid_to_cube_face_map[grid_face]
            cube_dir = self.TURNS[grid_dir][self.cube_orientations[grid_face]]
            # Identify cube neighbour
            _cube_face, _cube_dir = self.CUBE_EDGES[(cube_face, cube_dir)]
            # Identify grid neighbour
            _grid_face = self.cube_to_grid_face_map[_cube_face]
            _cube_turn = self.REVERSE_ROTATE[self.cube_orientations[_grid_face]]
            _grid_dir = self.TURNS[_cube_dir][_cube_turn]
            _edge = (_grid_face, _grid_dir)
            self.edges[edge] = _edge
            # Sanity check reverse edge
            if _edge in self.edges:
                if self.edges[_edge] != edge:
                    log.error(f"ERROR: Edge calculations do not compute: {edge} => {_edge} => {self.edges[_edge]}")

    def warp(self, x, y, grid_dir):
        face = (x // self.face_size, y // self.face_size)
        edge = (face, grid_dir)
        face_x = x % self.face_size
        face_y = y % self.face_size
        # Calculate distance from left corner
        if grid_dir == "North":
            face_v = face_x
        elif grid_dir in "East":
            face_v = face_y
        elif grid_dir in "South":
            face_v = self.face_size - face_x - 1
        elif grid_dir in "West":
            face_v = self.face_size - face_y - 1
        _edge = self.edges[edge]
        _face, _reverse_grid_dir = _edge
        _grid_dir = self.TURNS[_reverse_grid_dir]["Reverse"]
        # Apply distance from left corner to new face
        if _grid_dir == "North":
            _face_x = face_v
            _face_y = self.face_size - 1
        elif _grid_dir == "East":
            _face_x = 0
            _face_y = face_v
        elif _grid_dir == "South":
            _face_x = self.face_size - face_v - 1
            _face_y = 0
        elif _grid_dir == "West":
            _face_x = self.face_size - 1
            _face_y = self.face_size - face_v - 1
        _x = _face[0] * self.face_size + _face_x
        _y = _face[1] * self.face_size + _face_y
        return _x, _y, _grid_dir


def main():
    args = parse_args()
    world, path = parse_input(test=args.test)

    log.always("Part 1:")
    flat_grid = FlatGrid(world, path)
    result = flat_grid.solve()
    log.always(result)

    log.always("Part 2:")
    cube_grid = CubeGrid(world, path)
    result = cube_grid.solve()
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
