from model.cards import *
from Solitaire import *
from model.FiniteStateMachine import *

def returnTrue(state):
    return True

class SolitaireFSM(Solitaire):
    def true(self, unused):
        return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup Solitaire", onEntry=self.setup)
        play = Play("Playing Solitaire", onEntry=self.run)
        goal = Goal("Ended Solitaire")
        
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
        start = Start("Start player loop", (None, human), self.showGameBanner, self.true)
        humanTurn = Play("Human Player", (self, human), self.play, self.true)
        humanWin = Goal("Win", self.announceWinner)
        
        # Begin player loop
        startToHuman = Transition(start, returnTrue, humanTurn)

        # Invalid input case
        humanToHuman = Transition(humanTurn, lambda move: not self.checkValid, humanTurn)

        # Defines the player loop
        humanToSelf   = Transition(humanTurn, self.checkValid, humanTurn)

        #Defines win/loss conditions
        humanToWin   = Transition(humanTurn, self.checkWinCondition, humanWin, human)

        # TODO: add priority so that certain transitions are checked over others
        humanTurn.addTransition(humanToWin)

        start.addTransition(startToHuman)
        humanTurn.addTransition(humanToHuman)

        playerFSM.addState(start)
        playerFSM.addState(humanTurn)
        playerFSM.addState(humanWin)

        playerFSM.run()


if __name__ == '__main__':
    SolitaireFSM()
