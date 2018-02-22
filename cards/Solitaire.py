from cards import *
from SolitaireBoard import *
from SolitaireRulebook import *


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

        self.moveCount = 0

    def play(self):
        try:
            moves = self.rulebook.getAllPossibleMoves(self.board)
            while moves:
                print(repr(self.board), end="\n\n")
                print(self.getMoveDialogue(moves))
                nextMove = input("Choose your next move: ")

                while True:
                    try:
                        index = int(nextMove)
                        if index > len(moves) or index <= 0:
                            raise ValueError
                        else:
                            break
                    except ValueError:
                        nextMove = input("Choose your next move: ")

                self.executeMove(moves[index - 1])
                self.moveCount += 1
                print("\n")
                moves = self.rulebook.getAllPossibleMoves(self.board)
            print("Game Over")
        except (KeyboardInterrupt, QuitException):
            print("\nGame Exited")

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

game = Solitaire()
game.play()
