# the purpose of this program is to lay the foundations to which our
# games and language can be built upon.

import random


suits = ["hearts", "spades", "clubs", "diamonds"]
possibleValues = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# how do we represent a rule?
class Rule:


class Player:
    # the turn will indicate whether the player can interact with the
    # game or not.
    turn = False

    # players start out with an empty hand
    hand = Hand()
    def __init__(self):
        pass


class Card:
    value = None
    suit = None

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return value + " of " + suit

# standard 52 card deck. We may want to add methods or variables
# for containing Jokers or other stuff.
class Deck:

    cards = []

    def __init__(self):
        for suit in suits:
            for value in possibleValues:
                cards.append( Card(value, suit) )

    def __repr__(self):
        return str(cards)

    # shuffles the deck of cards. Keep in mind the random
    # function for shuffling sorts in place and returns
    # nothing.
    def shuffle(self):
        random.shuffle(cards)

# for our sakes, a pile is a visible or invisible stack of cards
# who is owned by no player.
class Pile:
    cards = []
    visible = False

    def __init__(self, cards, visible):
        self.cards = cards
        self.visible = visible

    def pickUpCard(self):
        return cards.pop()

    def placeCard(self, card):
        cards.append(card)

     
class Hand:
    cards = []
    def __repr__(self):
        return str(cards)
    def __init__(self, cards):
        self.cards = cards
    def placeCard(self, card, pile):
        pile.placeCard(card)
        cards.remove(card)
    def pickUpCard(self, pile):
        cards.append( pile.pickUpCard())


# this was in menzies notes... but what is it?
class Play:

# how do we represent a goal?
class Goal:


class Game:
    goal = Goal()

    # every game has a set of piles... may be empty
    piles = []
    
    # whether the game is finished or not
    isFinished = False

    # Which player is the winner
    winner = None

    rules = []


