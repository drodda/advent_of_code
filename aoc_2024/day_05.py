#!/usr/bin/env python3
import collections
import sys
import traceback

from common.utils import *


def parse_input(input_path):
    page_order_str, updates_str = read_multilines(input_path)
    pages_before = collections.defaultdict(set)
    for line in page_order_str:
        first, second = map(int, line.split("|"))
        # pages_after[first].add(second)
        pages_before[second].add(first)
    updates = [list(map(int, line.split(","))) for line in updates_str]
    return dict(pages_before), updates


def middle(lst):
    return lst[int((len(lst) - 1) / 2)]


def is_valid(pages_before, pages):
    for i, page in enumerate(pages):
        after = pages[i:]
        for page_before in pages_before.get(page, []):
            if page_before in after:
                return False
    return True


def solve_part1(pages_before, updates):
    result = 0
    for pages in updates:
        if is_valid(pages_before, pages):
            result += middle(pages)
    return result


def reorder(pages_before, pages):
    new_pages = []
    for i in range(len(pages)):
        # Find a page that can be inserted before all existing pages
        for page in pages:
            required_before = pages_before.get(page, [])
            if page not in new_pages and not set(pages).difference(new_pages + [page]).intersection(required_before):
                new_pages.append(page)
                break
        else:
            log.error(f"Unable to insert any page")
    return new_pages


def solve_part2(pages_before, updates):
    result = 0
    for pages in updates:
        if not is_valid(pages_before, pages):
            # Re-order
            new_pages = reorder(pages_before, pages)
            result += middle(new_pages)
    return result


def main():
    args = parse_args()
    pages_before, updates = parse_input(args.input)


    log.always("Part 1:")
    result = solve_part1(pages_before, updates)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(pages_before, updates)
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
