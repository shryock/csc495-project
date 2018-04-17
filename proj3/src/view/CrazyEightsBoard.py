from model.game import *

class CrazyEightsBoard(Board):
    def __repr__(self):
        board  = 'Deck: {}\n'.format(repr(self.drawPile.top()) if len(self.drawPile) else None)
        board += 'Play Pile: {}'.format(repr(self.playPile.top()))
        return board

    def setup(self):
        self.drawPile = self.piles[0]
        self.playPile = self.piles[1]

        self.drawPile.makeAllCardsInvisible()
        self.playPile.makeAllCardsVisible()
