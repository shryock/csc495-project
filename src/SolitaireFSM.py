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
        start = Start("Start")
        #                 name of state,   onentry    onexit    parameters as tuple
        humanTurn = Play("Human Player", (self, human), self.play)
        errorState = Play("Invalid Move", (self, human) )
        humanWin = Goal("Win", self.announceWinner)
        
        startToHuman = Transition(start, self.true, humanTurn)
        
        # Defines the player loop
        humanToSelf   = Transition(humanTurn, self.checkValid, humanTurn)
        humanError = Transition(humanTurn, lambda x: not self.checkValid, errorState)
        errorToHuman = Transition(errorState,  self.true,  humanTurn)

        #Defines win/loss conditions
        humanToWin   = Transition(humanTurn, self.checkWinCondition, humanWin, human)
        
        # TODO: add priority so that certain transitions are checked over others
        start.addTransition(startToHuman)
        humanTurn.addTransition(humanToWin) 
        humanTurn.addTransition(humanToSelf)
        humanTurn.addTransition(humanError)
        errorState.addTransition(errorToHuman)

        playerFSM.addState(humanTurn)
        playerFSM.addState(humanWin)
        playerFSM.addState(start)
        playerFSM.addState(errorToHuman)
        playerFSM.run()


if __name__ == '__main__':
    SolitaireFSM()
