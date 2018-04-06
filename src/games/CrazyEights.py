import os
import time
from model.cards import *
from model.FiniteStateMachine import *
from model import Logger
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

    def showGameBanner(self):
        Logger.log("\n"*2)
        Logger.log(" -----------------------------------------------")
        Logger.log("|                CRAZY EIGHTS                   |")
        Logger.log(" -----------------------------------------------")

    def showRoundNumber(self, roundNumber):
        Logger.log("\n")
        Logger.log("==================== Round %s ====================" % str(roundNumber))
        Logger.log("\n")

    def playerWins(self):
        Logger.log("You won the game!")

    def playerLoses(self):
        Logger.log("You lost the game!")

    def checkWinCondition(self, player):
        return len(player.hand) == 0

    def printNextRound(self, player):
        self.playPile.top().makeVisible()

        if player.isA(HumanPlayer):
            Logger.log("Deck: " + str(self.drawPile.top()))
            Logger.log("Play Pile: " + str(self.playPile.top()))
            Logger.log("Your hand: " + str(player.hand))
        elif player.isA(AIPlayer):
            Logger.log("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        time.sleep(1)

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

class AIPlayer(Player):
    
    def __init__(self, index):
        self.index = index
        self.hand = None
        self.name = "Computer Player " + str(index)
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.makeInvisible()
        self.hand.receiveCard(card)

    def makeMove(self, game):
        allMoves = game.getMoves(self)
        allMoves[0].card.makeVisible()
        Logger.log("\t", allMoves[0])
        suitChange = allMoves[0].make()
        if suitChange is not None: game.suitChange = suitChange

class HumanPlayer(Player):
    name = "you"

    def __init__(self):
        self.hand = None
        self.playerMove = -1
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.makeVisible()
        self.hand.receiveCard(card)

    def makeMove(self, game):
        moveFSM = FiniteStateMachine()

        start = Start("Start Player Move loop", self.printMove, payload=(game, None))
        makeMove = Play("Choose move", self.chooseMove, payload=(game, None))
        validMove = Goal("Valid move", self.executeMove, payload=(game, None))

        startToMakeMove = Transition(start, lambda: True, makeMove)
        makeMoveToValidMove = Transition(makeMove, self.madeValidMove, validMove, payload=game)
        makeMoveToMakeMove = Transition(makeMove, lambda game: not self.madeValidMove(game), makeMove, payload=game)

        start.addTransition(startToMakeMove)
        makeMove.addTransition(makeMoveToValidMove)
        makeMove.addTransition(makeMoveToMakeMove)

        moveFSM.addState(start)
        moveFSM.addState(makeMove)
        moveFSM.addState(validMove)

        moveFSM.run()

    def madeValidMove(self, game):
        Logger.log("Player move %d" % self.playerMove)
        if self.playerMove > len(game.getMoves(self)) or self.playerMove <= 0:
            return False
        return True

    def printMove(self, game):
        allMoves = game.getMoves(self)
        for index, move in enumerate(allMoves):
            Logger.log("   %i. %s" % (index+1, str(move)))

    def chooseMove(self, game):
        try:
            self.playerMove = int(input("Choose your next move: "))
        except ValueError:
            self.playerMove = -1

    def executeMove(self, game):
        selectedMove = game.getMoves(self)[self.playerMove-1]
        suitChange = selectedMove.make()
        if selectedMove.type =="play" and selectedMove.card.rank == 8:
            game.suitChange = suitChange
        else:
            game.suitChange = None

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
                suitChoiceInput = input("Choose which suit to switch to: ")
            elif self.player.isA(AIPlayer):
                suitChoiceInput = random.choice(range(1, 5))
            suitChoice = suits[int(suitChoiceInput)-1]
            Logger.log("Suit has been changed to ", suitCharacters[suitChoice])

            # I really don't like doing this, but I'm going to because it's a hacky, temporary fix.
            return suitChoice
