# the purpose of this program is to lay the foundations to which our
# games and language can be built upon.
import random

suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
possibleValues = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

class Card:
    rank = None
    suit = None
    visible = True
    isRed = True

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
            return "%4s" % ("" + self.rank + self.suit[0])
        else:
            return "%4s" % "[ ]"

# standard 52 card deck. We may want to add methods or variables
# for containing Jokers or other stuff.
class Deck:
    listOfCards = []

    def __init__(self):
        for suit in suits:
            for value in possibleValues:
                self.listOfCards.append( Card(value, suit, False) )

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
            for card in howManyEach:
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
            pile = Pile([], None)
            for i in range(pileAmount):
                pile.receiveCard( self.listOfCards.pop() )
            listOfPiles.append(pile)
        return listOfPiles

# this is the highest point of the model. Refer to UML in git.
class Game:
    goal = ""
    listOfPlayers = []
    deck = Deck()
    board = None

    def __init__(self, goal, listOfPlayers):
        self.goal = goal
        self.listOfPlayers = listOfPlayers

    def __repr__(self):
        return self.goal + self.listOfPlayers + self.board


# this is meant to be a generator of possible moves.
# to be inherited and implemented in game-specific code.
class RuleBook:
    def getAllPossibleMoves(self):
        raise NotImplementedError

# for our sakes, a pile is a stack of cards
# who is owned by no player. Each pile also
# has a set of rules, or list of playable moves
class Pile:
    cards = []
    ruleBook = RuleBook()
    def __repr__(self):
        return str([card for card in self.cards])

    def __init__(self, cards, ruleBook):
        self.cards = cards
        self.ruleBook = ruleBook

    def receiveCard(self, card):
        self.cards.append(card)

    def getTop(self):
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
        
class Hand(Pile):
    owner = None

    def __repr__(self):
        return self.getCards()
    def __init__(self, owner, cards, rulebook):
        self.owner = owner
        Pile.__init__(self, cards, rulebook)

class Player:
    # players start out with an empty hand
    hand = None
    def __init__(self, hand):
        self.hand = hand

    def receiveCard(self, card):
        hand.receiveCard(card)

class Board:
    setOfPiles = []
    def __init__(self, setOfPiles):
        self.setOfPiles = setOfPiles
    # boards are game specific.
    def printBoard(self):
        raise NotImplementedError
    def printPossibleMoves(self):
        raise NotImplementedError

class Play:
    currentPlayer = None
    listOfPiles = []
    def __init__(self, currentPlayer, listOfPiles):
        self.currentPlayer = currentPlayer
        self.listOfPiles = listOfPiles

    def getAllPossibleMoves(self):
        raise NotImplementedError

