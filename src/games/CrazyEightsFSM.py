from model.FiniteStateMachine import *
from model.cards import *
from games.CrazyEights import *
import time
from view.CrazyEightsBoard import *

class CrazyEightsFSM(CrazyEights, CrazyEightsBoard):

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup CrazyEights", self.setup)
        play = Play("Playing CrazyEights", self.run)
        goal = Goal("Ended CrazyEights")

        Transition(start, lambda: True, play)
        Transition(play, lambda: True, goal)

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
        startToHuman = Transition(start, lambda: True, humanTurn)

        #Defines win/loss conditions
        Transition(humanTurn, self.checkWinCondition, humanWin, human)
        Transition(aiPlayer1Turn, self.checkWinCondition, humanLoss, aiPlayer1)
        Transition(aiPlayer2Turn, self.checkWinCondition, humanLoss, aiPlayer2)
        Transition(aiPlayer3Turn, self.checkWinCondition, humanLoss, aiPlayer3)

        # Defines the player loop
        Transition(humanTurn, lambda: True, aiPlayer1Turn)
        Transition(aiPlayer1Turn, lambda: True, aiPlayer2Turn)
        Transition(aiPlayer2Turn, lambda: True, aiPlayer3Turn)
        Transition(aiPlayer3Turn, lambda: True, humanTurn)

        playerFSM.addState(start)
        playerFSM.addState(humanTurn)
        playerFSM.addState(aiPlayer1Turn)
        playerFSM.addState(aiPlayer2Turn)
        playerFSM.addState(aiPlayer3Turn)
        playerFSM.addState(humanWin)
        playerFSM.addState(humanLoss)

        playerFSM.run()

def __main__():
    
#    try:
    game = CrazyEightsFSM()
    # except:
        # print("\n\nGame Ended unexpectedly.\n")
        # exit()

if __name__ == '__main__':
    __main__()


