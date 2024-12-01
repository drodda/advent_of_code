#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.files = {}
        self.subdirs = {}
        self.parent = parent
        if parent is not None:
            parent.subdirs[name] = self

    def size(self):
        """ Calculate total size of directory + subdirectories """
        return sum(self.files.values()) + sum([subdir.size() for subdir in self.subdirs.values()])

    @property
    def path(self):
        parent_path = self.parent.path + "/" if self.parent is not None else ""
        return parent_path + self.name

    def print(self):
        _path = "/" if self.path == "" else self.path
        log.info(f"{_path}:")
        for name, size in self.files.items():
            log.always(f"{self.path}/{name}\t{size}")
        for subdir in self.subdirs.values():
            subdir.print()

    @classmethod
    def parse(cls, lines):
        """ Parse lines into directory structure """
        if lines[0] != "$ cd /":
            log.error(f"Bad input: {lines[0]}")
            return

        root = cls("")
        current_dir = root
        for line in lines[1:]:
            if line.startswith("$ "):
                cmd = line[2:]
                if cmd == "ls":
                    pass
                elif cmd.startswith("cd "):
                    dest = cmd[3:]
                    if dest == "..":
                        current_dir = current_dir.parent
                    elif dest in current_dir.subdirs:
                        current_dir = current_dir.subdirs[dest]
                    else:
                        log.error(f"Bad command: {line} - subdir {dest} not in dir {current_dir.name}")
                else:
                    log.error(f"Bad command: {line}")
            else:
                size, name = line.split(" ")
                if size == "dir":
                    _d = Dir(name, current_dir)
                else:
                    current_dir.files[name] = int(size)
        return root


def solve_part1(d):
    """ Part 1: Find sum of all dirs with total size at most 10,0000 """
    result = 0
    if d.size() < 100000:
        result += d.size()
    for subdir in d.subdirs.values():
        result += solve_part1(subdir)
    return result


def solve_part2(d, space_required):
    """ Part 2: Find the largest dir with size less than space_required """
    result = None
    if d.size() >= space_required:
        result = d.size()
        for subdir in d.subdirs.values():
            _result = solve_part2(subdir, space_required)
            if _result is not None and _result < result:
                result = _result
    return result


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)

    root = Dir.parse(lines)
    if args.verbose:
        root.print()

    log.always("Part 1:")
    result = solve_part1(root)
    log.always(result)

    log.always("Part 2:")
    space_available = 70000000 - root.size()
    space_required = 30000000 - space_available
    result = solve_part2(root, space_required)
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
