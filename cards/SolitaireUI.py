import cards
import sys

class SolitaireBoard:
    board = None

    def __init__(self, board):
        self.board = board

    # for this method, we are expecting that the boards piles 0-6 are the
    # playable cards, 7-10 are the Ace to King piles and 11-12 are the
    # excess cards
    def printBoard(self):
        sys.stdout.write(" ") 
        for pile in self.board.setOfPiles[7:11]:
            try:
                sys.stdout.write(repr(pile.getTop()) + " ")
            except IndexError:
                sys.stdout.write("[ ]  ")

        sys.stdout.write("     ")
        for pile in self.board.setOfPiles[11:13]:
            try:
                sys.stdout.write(repr(pile.getTop()))
            except IndexError:
                sys.stdout.write("[ ] ")
        sys.stdout.write("\n")

        print()

        for index in range(0,14):
            for pile in self.board.setOfPiles[0:7]:
                try:
                    sys.stdout.write(repr(pile.cards[index]) + " ")
                except IndexError:
                    sys.stdout.write("     ")
            sys.stdout.write("\n")

    def printPossibleMoves(self):
        print()

deck = cards.Deck()
deck.shuffle()
howMany = [1,2,3,4,5,6,7,0,0,0,0,0,24]
listOfPiles = deck.distributeCardsToPiles(howMany)
for pile in listOfPiles:
    pile.makeAllCardsVisible()
    for card in pile.cards[0:len(pile.cards) - 1]:
        card.visible = False

board = cards.Board(listOfPiles)

solitaire = SolitaireBoard(board)
solitaire.printBoard()
