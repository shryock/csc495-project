from model.util import *
from model.game import *

class State():
    """Representation of a state managed by a Machine

    Attributes:
        name (str): Name of state
        trans (list): List of transitions stored as Structs with an end state and a guard
    """

    def __init__(self, name):
        self.name = name
        self.trans = []

    def __repr__(self):
        return '{} => {}'.format(self.name, [tran.end.name for tran in self.trans])

    def addTransition(self, end, guard):
        """Add transition from self to end state with a conditional guard

        Args:
            end (State): End state of transition
            guard (function): Function that accepts a Game parameter and returns a boolean
        Returns:
            State instance, used for chaining method calls
        """
        self.trans.append(Struct(end=end, guard=guard))
        return self

    def step(self, game):
        """Makes transition from current state instance to end state, if possible

        Args:
            game (Game): Game instance to be passed around as payload, or game environment
        Returns:
            End state from transition, or current state if no transition possible
        """
        for tran in self.trans:
            if tran.guard(game):
                self.onExit(game)
                tran.end.onEntry(game)
                return tran.end
        return self

    def onEntry(self, game):
        """Called when transitioning from another state to current state

        Args:
            game (Game): Game instance in machine
        """
        pass

    def onExit(self, game):
        """Called when transitioning from current state to another state

        Args:
            game (Game): Game instance in machine
        """
        pass

    def quit(self):
        """Returns true if state instance is a final state"""
        return False


class EndState(State):
    """Representation of final state of machine"""

    def quit(self):
        return True


class StartState(State):
    """Representation of start state of game machine"""

    def onEntry(self, game):
        """Prints banner with name of game"""
        game.printBanner()


class PlayerState(State):
    """Representation of the decision making state for a player

    Attributes:
        machine (PlayerMachine): Machine used for managing player decisions
    """

    def __init__(self, name, machine):
        self.name = name
        self.trans = []
        self.machine = machine

    def onEntry(self, game):
        """Sets current player to the player's index and runs player machine"""
        game.currentPlayer = int(self.name[1]) - 1
        self.machine.run(game)


class PlayState(State):
    """Representation of game loop in game machine"""

    def createPlayMachine(self, players, rulebook):
        """Creates a machine that iterates through available players until a win or quit condition is met

        Args:
            players (list): List of players in a game
            rulebook (Rulebook): Rulebook associated with current game; must have win and quit guards
        Returns:
            Machine of player states
        """
        self.machine = Machine()

        for player in players:
            player.machine = PlayerMachine(rulebook)

        states = [self.machine.addState(
                    PlayerState('P{}'.format(i + 1), players[i].machine))
                    for i in range(len(players))]
        win = self.machine.addState(EndState('WIN'))
        quit = self.machine.addState(QuitState('QUIT'))

        # Add win and quit transitions to each player state, as well as a transition to the next player
        for i in range(len(states)):
            states[i].addTransition(win, rulebook.win)
            states[i].addTransition(quit, rulebook.quit)
            states[i].addTransition(states[(i + 1) % len(states)], rulebook.true)

        return self.machine

    def onEntry(self, game):
        """Runs generated machine of player states based off game"""
        self.createPlayMachine(game.players, game.rulebook).run(game)


class MoveState(State):
    """Representation of move selection for players"""

    def onEntry(self, game):
        """Prints round, board, hand, and moves (if applicable) before allowing user to select a move"""
        game.printRound()
        game.printBoard()
        game.printHand()
        game.printMoves()
        game.chooseMove()


class ValidMoveState(EndState):
    """Representation of state reached when player move selection is valid"""

    def onEntry(self, game):
        """Executes selected move and sets appropriate flags and counters"""
        game.invalid = False
        game.moveCount += 1
        game.executeMove()


class InvalidMoveState(State):
    """Representation of state reached when player move selection is invalid"""

    def onEntry(self, game):
        """Sets invalid move flag and prints message indicating invalid state"""
        game.invalid = True
        game.printInvalidMoveMessage()


class GoalState(EndState):
    """Representation of end of game state"""

    def onEntry(self, game):
        """Prints goal message at end of game"""
        game.goal()


class QuitState(EndState):
    """Representation of state reached when player selects to quit game"""

    def onEntry(self, game):
        """Prints quit message before exiting"""
        game.printQuit()


class Machine():
    """Finite state machine used for managing and iterating through states and transitions

    Attributes:
        states (dict): Dictionary of states in machine, stored using name of state
        start (State): Start state of machine
    """
    def __init__(self):
        self.states = {}
        self.start = None

    def __repr__(self):
        return 'start: {}\n\n'.format(self.start.name) + '\n'.join([repr(self.states[key]) for key in self.states.keys()])

    def addState(self, state):
        """Adds state to machine, overwriting that of the same name, if it exists

        Args:
            state (State): State to be added to machine
        Returns:
            The given state
        """
        # Sets start state as given state if no start state exists
        self.start = self.start or state
        self.states[state.name] = state
        return self.states[state.name]

    def run(self, game):
        """Steps through states in machine until a final state is reached"""
        state = self.start

        state.onEntry(game)
        while not state.quit():
            state = state.step(game)
        state.onExit(game)


class GameMachine(Machine):
    """Finite state machine representing the highest abstraction of a game, consisting of only a start state, play loop, and end goal

    Attributes:
        game (Game): Game model to be manipulated during machine run
    """

    def __init__(self, game):
        self.game = game
        self.game.setup()
        self.createMachine()

    def createMachine(self):
        """Creates generic game machine consisting of start, play, and goal states with single transitions"""
        self.states = {
            'START': StartState('START'),
            'PLAY':  PlayState('PLAY'),
            'GOAL':  GoalState('GOAL')
        }
        self.start = self.states['START']

        # Start state always transitions to play state on exit
        self.states['START'].addTransition(self.states['PLAY'], self.game.rulebook.true)
        # Play state always transitions to goal state on exit
        self.states['PLAY'].addTransition(self.states['GOAL'], self.game.rulebook.true)

    def startGame(self):
        """Starts game machine"""
        self.run(self.game)


class PlayerMachine(Machine):
    """Finite state machine representing the decision making steps of a player, including move selection and evaluation of the selected move

    Attributes:
        rulebook (Rulebook): Game rulebook used for evaluating validity of player move
    """

    def __init__(self, rulebook):
        self.rulebook = rulebook
        self.createMachine()

    def createMachine(self):
        """Creates generic player machine consisting of move selection, invalid move, and valid move states"""
        self.states = {
            'MOVE': MoveState('MOVE'),
            'INVALID': InvalidMoveState('INVALID'),
            'VALID': ValidMoveState('VALID')
        }
        self.start = self.states['MOVE']

        # Transition from move selection state to valid move state based on rulebook evaluation
        self.states['MOVE'].addTransition(self.states['VALID'], self.rulebook.validMove)
        # Transition from move selection state to invalid move state if rulebook does not accept move
        self.states['MOVE'].addTransition(self.states['INVALID'], self.rulebook.true)
        # Always transition from invalid move state to move selection state
        self.states['INVALID'].addTransition(self.states['MOVE'], self.rulebook.true)
