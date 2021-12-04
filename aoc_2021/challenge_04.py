#!/usr/bin/env python3
import copy
import os
import sys
import traceback
import numpy as np

from utils import *


VALUE_USED = -1


def play_bingo(boards, numbers, start=0):
    # boards = [np.copy(board) for board in boards]
    for _round, number in enumerate(numbers[start:]):
        for i, board in enumerate(boards):
            board[board == number] = VALUE_USED
            if is_winning_board(board):
                return start+_round, i, board
    return len(numbers), None, None


def calculate_part_1(boards, numbers):
    # Copy boards as this will modify
    boards = [np.copy(board) for board in boards]
    _round, i, board = play_bingo(boards, numbers)
    score = np.sum(board[board != VALUE_USED]) * numbers[_round]
    return score


def calculate_part_2(boards, numbers):
    # Copy boards as this will modify
    boards = [np.copy(board) for board in boards]
    _round = 0
    while _round < len(numbers):
        _round, i, board = play_bingo(boards, numbers, _round)
        if i is None:
            return None
        if len(boards) == 1:
            score = np.sum(board[board != VALUE_USED]) * numbers[_round]
            return score
        # Remove winning board
        boards.pop(i)
    return None


def create_board(data):
    grid = [list(map(int, row.split())) for row in data]
    return np.matrix(grid)


def is_winning_board(board):
    # Check rows
    for i in range(board.shape[0]):
        if np.all(board[i, :] == VALUE_USED):
            return True
    for i in range(board.shape[1]):
        if np.all(board[:, i] == VALUE_USED):
            return True
    # if np.all(np.diag(board) == VALUE_USED):
    #     return True
    # if np.all(np.diag(np.fliplr(board)) == VALUE_USED):
    #     return True
    return False




def main():
    args = parse_args()
    data = read_multilines(data_file_path_main(test=args.test))
    numbers = list(map(int, (",".join(next(data))).split(",")))
    # trace()

    # numbers = map(int, next(data).split(","))
    boards = [create_board(item) for item in data]
    log_always("Part 1:")
    log_always(calculate_part_1(boards, numbers))
    log_always("Part 2:")
    log_always(calculate_part_2(boards, numbers))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
