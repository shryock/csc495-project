from model.game import *

class CrazyEightsRulebook(Rulebook):
    def win(self, game):
        player = game.players[game.currentPlayer]
        return len(player.hand) == 0

    def canPlay(self, card, game):
        topCard = game.board.playPile.top()
        return card.suit == topCard.suit or card.rank == topCard.rank or card.rank == '8'

    def getMoves(self, game):
        player = game.players[game.currentPlayer]
        moves = []

        for card in player.hand:
            if self.canPlay(card, game):
                cardIndex = player.hand.indexOf(card.face())
                moves += [Move(cardIndex, player.hand, game.board.playPile, 'MOVE')]
        moves += [Move(None, game.board.drawPile, player.hand, 'DRAW')]

        return moves
