#!/usr/bin/env python3

import sys
import traceback
import copy

from common.utils import *


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
    player_1_win = len(cards1) > len(cards2)
    return cards1, cards2, player_1_win


def play_round(cards1, cards2):
    """ Play a single round of a regular game. Cards are modified in place """
    card1 = cards1.pop(0)
    card2 = cards2.pop(0)
    play_regular(card1, card2, cards1, cards2)


def play_regular(card1, card2, cards1, cards2):
    """ Play a regular game and allocate cards """
    log.verbose(f"Player 1: {card1} {cards1}")
    log.verbose(f"Player 1: {card2} {cards2}")
    allocate_cards(card1, card2, cards1, cards2, card1 > card2)


def allocate_cards(card1, card2, cards1, cards2, player_1_win):
    """ Allocate cards to player 1 if player_1_win, else to player 2"""
    if player_1_win:
        cards1.append(card1)
        cards1.append(card2)
    else:
        cards2.append(card2)
        cards2.append(card1)


def print_result(cards1, cards2, player_1_win):
    winner = "1" if player_1_win else "2"
    log.debug(f"Player 1: {cards1}")
    log.debug(f"Player 2: {cards2}")
    log.always(f"Winner: {winner}")
    log.always(f"Player 1: {calculate_score(cards1)}")
    log.always(f"Player 2: {calculate_score(cards2)}")


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


def play_game_recursive(cards1_in, cards2_in, g=1):
    """ Play a whole game using recursive rules
        Returns cards on completion and a boolean indicating if player 1 wins
    """
    # Copy cards
    cards1 = copy.copy(cards1_in)
    cards2 = copy.copy(cards2_in)
    # Make history
    history1 = []
    history2 = []
    r = 1
    try:
        # Loop
        while cards1 and cards2:
            play_round_recursive(cards1, cards2, history1, history2, g, r)
            r += 1
        player_1_win = len(cards1) > len(cards2)
    except GameOver as result:
        player_1_win = result.player_1_win
    return cards1, cards2, player_1_win


def play_round_recursive(cards1, cards2, history1, history2, g=1, r=1):
    """ Play a single round of a recursive game. Cards are modified in place
        Raises GameOver if this is an early end of game
    """
    log.debug(f"Game {g} Round {r}: {cards1} vs {cards2}")
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
        log.verbose(f"Playing a game {g+1} for cards {card1} {cards1}, {card2} {cards2}")
        _, _, player_1_win = play_game_recursive(_cards1, _cards2, g+1)
        winner = "1" if player_1_win else "2"
        log.verbose(f"Winner of game {g+1} for cards {card1} {cards1}, {card2} {cards2}: {winner}")
        allocate_cards(card1, card2, cards1, cards2, player_1_win)
    else:
        # Not recursive round: play a regular round
        play_regular(card1, card2, cards1, cards2)


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    cards1_str, cards2_str = read_multilines(data_file)
    cards1 = list(map(int, cards1_str[1:]))
    cards2 = list(map(int, cards2_str[1:]))

    log.always("Part 1")
    _cards1, _cards2, _player_1_win = play_game(cards1, cards2)
    print_result(_cards1, _cards2, _player_1_win)

    log.always("Part 2")
    _cards1, _cards2, _player_1_win = play_game_recursive(cards1, cards2)
    print_result(_cards1, _cards2, _player_1_win)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
