from model.Logger import *
import random

suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suitCharacters = {"Hearts": "\u2665", "Spades": "\u2660", "Clubs": "\u2663", "Diamonds": "\u2666"}

class Game():
    def __init__(self):
        self.name = 'Game'
        self.board = None
        self.rulebook = None
        self.players = []
        self.moves = {}

        self.currentPlayer = -1
        self.playerMoves = []
        self.selectedMove = -1
        self.quit = False

    def setup(self):
        raise NotImplementedError

    def goal(self):
        raise NotImplementedError

    def quitGame(self, move):
        self.quit = True

    def chooseMove(self):
        self.selectedMove = self.players[self.currentPlayer].chooseMove()

    def executeMove(self):
        move = self.playerMoves[self.selectedMove]
        self.moves[move.moveType](move)

    def playerIsHuman(self):
        return self.players[self.currentPlayer].isA(HumanPlayer)

    def printBanner(self):
        log('-' * 50)
        log('|', self.name.center(48), '|')
        log('-' * 50, '\n')

    def printBoard(self):
        log(repr(self.board), '\n')

    def printMoves(self):
        self.playerMoves = self.rulebook.getMoves(self)
        self.playerMoves += [Move(None, None, None, 'QUIT')]
        for i in range(len(self.playerMoves)):
            log('{:>4}. {}'.format(i + 1, repr(self.playerMoves[i])))

    def printQuit(self):
        log('Player {} has quit the game'.format(self.currentPlayer + 1))

    def printInvalidMoveMessage(self):
        log('Invalid move selection. Please try again.', '\n')


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
            return '{}{}'.format(self.rank, suitCharacters[self.suit])
        else:
            return '[ ]'

    def makeVisible(self):
        self.visible = True

    def makeInvisible(self):
        self.visible = False


class Deck():
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def distributeCardsToPlayers(self, howManyEach, players):
        for player in players:
            for card in range(howManyEach):
                player.receiveCard(self.cards.pop())

    def distributeCardsToPiles(self, howManyEach, piles):
        for i in range(len(piles)):
            for card in range(howManyEach[i]):
                piles[i].receiveCard(self.cards.pop())


class Pile():
    def __init__(self, name, cards=None):
        self.name = name
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

    def indexOf(self, card):
        for i in range(len(self.cards)):
            if repr(self.cards[i]) == card:
                return i
        return -1

    def receiveCard(self, card):
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
        self.setup()

    def __repr__(self):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError


class Move():
    def __init__(self, cardIndex, fromPile, toPile, moveType):
        self.cardIndex = cardIndex
        self.fromPile = fromPile
        self.toPile = toPile
        self.moveType = moveType

    def __repr__(self):
        if self.moveType == 'DRAW':
            return 'Draw card from Deck'
        elif self.moveType == 'RESHUFFLE':
            return 'Reshuffle Deck'
        elif self.moveType == 'SHOW':
            return 'Show {}'.format(self.fromPile.name)
        elif self.moveType == 'QUIT':
            return 'Quit'
        else:
            return '{} {} from {} to {}'.format(
                self.moveType.title(),
                repr(self.fromPile[self.cardIndex]),
                self.fromPile.name,
                self.toPile.name)


class Rulebook():
    def true(self, game):
        return True

    def validMove(self, game):
        return game.selectedMove >= 0 and game.selectedMove < len(game.playerMoves)

    def quit(self, game):
        return game.quit

    def win(self, game):
        raise NotImplementedError

    def getMoves(self, game):
        raise NotImplementedError


class Player():
    def __init__(self):
        self.hand = Pile('Hand')

    def isA(self, type):
        return isinstance(self, type)

    def receiveCard(self, card):
        raise NotImplementedError

    def chooseMove(self):
        raise NotImplementedError


class HumanPlayer(Player):
    def receiveCard(self, card):
        card.makeVisible()
        self.hand.receiveCard(card)

    def chooseMove(self):
        try:
            log('\n', 'Choose your next move: ')
            selectedMove = int(input()) - 1
            log(str(selectedMove), printLog=False)
        except ValueError:
            selectedMove = -1
        return selectedMove


class AIPlayer(Player):
    def receiveCard(self, card):
        card.makeInvisible()
        self.hand.receiveCard(card)

    def chooseMove(self):
        return 0
