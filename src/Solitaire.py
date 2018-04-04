import sys
from model.cards import *
from view.SolitaireBoard import *
from model.SolitaireRulebook import *


MOVE      = 0
SHOW      = 1
DRAW      = 2
RESHUFFLE = 3
QUIT      = 4

class Solitaire(Game):
    HOW_MANY    = [1,2,3,4,5,6,7,0,0,0,0,0,24]

    def setup(self):
        self.players = [Player()]
        self.piles = Deck().distributeCardsToPiles(Solitaire.HOW_MANY)
        self.board = SolitaireBoard(self.piles)
        self.rulebook = SolitaireRulebook()
        self.index = -1
        self.moves = self.rulebook.getAllPossibleMoves(self.board)
        self.valid = True
        self.moveCount = 0
        self.showGameBanner()

    def play(self):
        try:
            if self.valid:
                self.executeMove(self.moves[self.index - 1])
                self.moveCount += 1
        except (KeyboardInterrupt, QuitException):
            print("\nGame Exited")
            exit()

    def checkValid(self):
        self.moves = self.rulebook.getAllPossibleMoves(self.board)
        print(repr(self.board), end="\n\n")
        print(self.getMoveDialogue(self.moves))
        try:
            nextMove = input("Choose your next move: ")
            self.index = int(nextMove) 
            self.valid = not (self.index > len(self.moves) or self.index <= 0)
        except ValueError:
            self.valid = False
        return self.valid 

    def checkWinCondition(self):
        for pile in self.board.suitPiles:
            if len(pile) < 13:
                return False
        return True

    def announceWinner(self):
        print("\n\nCongratulations!! You Win!!\n")

    def showGameBanner(self):
        print("\n"*2)
        print(" -----------------------------------------------")
        print("|                  SOLITAIRE                    |")
        print(" -----------------------------------------------")

    def getMoveDialogue(self, moves):
        return "\n".join(["%d. %s" % (i + 1, moves[i][0]) for i in range(len(moves))])

    def executeMove(self, move):
        tokens = move[0].split(" ")
        if move[1] == MOVE:
            self.move(tokens[1], tokens[3], tokens[5])
        elif move[1] == SHOW:
            self.show(tokens[1])
        elif move[1] == DRAW:
            self.draw()
        elif move[1] == RESHUFFLE:
            self.reshuffle()
        elif move[1] == QUIT:
            raise QuitException
        else:
            raise ValueError

    def getPileByName(self, name):
        for pile in self.piles:
            if pile.name == name:
                return pile
        return None

    def getCardPosition(self, value, pile):
        for i in range(len(pile.cards)):
            if pile[i].rank + pile[i].suit[0] == value:
                return i
        return -1

    def move(self, card, pile1, pile2):
        pile1 = self.getPileByName(pile1)
        pile2 = self.getPileByName(pile2)
        pos = self.getCardPosition(card, pile1)
        pile1.giveSetOfCards(pos, pile2)

    def show(self, pile):
        pile = self.getPileByName(pile)
        pile.top().visible = True

    def draw(self):
        self.board.stock.giveOneCard(self.board.waste)
        self.board.waste.top().visible = True

    def reshuffle(self):
        self.board.waste.makeAllCardsInvisible()
        self.board.waste.cards.reverse()
        self.board.waste.giveSetOfCards(0, self.board.stock)


class QuitException(Exception): pass
