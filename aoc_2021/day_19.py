#!/usr/bin/env python3

import collections
import math
import sys
import traceback
import itertools
import numpy as np

from common.utils import *


# All 24 possible 90* rotations for a 3d object
ROTATIONS = [
    np.array(((-1, 0, 0), (0, -1, 0), (0, 0, 1))),
    np.array(((-1, 0, 0), (0, 0, -1), (0, -1, 0))),
    np.array(((-1, 0, 0), (0, 0, 1), (0, 1, 0))),
    np.array(((-1, 0, 0), (0, 1, 0), (0, 0, -1))),
    np.array(((0, -1, 0), (-1, 0, 0), (0, 0, -1))),
    np.array(((0, -1, 0), (0, 0, -1), (1, 0, 0))),
    np.array(((0, -1, 0), (0, 0, 1), (-1, 0, 0))),
    np.array(((0, -1, 0), (1, 0, 0), (0, 0, 1))),
    np.array(((0, 0, -1), (-1, 0, 0), (0, 1, 0))),
    np.array(((0, 0, -1), (0, -1, 0), (-1, 0, 0))),
    np.array(((0, 0, -1), (0, 1, 0), (1, 0, 0))),
    np.array(((0, 0, -1), (1, 0, 0), (0, -1, 0))),
    np.array(((0, 0, 1), (-1, 0, 0), (0, -1, 0))),
    np.array(((0, 0, 1), (0, -1, 0), (1, 0, 0))),
    np.array(((0, 0, 1), (0, 1, 0), (-1, 0, 0))),
    np.array(((0, 0, 1), (1, 0, 0), (0, 1, 0))),
    np.array(((0, 1, 0), (-1, 0, 0), (0, 0, 1))),
    np.array(((0, 1, 0), (0, 0, -1), (-1, 0, 0))),
    np.array(((0, 1, 0), (0, 0, 1), (1, 0, 0))),
    np.array(((0, 1, 0), (1, 0, 0), (0, 0, -1))),
    np.array(((1, 0, 0), (0, -1, 0), (0, 0, -1))),
    np.array(((1, 0, 0), (0, 0, -1), (0, 1, 0))),
    np.array(((1, 0, 0), (0, 0, 1), (0, -1, 0))),
    np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1))),
]


def rotate(coords, rotation):
    """ Rotate all coordinates in coords by rotation """
    return np.matmul(coords, rotation)


def is_match(coords_a, coords_b):
    """ Check if coords_a matches coords_b for any given rotation
        To match there must be at least 12 sensors at the same position.
        Returns a tuple of:
            Boolean: True if a match is found
            Offset (x,y,z array) of coords_b from coords_a
            coords_b rotated to the same orientation as coords_a shifted so that at least 12 sensors match coords_a
    """
    len_a = coords_a.shape[0]
    len_b = coords_b.shape[0]
    # For every combination of coordinates in coord_a and coord_b:
    for coord_a in coords_a:
        for coord_b in coords_b:
            # Calculate the offset of coord_a from coord_b
            offset = coord_a - coord_b
            # Apply that offset to all offsets in coords_b
            _coords_b = coords_b + offset
            # Count the number of coordinates that are the same at that offset
            len_ab = np.unique(np.concatenate([coords_a, _coords_b], axis=0), axis=0).shape[0]
            matches = len_a + len_b - len_ab
            if matches >= 12:
                return True, offset, _coords_b
    return False, None, None


def find_match(known_sensors, unknown_sensors, sensor_offsets, tried):
    """ Find the first sensor from unknown_sensors that matches a sensor in known_sensors
        To match there must be at least 12 sensors at the same position.
        If a sensor is found:
            * Add to known_sensors, at the orientation and offset required
            * Add the location (offset) of the found sensor to sensor_offsets
            * Remove from unknown_sensors
        tried is a dictionary of known_sensor.id: [unknown_sensor.id, ...] to prevent searching the same pair more than once
    """
    # For every combination of known sensors and unknown sensors:
    for known_id, known_coords in known_sensors.items():
        for unknown_id, unknown_coords in unknown_sensors.items():
            # Skip combinatoins that have already been checked - it won't work a second time around
            if unknown_id in tried[known_id]:
                continue
            # For every rotation:
            for rotation in ROTATIONS:
                # Apply the rotation to the unknown sensor coordinates
                _unknown_coords = rotate(unknown_coords, rotation)
                match, offset, new_coords = is_match(known_coords, _unknown_coords)
                if match:
                    log.info(f"Match found: {unknown_id} = {known_id} at {offset}")
                    known_sensors[unknown_id] = new_coords
                    sensor_offsets[unknown_id] = offset
                    del unknown_sensors[unknown_id]
                    return True
            tried[known_id].add(unknown_id)
    return False


def parse_block(lines):
    """ Parse a block of lines from input. A block contains information from a single sensor """
    _id = int(lines[0].split(" ")[2])
    beacons_dist = np.array([list(map(int, line.split(","))) for line in lines[1:]])
    return _id, beacons_dist


def main():
    args = parse_args()
    data_text = read_multilines(input_file_path_main(test=args.test))
    data = dict([parse_block(lines) for lines in data_text])

    known_sensors = {0: data[0]}
    sensor_offsets = {0: np.array([0, 0, 0])}
    unknown_sensors = {_id: coords for _id, coords in data.items() if _id not in known_sensors}
    tried = collections.defaultdict(set)
    while unknown_sensors:
        if not find_match(known_sensors, unknown_sensors, sensor_offsets, tried):
            log.error("Unable to match any more sensors?")
            break

    log.always("Part 1:")
    total_sensors = np.unique(
        np.concatenate(
            [coords for coords in known_sensors.values()],
            axis=0
        ),
        axis=0
    ).shape[0]
    log.always(total_sensors)

    log.always("Part 2:")
    distance_largest = 0
    _sensor_offsets = list(sensor_offsets.values())

    for i, coord_a in enumerate(_sensor_offsets):
        for coord_b in _sensor_offsets[i+1:]:
            distance = np.sum(np.abs(coord_b - coord_a))
            distance_largest = max(distance_largest, distance)
    log.always(distance_largest)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
