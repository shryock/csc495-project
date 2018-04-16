from model.game import *
from model.util import *
from view.CrazyEightsBoard import *
from games.CrazyEightsRulebook import *

class CrazyEights(Game):
    CARDS_PER_PLAYER = 5

    def setup(self):
        self.name = 'Crazy Eights'
        self.showRounds = True
        self.players = [HumanPlayer(), AIPlayer(), AIPlayer(), AIPlayer()]

        deck = Deck()
        deck.distributeCardsToPlayers(CrazyEights.CARDS_PER_PLAYER, self.players)

        drawPile = Pile('Deck', deck.cards)
        playPile = Pile('Play Pile')

        while drawPile.top().rank == '8':
            drawPile.shuffle()

        drawPile.giveOneCard(playPile)

        self.board = CrazyEightsBoard([drawPile, playPile])
        self.board.setup()

        self.rulebook = CrazyEightsRulebook()
        self.moves = {
            'MOVE': self.play,
            'DRAW': self.draw,
            'QUIT': self.quitGame
        }

    def play(self, move):
        if move.fromPile[move.cardIndex].rank == '8':
            newSuit = self.players[self.currentPlayer].chooseSuit()
            move.fromPile[move.cardIndex].suit = suits[newSuit]

        card = move.fromPile.remove(move.cardIndex)
        card.makeVisible()
        move.toPile.receiveCard(card)

    def draw(self, move):
        if not len(self.board.drawPile):
            self.board.playPile.giveSetOfCards(0, self.board.drawPile)
            self.board.drawPile.giveOneCard(self.board.playPile)
            self.board.drawPile.makeAllCardsInvisible()
            self.board.drawPile.shuffle()

        self.board.drawPile.giveOneCard(move.toPile)
        if self.playerIsHuman():
            move.toPile.top().makeVisible()
