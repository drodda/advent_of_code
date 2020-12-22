#!/usr/bin/env python3
import traceback
import collections
import copy

from utils import *

import ipdb


###############################################################################
# Regular game


def play_game(cards1_in, cards2_in):
    """ Play a whole game using regular rules """
    # Copy cards
    cards1 = copy.copy(cards1_in)
    cards2 = copy.copy(cards2_in)
    # Loop
    while cards1 and cards2:
        play_round(cards1, cards2)
    return cards1, cards2


def play_round(cards1, cards2):
    """ Play a single round of a regular game. Cards are modified in place """
    card1 = cards1.pop(0)
    card2 = cards2.pop(0)
    play_regular(card1, card2, cards1, cards2)


def play_regular(card1, card2, cards1, cards2):
    """ Play a regular game and allocate cards """
    print_verbose(f"Player 1: {card1} {cards1}")
    print_verbose(f"Player 1: {card2} {cards2}")
    allocate_cards(card1, card2, cards1, cards2, card1 > card2)


def allocate_cards(card1, card2, cards1, cards2, player_1_win):
    """ Allocate cards to player 1 if player_1_winner, else to player 2"""
    if player_1_win:
        cards1.append(card1)
        cards1.append(card2)
    else:
        cards2.append(card2)
        cards2.append(card1)


def calculate_score(cards):
    score = 0
    for i, card in enumerate(cards):
        score += (len(cards) - i) * card
    return score


###############################################################################
# Recursive game


class GameOver(Exception):
    """ Raised when a game ends """
    def __init__(self, player_1_win, cards1, cards2):
        self.player_1_win = bool(player_1_win)
        self.cards1 = cards1
        self.cards2 = cards2

    @property
    def winner(self):
        return 1 if self.player_1_win else 2

    def __str__(self):
        return f"Winner: Player {self.winner}"


def play_game_recursive(cards1_in, cards2_in, raise_on_exit=False, g=1):
    """ Play a whole game using recursive rules
        Returns cards on completion, unless raise_on_exit, in which case GameOver will be raised
    """
    # Copy cards
    cards1 = copy.copy(cards1_in)
    cards2 = copy.copy(cards2_in)
    # Make history
    history1 = []
    history2 = []
    r = 1
    try:
        while cards1 and cards2:
            play_round_recursive(cards1, cards2, history1, history2, g, r)
            r += 1
    except GameOver:
        pass
    if raise_on_exit:
        raise GameOver(len(cards1) > 0, cards1, cards2)
    return cards1, cards2


def play_round_recursive(cards1, cards2, history1, history2, g=1, r=1):
    """ Play a single round of a recursive game. Cards are modified in place
        Raises GameOver if this is an end of game
    """
    print_debug(f"Game {g} Round {r}: {cards1} vs {cards2}")
    if cards1 in history1 or cards2 in history2:
        raise GameOver(1, cards1, cards2)
    history1.append(copy.copy(cards1))
    history2.append(copy.copy(cards2))
    card1 = cards1.pop(0)
    card2 = cards2.pop(0)
    if len(cards1) >= card1 and len(cards2) >= card2:
        # Recurse! Copy cards
        _cards1 = cards1[:card1]
        _cards2 = cards2[:card2]
        # Play the game
        try:
            print_verbose(f"Playing a game {g+1} for cards {card1} {cards1}, {card2} {cards2}")
            play_game_recursive(_cards1, _cards2, True, g+1)
        except GameOver as result:
            print_verbose(f"Winner of game {g+1} for cards {card1} {cards1}, {card2} {cards2}: {result.winner}")
            allocate_cards(card1, card2, cards1, cards2, result.player_1_win)
    else:
        play_regular(card1, card2, cards1, cards2)


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    (_, *cards1_str), (_, *cards2_str) = read_multilines(data_file)
    cards1 = list(map(int, cards1_str))
    cards2 = list(map(int, cards2_str))

    print("Part 1")
    _cards1, _cards2 = play_game(cards1, cards2)
    print_debug(f"Player 1: {_cards1}")
    print_debug(f"Player 2: {_cards2}")
    print(f"Player 1: {calculate_score(_cards1)}")
    print(f"Player 2: {calculate_score(_cards2)}")

    print("Part 2")
    _cards1, _cards2 = play_game_recursive(cards1, cards2)
    print_debug(f"Player 1: {_cards1}")
    print_debug(f"Player 2: {_cards2}")
    print(f"Player 1: {calculate_score(_cards1)}")
    print(f"Player 2: {calculate_score(_cards2)}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
