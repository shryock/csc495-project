from model.game import *
from model.util import *
from view.SolitaireBoard import *
from games.SolitaireRulebook import *

class Solitaire(Game):
    HOW_MANY = [1,2,3,4,5,6,7,0,0,0,0,0,24]

    def setup(self):
        self.name = 'Solitaire'
        self.piles = [Pile(None) for _ in Solitaire.HOW_MANY]
        Deck().distributeCardsToPiles(Solitaire.HOW_MANY, self.piles)

        self.board = SolitaireBoard(self.piles)
        self.board.setup()

        self.rulebook = SolitaireRulebook()
        self.players = [HumanPlayer()]
        self.moves = {
            'MOVE': self.move,
            'SHOW': self.show,
            'DRAW': self.draw,
            'RESHUFFLE': self.reshuffle,
            'QUIT': self.quitGame
        }

    def goal(self):
        pass

    def move(self, move):
        move.fromPile.giveSetOfCards(move.cardIndex, move.toPile)

    def show(self, move):
        move.fromPile.top().makeVisible()

    def draw(self, move):
        self.board.deck.giveOneCard(self.board.waste)
        self.board.waste.top().makeVisible()

    def reshuffle(self, move):
        self.board.waste.makeAllCardsInvisible()
        self.board.waste.cards.reverse()
        self.board.waste.giveSetOfCards(0, self.board.deck)
