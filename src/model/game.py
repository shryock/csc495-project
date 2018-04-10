import random

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

    def chooseMove(self):
        self.selectedMove = self.players[currentPlayer].chooseMove()

    def executeMove(self):
        move = self.playerMoves[self.selectedMove]
        self.moves[move.type](move)

    def playerIsHuman(self):
        return self.players[self.currentPlayer].isA(HumanPlayer)

    def printbanner(self):
        Logger.log(''.center(50))
        Logger.log('|', self.name.center(48), '|')
        Logger.log(''.center(50))

    def printBoard(self):
        Logger.log(repr(self.board))

    def printMoves(self):
        self.moves = self.rulebook.getMoves(self)
        for i in range(len(self.moves)):
            Logger.log('{:>4}. {}'.format(i + 1, repr(self.moves[i])))

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
            return '{}{}'.format(self.rank, suitCharacters[self.suit])

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


class Move():
    def __init__(self, cardIndex, fromPile, toPile, moveType):
        self.cardIndex = cardIndex
        self.fromPile = fromPile
        self.toPile = toPile
        self.moveType = moveType

    def __repr__(self):
        if moveType == 'Draw':
            return 'Draw card from deck'
        elif moveType == 'Quit':
            return 'Quit'
        else:
            return '{} {} from {} to {}'.format(
                self.moveType, repr(self.fromPile[self.cardIndex]),
                fromPile.name, toPile.name)


class Rulebook():
    def true(self, game):
        return true

    def validMove(self, game):
        return game.selectedMove >= 0 and game.selectedMove < len(game.playerMoves)

    def quit(self, game):
        return game.selectedMove == len(game.playerMoves) - 1

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

    def chooseMove(self, game):
        raise NotImplementedError


class HumanPlayer(Player):
    def receiveCard(self, card):
        card.makeVisible()
        self.hand.receiveCard(card)

    def chooseMove(self, game):
        try:
            Logger.log('Choose your next move: ')
            selectedMove = int(input()) - 1
            Logger.log(str(selectedMove))
        except ValueError:
            selectedMove = -1
        return selectedMove


class AIPlayer(Player):
    def receiveCard(self, card):
        card.makeInvisible()
        self.hand.receiveCard(card)

    def chooseMove(self, game):
        return 0
