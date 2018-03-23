# the purpose of this program is to lay the foundations to which our
# games and language can be built upon.
import random

suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suitCharacters = {"Hearts": "\u2665", "Spades": "\u2660", "Clubs": "\u2663", "Diamonds": "\u2666"}

class Card:
    def __init__(self, rank, suit, visible):
        self.rank = rank
        self.suit = suit
        self.visible = visible
        if suit == "Hearts" or suit == "Diamonds":
            self.isRed = True
        else:
            self.isRed = False

    def __repr__(self):
        if self.visible:
            return "%4s" % ("" + self.rank + suitCharacters[self.suit])
        else:
            return "%4s" % "[ ]"

    def makeVisible(self):
        self.visible = True

    def makeInvisible(self):
        self.visible = False

# standard 52 card deck. We may want to add methods or variables
# for containing Jokers or other stuff.
class Deck:
    def __init__(self):
        self.listOfCards = [Card(rank, suit, False) for suit in suits for rank in ranks]
        self.shuffle()

    def __repr__(self):
        return self.listOfCards

    # shuffles the deck of cards. Keep in mind the random
    # function for shuffling sorts in place and returns
    # nothing.
    def shuffle(self):
        random.shuffle(self.listOfCards)

    # distributes a certain number of cards to each player
    def distributeCardsToPlayers(self, howManyEach, players):
        for player in players:
            for card in range(0, howManyEach):
                player.receiveCard(self.listOfCards.pop())

    # distinction between players and piles:
    # Piles have an unknown amount of cards per pile.
    # input will be a list of integers that each pile should
    # have and return the list of piles
    # this will be used to create a board.
    def distributeCardsToPiles(self, howMany):
        listOfPiles = []
        # iterate through list of integers
        # ex. [1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 24] for solitaire
        for pileAmount in howMany:
            pile = Pile()
            for i in range(pileAmount):
                pile.receiveCard( self.listOfCards.pop() )
            listOfPiles.append(pile)
        return listOfPiles

# this is the highest point of the model. Refer to UML in git.
class Game:
    def __init__(self):
        self.deck = Deck()
        self.board = None
        self.players = None
        self.rulebook = None
        self.setup()

    def __repr__(self):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError


# this is meant to be a generator of possible moves.
# to be inherited and implemented in game-specific code.
class RuleBook:
    def getAllPossibleMoves(self, board):
        raise NotImplementedError

# for our sakes, a pile is a stack of cards
# who is owned by no player. Each pile also
# has a set of rules, or list of playable moves
class Pile:
    def __repr__(self):
        return str([card for card in self.cards])

    def __init__(self, cards=None):
        self.cards = cards or []

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def receiveCard(self, card):
        self.cards.append(card)

    def top(self):
        return self.cards[-1]

    def getContents(self):
        return self.cards

    # this function will give one card from one pile to
    # another pile. Useful when flipping one card over or
    # picking up a card from the center pile into a hand.
    def giveOneCard(self, otherPile):
        otherPile.receiveCard(self.cards.pop())

    # This function will give every card from [indexToGive] to
    # the end of the list. Useful for instances like solitaire.
    def giveSetOfCards(self, indexToGive, otherPile):
        remainingCards = len(self.cards) - indexToGive
        for i in range(remainingCards):
            otherPile.receiveCard(self.cards.pop(indexToGive))

    def makeAllCardsInvisible(self):
        for card in self.cards:
            card.visible = False

    def makeAllCardsVisible(self):
        for card in self.cards:
            card.visible = True
    def isEmpty(self):
        return len(self.cards) == 0

    def replaceWith(self, otherPile):
        self = otherPile.getContents()
        self.makeAllCardsInvisible()
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.getContents())
        
class Player:
    name = ""

    # players start out with an empty hand
    def __init__(self, hand=None):
        self.hand = hand

    def receiveCard(self, card):
        if self.hand:
            self.hand.receiveCard(card)

    def isA(self, otherPlayerType):
        return isinstance(self, otherPlayerType)
class Board:
    def __init__(self, piles=None):
        self.piles = piles or []
    # boards are game specific.
    def printBoard(self):
        raise NotImplementedError
    def printPossibleMoves(self):
        raise NotImplementedError
