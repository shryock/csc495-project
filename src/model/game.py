import random

class UndefinedGameException(Exception):
    def __init__(self, message="Game parameter is undefined"):
        self.message = message


class Game():
    def __init__(self):
        self.name = 'Game'
        self.board = None
        self.rulebook = None
        self.players = []

        self.currentPlayer = -1
        self.moves = []
        self.selectedMove = -1
        self.quit = False

    def setup(self):
        raise NotImplementedError

    def goal(self):
        raise NotImplementedError

    def chooseMove(self):
        self.selectedMove = self.players[currentPlayer].chooseMove()

    def executeMove(self):
        raise NotImplementedError

    def printbanner(self):
        Logger.log(''.center(50))
        Logger.log('|', self.name.center(48), '|')
        Logger.log(''.center(50))

    def printBoard(self):
        Logger.log(repr(self.board))

    def printMoves(self):
        self.moves = self.rulebook.getMoves(self)
        for i in range(len(self.moves)):
            Logger.log('{:>4}. {}'.format(i, self.moves[i]))

    def printInvalidMoveMessage(self):
        Logger.log('Invalid move selection. Please try again.')


class Card():
    def __init__(self, rank, suit, visible=False):
        self.rank = rank
        self.suit = suit
        self.visible = visible
        if suit == 'Hearts' or suit == 'Diamonds':
            self.isRed = True
        else:
            self.isRed = False

    def __repr__(self):
        if self.visible:
            return '{:>3}{}'.format(self.rank, suitCharacters[self.suit])

    def makeVisible(self):
        self.visible = True

    def makeInvisible(self):
        self.visible = False

class Deck():
    def __init__(self):
        self.listOfCards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.listOfCards)

    def distributeCardsToPlayers(self, howManyEach, players):
        for player in players:
            for card in range(howManyEach):
                player.receiveCard(self.listOfCards.pop())

    def distributeCardsToPiles(self, howManyEach, piles):
        for i in range(len(piles)):
            for card in range(howManyEach[i]):
                piles[i].receiveCard(self.listOfCards.pop())


class Pile():
    def __init__(self, cards=None):
        self.cards = cards or []

    def __repr__(self):
        return repr(self.cards)

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def addCard(self, card):
        self.cards.append(card)

    def top(self):
        return self.cards[-1]

    def giveOneCard(self, otherPile):
        otherPile.receiveCard(self.cards.pop())

    def giveSetOfCards(self, indexToGive, otherPile):
        remainingCards = len(self.cards) - indexToGive
        for i in range(remainingCards):
            otherPile.receiveCard(self.cards.pop(indexToGive))

    def makeAllCardsVisible(self):
        for card in self.cards:
            card.makeVisible()

    def makeAllCardsInvisible(self):
        for card in self.cards:
            card.makeInvisible()

    def isEmpty(self):
        return len(self.cards) == 0

    def shuffle(self):
        random.shuffle(self.cards)


class Board():
    def __init__(self, piles=None):
        self.piles = piles or []

    def __repr__(self):
        raise NotImplementedError


class Rulebook():
    def true(self, payload):
        return true

    def validMove(self, payload):
        raise NotImplementedError

    def win(self, payload):
        raise NotImplementedError

    def quit(self, payload):
        raise NotImplementedError

    def getMoves(self, game):
        raise NotImplementedError


class Player():
    def __init__(self):
        self.hand = Pile()

    def receiveCard(self, card):
        raise NotImplementedError

    def chooseMove(self, game):
        raise NotImplementedError


class HumanPlayer(Player):
    def receiveCard(self, card):
        card.makeVisible()
        self.hand.receiveCard(card)

    def chooseMove(self, game):
        try:
            Logger.log('Choose your next move: ')
            selectedMove = int(input())
            Logger.log(str(selectedMove))
        except ValueError:
            selectedMove = -1
        return selectedMove


class AIPlayer(Player):
    def receiveCard(self, card):
        card.makeInvisible()
        self.hand.receiveCard(card)

    def chooseMove(self, game):
        raise NotImplementedError
