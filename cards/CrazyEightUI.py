import cards
import sys

class CrazyEightBoard:
    board = None

    def __init__(self, board):
        self.board = board
    
    def printBoard(self):
        for pile in self.board.setOfPiles:
            try:
                sys.stdout.write(repr(pile.getTop()) + "   ")
            except IndexError:
                sys.stdout.write("[ ]  ")


deck = cards.Deck()
deck.shuffle()
howMany = [1,51]
listOfPiles = deck.distributeCardsToPiles(howMany)

board = cards.Board(listOfPiles)
crazyeight = CrazyEightBoard(board)
crazyeight.printBoard()
