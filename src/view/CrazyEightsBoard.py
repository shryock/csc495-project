from model import Logger
from model.cards import *
import time
from model.FiniteStateMachine import *

class CrazyEightsBoard:


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


    def printNextRound(self, player):
        self.playPile.top().makeVisible()

        if player.isA(HumanPlayer):
            Logger.log("Deck: " + str(self.drawPile.top()))
            Logger.log("Play Pile: " + str(self.playPile.top()))
            Logger.log("Your hand: " + str(player.hand))
        elif player.isA(AIPlayer):
            Logger.log("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        time.sleep(1)

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
            Logger.log("Choose your next move: ")
            self.playerMove = int(input())
            Logger.log(str(self.playerMove))
        except ValueError:
            self.playerMove = -1

    def executeMove(self, game):
        selectedMove = game.getMoves(self)[self.playerMove-1]
        suitChange = selectedMove.make()
        if selectedMove.type =="play" and selectedMove.card.rank == 8:
            game.suitChange = suitChange
        else:
            game.suitChange = None

       
