import inspect
from collections import Counter
from functools import cmp_to_key
from typing import Dict, Set, Tuple

from util.process_input import read_puzzle

### DESCRIPTION ###
# In Camel Cards, you get a list of hands,
# and your goal is to order them based on the strength of each hand.
# A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
# The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

# Cards ranking:
# Every hand is exactly one type. From strongest to weakest, they are:

# 5 Five of a kind, where all five cards have the same label: AAAAA
# 4,1 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# 3,2 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# 3,1,1 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 2,2,1 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 2,1,1,1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 1,1,1,1,1 High card, where all cards' labels are distinct: 23456

# Second ordering rule
# If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.
#
# So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

Face = str
Value = int
Game = list[tuple[str, int]]
card_to_value: Dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def solve_puzzle(puzzle: list[str]) -> int:
    game = read_game(puzzle)
    game = order_game_by_hand_strength(game)
    result = count_wins(game)
    return result


def read_game(puzzle: list[str]) -> Game:
    game = []
    for row in puzzle:
        cards, bet = row.split(" ")
        game.append((cards, int(bet)))
    return game


def order_game_by_hand_strength(game: Game) -> Game:
    # sort game by hand strength, with compare_hands function
    # compare_hands accepts x[0] and y[0] to compare, but sort accepts only one argument...

    return sorted(game, key=cmp_to_key(compare_hands))

    # game.sort(cmp=lambda x, y: compare_hands(x[0], y[0]))


def count_wins(game: Game):
    wins = 0
    for rank, (hand, bet) in enumerate(game):
        print(rank, hand, bet, bet * (rank + 1))
        wins += bet * (rank + 1)
    return wins


def compare_hands(player1: str, player2: str) -> int:
    hand1 = player1[0]
    hand2 = player2[0]

    main_ordering = compare_hands_by_type(hand1, hand2)
    print(f"{inspect.stack()[0][3]} ({hand1}, {hand2}) {main_ordering=}")
    if main_ordering == 0:
        return compare_hands_by_card(hand1, hand2)
    else:
        return main_ordering


def compare_hands_by_type(hand1: str, hand2: str) -> int:
    # print(f"{inspect.stack()[0][3]}({hand1}, {hand2})")
    hand1 = substitute_J_with_any_card(hand1)
    hand2 = substitute_J_with_any_card(hand2)

    card_counts_1 = Counter(hand1).values()
    card_counts_2 = Counter(hand2).values()
    # print(card_counts_2, card_counts_1)
    counts_to_type = {
        (5,): 0,
        (4, 1): 1,
        (3, 2): 2,
        (3, 1, 1): 3,
        (2, 2, 1): 4,
        (2, 1, 1, 1): 5,
        (1, 1, 1, 1, 1): 6,
    }
    hand1_type = counts_to_type[tuple(sorted(card_counts_1, reverse=True))]
    hand2_type = counts_to_type[tuple(sorted(card_counts_2, reverse=True))]
    return -(hand1_type - hand2_type)


def compare_hands_by_card(hand1: str, hand2: str) -> int:
    for a, b in zip(hand1, hand2):
        if card_to_value[a] > card_to_value[b]:
            return 1
        elif card_to_value[a] < card_to_value[b]:
            return -1
    return 0


def substitute_J_with_any_card(hand: str) -> str:
    # 5J should be 5A
    # 4J and 1? should be 5?

    # 3J and 2X should be: 5X
    # 3J and 1? and 1? should be: 4X and 1?

    # 2J and 3X should be: 5X
    # 2J and 2X and 1? should be: 4X and 1?
    # 2J and 1? and 1? and 1? should be: 3X and 1? and 1?

    # 1J and 4X should be: 5X
    # 1J and 3X and 1? should be: 4X and 1?
    # 1J and 2X and 2Y should be: 3X and 2Y
    # 1J and 2X and 1? and 1? should be: 3X and 1? and 1?
    # 1J and 1? and 1? and 1? and 1? should be: 2X and 1? and 1? and 1?

    j_count = hand.count("J")
    # find most common card which is not J.
    if j_count == 5:
        return "AAAAA"
    best_card_to_substitute_j = Counter(hand.replace("J", "")).most_common()[0][0]
    hand = hand.replace("J", best_card_to_substitute_j)

    return hand


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: list[str] = read_puzzle("small_input.txt")
        print(solve_puzzle(puzzle))
        assert 6440 == solve_puzzle(puzzle)
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
