from model.FiniteStateMachine import *
from model.cards import *
from CrazyEights import *
import time

def returnTrue(): return True

class CrazyEightsFSM(CrazyEights):

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def true(self) : return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup CrazyEights", self.setup)
        play = Play("Playing CrazyEights", self.run)
        goal = Goal("Ended CrazyEights")

        startToPlay = Transition(start, self.true, play)
        playToGoal = Transition(play, self.true, goal)

        self.fsm.addState(start)
        self.fsm.addState(play)
        self.fsm.addState(goal)

        self.fsm.run()

    def run(self):
        playerFSM = FiniteStateMachine()

        human = self.players[0]
        aiPlayer1 = self.players[1]
        aiPlayer2 = self.players[2]
        aiPlayer3 = self.players[3]

        start = Start("Start player loop", self.showGameBanner, self.printNextRound, (None, human))
        humanTurn = Play("Human Player", human.makeMove, self.printNextRound, (self, aiPlayer1))
        aiPlayer1Turn = Play("AI Player 1", aiPlayer1.makeMove, self.printNextRound, (self, aiPlayer2))
        aiPlayer2Turn = Play("AI Player 2", aiPlayer2.makeMove, self.printNextRound, (self, aiPlayer3))
        aiPlayer3Turn = Play("AI Player 3", aiPlayer3.makeMove, self.printNextRound, (self, human))
        humanWin = Goal("Win", self.playerWins)
        humanLoss = Fail("Lose", self.playerLoses)

        # Begin player loop
        startToHuman = Transition(start, returnTrue, humanTurn)

        # Defines the player loop
        humanToAI1   = Transition(humanTurn, returnTrue, aiPlayer1Turn)
        ai1ToAI2     = Transition(aiPlayer1Turn, returnTrue, aiPlayer2Turn)
        ai2ToAI3     = Transition(aiPlayer2Turn, returnTrue, aiPlayer3Turn)
        ai3ToHuman   = Transition(aiPlayer3Turn, returnTrue, humanTurn)

        #Defines win/loss conditions
        humanToWin   = Transition(humanTurn, self.checkWinCondition, humanWin, human)
        ai1ToLose    = Transition(aiPlayer1Turn, self.checkWinCondition, humanLoss, aiPlayer1)
        ai2ToLose    = Transition(aiPlayer2Turn, self.checkWinCondition, humanLoss, aiPlayer2)
        ai3ToLose    = Transition(aiPlayer3Turn, self.checkWinCondition, humanLoss, aiPlayer3)

        playerFSM.addState(start)
        playerFSM.addState(humanTurn)
        playerFSM.addState(aiPlayer1Turn)
        playerFSM.addState(aiPlayer2Turn)
        playerFSM.addState(aiPlayer3Turn)
        playerFSM.addState(humanWin)
        playerFSM.addState(humanLoss)

        playerFSM.run()

def __main__():
    
    try:
        game = CrazyEightsFSM()
    except:
        print("\n\nGame Ended unexpectedly.\n")
        exit()

if __name__ == '__main__':
    __main__()


