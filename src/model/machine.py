from util import Struct
from game import *

class State():
    def __init__(self, name):
        self.name = name
        self.trans = []

    def __repr__(self):
        return '{} => {}'.format(self.name, [tran.end.name for tran in self.trans])

    def addTransition(self, end, guard):
        self.trans.append(Struct(end=end, guard=guard))
        return self

    def step(self, game):
        for tran in self.trans:
            if tran.guard(game):
                self.onExit(game)
                tran.end.onEntry(game)
                return tran.end
        return self

    #TODO: Make generic onEntry and onExit
    def onEntry(self, game): pass

    def onExit(self, game): pass

    def quit(self):
        return False


class EndState(State):
    def quit(self):
        return True


class StartState(State):
    def onEntry(self, game):
        game.setup()

    def onExit(self, game):
        game.printBanner()


class PlayerState(State):
    def __init__(self, name, machine):
        self.name = name
        self.machine = machine
        self.trans = []

    def onEntry(self, game):
        game.currentPlayer = int(self.name[1] - 1)
        self.machine.run(game)


class PlayState(State):
    def createPlayMachine(self, players, rulebook):
        self.machine = Machine()
        states = [self.machine.addState(
                    PlayerState('P{}'.format(i + 1), players[i].machine))
                    for i in range(len(players))]
        win = self.machine.addState(EndState('WIN'))
        quit = self.machine.addState(QuitState('QUIT'))

        for i in range(len(states)):
            states[i].addTransition(win, rulebook.win)
            states[i].addTransition(quit, rulebook.quit)
            states[i].addTransition(states[(i + 1) % len(states)], rulebook.true)

    def onEntry(self, game):
        self.createPlayMachine(game.players, game.rulebook).run(game)


class MoveState(State):
    def onEntry(self, game):
        if game.playerIsHuman():
            game.printBoard()
            game.printMoves()
        game.chooseMove()


class ValidMoveState(EndState):
    def onEntry(self, game):
        game.executeMove()


class InvalidMoveState(State):
    def onEntry(self, game):
        game.printInvalidMoveMessage()


class GoalState(EndState):
    def onEntry(self, game):
        game.goal()


class QuitState(EndState):
    def onEntry(self, game):
        game.quit = True


class Machine():
    def __init__(self):
        self.states = {}
        self.start = None

    def __repr__(self):
        return 'start: {}\n\n'.format(self.start.name) + '\n'.join([repr(self.states[key]) for key in self.states.keys()])

    def addState(self, state):
        self.start = self.start or state
        self.states[state.name] = state
        return self.states[state.name]

    def run(self, game):
        state = self.start

        state.onEntry(game)
        while not state.quit():
            state = state.step(game)
        state.onExit(game)


class GameMachine(Machine):
    def __init__(self, game):
        self.game = game
        self.createMachine()

    def createMachine(self):
        self.states = {
            'START': StartState('START'),
            'PLAY':  PlayState('PLAY'),
            'GOAL':  GoalState('GOAL')
        }
        self.start = self.states['START']

        self.states['START'].addTransition(self.states['PLAY'], game.rulebook.true)
        self.states['PLAY'].addTransition(self.states['GOAL'], game.rulebook.true)

    def start(self):
        self.run(self.game)


class PlayerMachine(Machine):
    def __init__(self, rulebook):
        self.rulebook = rulebook
        self.createMachine()

    def createMachine(self):
        self.states = {
            'MOVE': MoveState('MOVE'),
            'INVALID': InvalidMoveState('INVALID'),
            'VALID': ValidMoveState('VALID')
        }
        self.start = self.states['MOVE']

        self.states['MOVE'].addTransition(self.states['VALID'], self.rulebook.validMove)
        self.states['MOVE'].addTransition(self.states['INVALID'], self.rulebook.true)
        self.states['INVALID'].addTransition(self.states['MOVE'], self.rulebook.true)
