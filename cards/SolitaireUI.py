import cards
import sys

class SolitaireBoard:
    board = None

    def __init__(self, board):
        self.board = board

    def printBoard(self):

        for index in range(1):
            for pile in self.board.setOfPiles[8:12]:
                try:
                    sys.stdout.write(repr(pile.cards[-1]) + " ")
                except IndexError:
                    sys.stdout.write("[ ]")
            sys.stdout.write("\n")

        print()

        for index in range(0,7):
            for pile in self.board.setOfPiles[0:8]:
                try:
                    sys.stdout.write(repr(pile.cards[index]) + " ")
                except IndexError:
                    sys.stdout.write("    ")
            sys.stdout.write("\n")



    def printPossibleMoves(self):
        print()


deck = cards.Deck()
howMany = [1,2,3,4,5,6,7,0,0,0,0,0,24]
listOfPiles = deck.distributeCardsToPiles(howMany)
board = cards.Board(listOfPiles)

solitaire = SolitaireBoard(board)
solitaire.printBoard()
