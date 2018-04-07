import os
import time
from model.cards import *
from model.FiniteStateMachine import *
from model import Logger
from view.CrazyEightsBoard import *

class CrazyEights:

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def setup(self):
        self.state = "running"

        self.players = []
        self.players.append(HumanPlayer())
        for i in range(0, CrazyEights.NUMBER_AI_PLAYERS):
            self.players.append(AIPlayer(i))

        self.suitChange = None

        deck = Deck()
        deck.shuffle()
        deck.distributeCardsToPlayers(5, self.players)

        self.drawPile = Pile(deck.listOfCards)
        while (self.drawPile.top().rank == "8"):
            Logger.log("There was an 8 at the top of the pile, so it was reshuffled.")
            random.shuffle(self.drawPile.getContents())


        self.playPile = Pile()
        self.drawPile.giveOneCard(self.playPile)

        self.winner = None

    def checkWinCondition(self, player):
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

    def getMoves(self, player):
        playable_moves = []
        
        for card in player.hand:
            if self.canPlay(card):
                play_a_card = Move(card, player.hand, self.playPile, player, "play")
                playable_moves.append(play_a_card)

        #self.suitChange = None
        draw_a_card = Move(self.drawPile.top(), self.drawPile, player.hand, player, "draw")
        playable_moves.append(draw_a_card)
        return playable_moves

class Move:
    def __init__(self, card, fromPile, toPile, player, moveType):
        self.card = card
        self.fromPile = fromPile
        self.toPile = toPile
        self.player = player
        self.type = moveType

    def __repr__(self):
        if (self.type == "play"):
            return "Move " + str(self.card) + " to the play pile."
        elif (self.type == "draw"):
            return "Draw card from the deck."

    def make(self):
        self.fromPile.getContents().remove(self.card)
        if self.player.isA(HumanPlayer):
            self.card.makeVisible()
        if self.player.isA(AIPlayer) and self.type == "draw":
            self.card.makeInvisible()
        self.toPile.receiveCard(self.card)

        if self.card.rank == "8" and self.type == "play":
            suitChoiceInput = None
            if self.player.isA(HumanPlayer):
                [Logger.log(str(i + 1) + ". ", suitCharacters[suits[i]]) for i in range(4)   ]
                Logger.log("Choose which suit to switch to: ")
                suitChoiceInput = input()
                Logger.log(str(suitChoiceInput) + '\n')
            elif self.player.isA(AIPlayer):
                suitChoiceInput = random.choice(range(1, 5))
            suitChoice = suits[int(suitChoiceInput)-1]
            Logger.log("Suit has been changed to ", suitCharacters[suitChoice])

            return suitChoice
