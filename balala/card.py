from pygame import Rect
import random

order = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
]

card_chips = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
]

suit_names = [
    "Spades", "Hearts", "Clubs", "Diamonds"
]

card_names = [
    2, 3, 4, 5, 6, 7, 8, 9, 10,
    "Jack", "Queen", "King", "Ace"
]

suits = "SHCD"

class Card:
    def __init__(self, rank, suit):
        self.rank = order.index(rank)
        self.suit = suits.index(suit)
        self.chips = card_chips[self.rank]
    
    def print(self):
        print(f"{card_names[self.rank]} of {suit_names[self.suit]}")

hand = []

def get_card_from_user():
    card = input("? ").upper()
    return Card(card[0], card[1])

for i in range(5):
    hand.append(get_card_from_user())

for i in hand:
    i.print()

def check_for_pair(hand):
    for i in hand:
        for j in hand:
            if i == j: continue
            if i.rank == j.rank: return True
    
    return False

def check_for_two_pair(hand):
    pairs = []

    for i in hand:
        for j in hand:
            if i == j: continue
            if [i.rank, j.rank] in pairs or [j.rank, i.rank] in pairs: continue
            if i.rank == j.rank: pairs.append([i.rank, j.rank])

    return len(pairs) >= 2

def check_for_three_of_a_kind(hand):
    checks = {}

    for i in hand:
        if i.rank not in checks.keys():
            checks[i.rank] = 1
        
        else:
            checks[i.rank] += 1
    
    for i in checks:
        if checks[i] >= 3: return True

    return False

def check_for_four_of_a_kind(hand):
    checks = {}

    for i in hand:
        if i.rank not in checks.keys():
            checks[i.rank] = 1
        
        else:
            checks[i.rank] += 1
    
    for i in checks:
        if checks[i] >= 4: return True

    return False

def check_for_five_of_a_kind(hand):
    checks = {}

    for i in hand:
        if i.rank not in checks.keys():
            checks[i.rank] = 1
        
        else:
            checks[i.rank] += 1
    
    for i in checks:
        if checks[i] == 5: return True

    return False

def check_for_flush_five(hand):
    return check_for_flush(hand) and check_for_five_of_a_kind(hand)

def check_for_full_house(hand):
    checks = {}

    for i in hand:
        if i.rank not in checks.keys():
            checks[i.rank] = 1
        
        else:
            checks[i.rank] += 1

    three, two = False, False

    for i in checks:
        if checks[i] == 3: three = True
        if checks[i] == 2: two = True

    return three and two

def check_for_flush(hand):
    suit = hand[0].suit
    isFlush = True

    if len(hand) < 5: return False

    for i in hand:
        isFlush = isFlush and i.suit == suit

    return isFlush

def check_for_flush_house(hand):
    return check_for_full_house(hand) and check_for_flush(hand)

def check_for_straight(hand):
    last = hand[0].rank

    if len(hand) < 5: return False

    for i in hand[1:]:
        if i.rank != last + 1: return False
        last += 1
    
    return True

def check_for_straight_flush(hand):
    return check_for_straight(hand) and check_for_flush(hand)

def placeholder(hand): return False

hand_names = [
    "High Card",
    "Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
    "Flush House",
    "Five of a Kind",
    "Flush Five"
]

def calculate(hand):
    hand = sorted(hand, key= lambda x: x.rank)

    functions = [
        check_for_pair,
        check_for_two_pair,
        check_for_three_of_a_kind,
        check_for_straight,
        check_for_flush,
        check_for_full_house,
        check_for_four_of_a_kind,
        check_for_straight_flush,
        check_for_flush_house,
        check_for_five_of_a_kind,
        check_for_flush_five
    ]

    results = [
        True
    ]

    for i in functions:
        results.append(i(hand))

    index = len(results)

    for i in range(len(results) - 1, -1, -1):
        if results[i]:
            print(hand_names[i])
            return

calculate(hand)