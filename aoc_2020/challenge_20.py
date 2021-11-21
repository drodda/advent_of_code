#!/usr/bin/env python3
import traceback
import numpy as np
import math

from utils import *


POS_TOP = 0
POS_LEFT = 1
POS_BOTTOM = 2
POS_RIGHT = 3

TARGET_SHAPE_STR = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n").splitlines()


class Tile:
    def __init__(self, tile_text):
        self.num = int(tile_text[0].strip(": ").split(" ")[1])
        self.array = text_to_array(tile_text[1:])
        self.recalculate_edges()

    def recalculate_edges(self):
        """ Calculate integer-representation of edges """
        self.edges = self.calculate_edges()
        self.edges_reversed = self.calculate_reverse_edges()

    @property
    def edge_top(self):
        return self.edges[POS_TOP]

    @property
    def edge_left(self):
        return self.edges[POS_LEFT]

    @property
    def edge_bottom(self):
        return self.edges[POS_BOTTOM]

    @property
    def edge_right(self):
        return self.edges[POS_RIGHT]

    def calculate_edges(self):
        return [
            self.edge_to_int(self.row(0)),   # Top
            self.edge_to_int(self.col(0)),   # Left
            self.edge_to_int(self.row(-1)),  # Bottom
            self.edge_to_int(self.col(-1)),  # Right
        ]

    def calculate_reverse_edges(self):
        return [
            self.edge_to_int(np.flip(self.row(0))),   # Top
            self.edge_to_int(np.flip(self.col(0))),   # Left
            self.edge_to_int(np.flip(self.row(-1))),  # Bottom
            self.edge_to_int(np.flip(self.col(-1))),  # Right
        ]

    def row(self, n):
        """ Return the nth row as a string """
        return self.array[n, :]

    def col(self, n):
        """ Return the nth column as a string """
        return self.array[:, n]

    @staticmethod
    def edge_to_int(edge):
        """ Calculate the integer representation of an edge (a row or column a numpy array) """
        edge_bin = "".join(["1" if v else "0" for v in edge])
        return int(edge_bin, 2)

    def rotate(self, n):
        """ Rotate counter-clockwise steps times """
        self.array = np.rot90(self.array, n)
        self.recalculate_edges()

    def rotate_to(self, edge, pos):
        """ Rotate and/or flip so that edge is at pos
            Positions are counted counter-clockwise from top
        """
        if edge not in self.edges and edge not in self.edges_reversed:
            raise RuntimeError(f"{self} cannot be rotated to match {edge}")
        # Determine the location of the desired edge
        current_pos = self.edges.index(edge) if edge in self.edges else self.edges_reversed.index(edge)
        # Rotate that to the desired position
        self.rotate(pos - current_pos)
        # Flip if necessary
        if self.edges[pos] != edge:
            if pos in [0, 2]:
                self.flip_horizontal()
            else:
                self.flip_vertical()

    def flip_vertical(self):
        """ Flip around the horizontal axis: top becomes bottom """
        self.array = np.flip(self.array, 0)
        self.recalculate_edges()

    def flip_horizontal(self):
        """ Flip around the vertical axis: left becomes right """
        self.array = np.flip(self.array, 1)
        self.recalculate_edges()

    @property
    def edges_all(self):
        return [self.edges, self.edges_reversed]

    @property
    def inner_array(self):
        return self.array[1:-1, 1:-1]

    def __repr__(self):
        return f"<Tile {self.num}>"


def find_neighbour(tiles, tile, pos):
    edge = tile.edges[pos]
    for _tile in tiles:
        if _tile == tile:
            continue
        if edge in _tile.edges or edge in _tile.edges_reversed:
            return _tile
    raise IndexError(f"No file with edge {edge}")


def text_to_array(text_lines):
    return np.array([[c == "#" for c in row] for row in text_lines])


def array_to_text(array):
    """ Convert array back to sting representation """
    return ["".join(["#" if i else "." for i in row]) for row in array]


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    data_text = read_multilines(data_file)
    tiles = [Tile(lines) for lines in data_text]
    n = int(math.sqrt(len(tiles)))

    # Find the value of all edges
    all_edges = []
    for tile in tiles:
        all_edges.extend(tile.edges)
        all_edges.extend(tile.edges_reversed)

    log_always("Part 1")
    # Corners are tiles that have only 2 edges that match other tiles
    corners = []
    part1_result = 1
    for tile in tiles:
        matched_edges = 0
        for edge in tile.edges:
            if all_edges.count(edge) == 2:
                matched_edges += 1
        if matched_edges == 2:
            log_debug(f"Corner: {tile}")
            corners.append(tile)
            part1_result *= tile.num
    log_always(part1_result)

    # Arrange tiles in order. Start with one of the corners
    corner = corners[0]
    # Rotate it so that the bottom and right edges have matching tiles
    matched_bottom = all_edges.count(corner.edge_bottom) == 2
    matched_right = all_edges.count(corner.edge_right) == 2
    if not (matched_bottom and matched_right):
        if matched_right:
            corner.rotate(-1)
        elif matched_bottom:
            corner.rotate(1)
        else:
            corner.rotate(2)

    # Build grid starting from corner
    rows = []
    try:
        for i in range(n):
            row = []
            if i == 0:
                # Row 0: use corner
                tile = corner
            else:
                # Row 1+: find the tile that is below corner
                neighbour = rows[-1][0]
                tile = find_neighbour(tiles, neighbour, POS_BOTTOM)
                tile.rotate_to(neighbour.edge_bottom, POS_TOP)
            row.append(tile)
            neighbour = tile
            for j in range(1, n):
                # Find tile to the right of neighbour
                tile = find_neighbour(tiles, neighbour, POS_RIGHT)
                tile.rotate_to(neighbour.edge_right, POS_LEFT)
                row.append(tile)
                neighbour = tile
            rows.append(row)
    except IndexError as e:
        traceback.print_exc()
        ipdb.set_trace()

    # Merge into a single grid
    grid = np.concatenate([np.concatenate([i.inner_array for i in row], axis=1) for row in rows])
    grid_x, grid_y = grid.shape

    target_shape_orig = text_to_array(TARGET_SHAPE_STR)
    target_shape_count = np.sum(target_shape_orig)

    monsters_found = 0
    for flip in range(2):
        target_shape = target_shape_orig
        if flip > 0:
            target_shape = np.flip(target_shape, 0)
        for rotation in range(4):
            target_shape = np.rot90(target_shape, rotation)
            target_x, target_y = target_shape.shape
            for i in range(grid_x - target_x):
                for j in range(grid_y - target_y):
                    grid_sub = grid[i:i+target_x, j:j+target_y]
                    if np.sum(np.multiply(grid_sub, target_shape)) == target_shape_count:
                        log_debug(f"Target found! {i} {j} {rotation}")
                        monsters_found +=1
    log_always("Part 2")
    part2_result = np.sum(grid) - monsters_found * np.sum(target_shape_orig)
    log_always(part2_result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
