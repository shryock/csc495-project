from model.cards import *
from games.Solitaire import *
from model.FiniteStateMachine import *

def returnTrue():
    return True

class SolitaireFSM(Solitaire):
    def true(self):
        return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup Solitaire", self.setup)
        play = Play("Playing Solitaire", self.run)
        goal = Goal("Ended Solitaire")
        
        Transition(start, self.true, play)
        Transition(play, self.true, goal)
        
        self.fsm.addState(start)
        self.fsm.addState(play)
        self.fsm.addState(goal)

        self.fsm.run()
        
    def run(self):
        playerFSM = FiniteStateMachine()
        human = self.players[0]
        start = Start("Start")
        #                 name of state,   onentry    onexit    parameters as tuple
        humanTurn = Play("Human Player", self.play )
        errorState = Play("Invalid Move" )
        humanWin = Goal("Win", self.announceWinner)
        
        Transition(start, self.true, humanTurn)
        
        # Defines the player loop
        Transition(humanTurn, self.checkValid, humanTurn)
        Transition(humanTurn, lambda: not self.checkValid, errorState)
        Transition(errorState,  self.true,  humanTurn)

        #Defines win/loss conditions
        Transition(humanTurn, self.checkWinCondition, humanWin)
        
        playerFSM.addState(humanTurn)
        playerFSM.addState(humanWin)
        playerFSM.addState(start)
        playerFSM.addState(errorState)
        playerFSM.run()

def __main__():
    try:
        game = SolitaireFSM()
    except:
        print("\n\nGame Ended unexpectedly.\n")
        exit()

if __name__ == '__main__':
    __main__()
