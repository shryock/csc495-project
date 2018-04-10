

class CrazyEightsRuleBook:

    def win(self, game):
        player = game.players[game.currentPlayer]
        return len(player.hand) == 0

    def canPlay(self, card):
        playPile = self.playPile
        topCard = playPile.top()
        # If the last card played was an 8 and the suit was changed...
        if self.suitChange is not None:
            canBePlayed = (card.suit == self.suitChange) or (card.rank == "8")
        # Normal game condition; no 8 was played
        else:
            canBePlayed = (card.suit == topCard.suit) or (card.rank == topCard.rank) or (card.rank == "8")
        return canBePlayed

    def getMoves(self, game):
        player = game.players[game.currentPlayer]
        playable_moves = []

        for card in player.hand:
            if self.canPlay(card):
                play_a_card = Move(card, player.hand, self.playPile, player, "play")
                playable_moves.append(play_a_card)

        #self.suitChange = None
        draw_a_card = Move(self.drawPile.top(), self.drawPile, player.hand, player, "draw")
        playable_moves.append(draw_a_card)
        return playable_moves

