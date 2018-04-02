from model.FiniteStateMachine import *
from model.cards import *
from CrazyEights import *
import time

def returnTrue(state):
    return True

class CrazyEightsFSM(CrazyEights):

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def true(self, state) : return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup CrazyEights", onEntry=self.setup)
        play = Play("Playing CrazyEights", onEntry=self.run)
        goal = Goal("Ended CrazyEights")

        startToPlay = Transition(start, self.true, play)
        playToGoal = Transition(play, self.true, goal)

        start.addTransition(startToPlay)
        play.addTransition(playToGoal)

        self.fsm.addState(start)
        self.fsm.addState(play)
        self.fsm.addState(goal)

        self.fsm.run()


    def run(self, unused):
        playerFSM = FiniteStateMachine()

        human = self.players[0]
        aiPlayer1 = self.players[1]
        aiPlayer2 = self.players[2]
        aiPlayer3 = self.players[3]

        start = Start("Start player loop", (None, human), self.showGameBanner, self.printNextRound)
        humanTurn = Play("Human Player", (self, aiPlayer1), human.makeMove, self.printNextRound)
        aiPlayer1Turn = Play("AI Player 1", (self, aiPlayer2), aiPlayer1.makeMove, self.printNextRound)
        aiPlayer2Turn = Play("AI Player 2", (self, aiPlayer3), aiPlayer2.makeMove, self.printNextRound)
        aiPlayer3Turn = Play("AI Player 3", (self, human), aiPlayer3.makeMove, self.printNextRound)
        humanWin = Goal("Win", self.announceWinner)
        humanLoss = Fail("Lose", self.announceWinner)

        # Begin player loop
        startToHuman = Transition(start, returnTrue, humanTurn)

        # Invalid input case
        humanToHuman = Transition(humanTurn, lambda state: not human.madeValidMove, humanTurn)

        # Defines the player loop
        humanToAI1   = Transition(humanTurn, human.madeValidMove, aiPlayer1Turn)
        ai1ToAI2     = Transition(aiPlayer1Turn, returnTrue, aiPlayer2Turn)
        ai2ToAI3     = Transition(aiPlayer2Turn, returnTrue, aiPlayer3Turn)
        ai3ToHuman   = Transition(aiPlayer3Turn, returnTrue, humanTurn)

        #Defines win/loss conditions
        humanToWin   = Transition(humanTurn, self.checkWinCondition, humanWin, human)
        ai1ToLose    = Transition(aiPlayer1Turn, self.checkWinCondition, humanLoss, aiPlayer1)
        ai2ToLose    = Transition(aiPlayer2Turn, self.checkWinCondition, humanLoss, aiPlayer2)
        ai3ToLose    = Transition(aiPlayer3Turn, self.checkWinCondition, humanLoss, aiPlayer3)

        # TODO: add priority so that certain transitions are checked over others
        humanTurn.addTransition(humanToWin)
        aiPlayer1Turn.addTransition(ai1ToLose)
        aiPlayer2Turn.addTransition(ai2ToLose)
        aiPlayer3Turn.addTransition(ai3ToLose)

        start.addTransition(startToHuman)
        humanTurn.addTransition(humanToHuman)
        humanTurn.addTransition(humanToAI1)
        aiPlayer1Turn.addTransition(ai1ToAI2)
        aiPlayer2Turn.addTransition(ai2ToAI3)
        aiPlayer3Turn.addTransition(ai3ToHuman)

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
        game.run()
    except:
        print("\n\nGame Ended unexpectedly.\n")
        exit()

if __name__ == '__main__':
    __main__()


