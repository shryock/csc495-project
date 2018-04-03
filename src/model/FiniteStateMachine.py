import random

class FiniteStateMachine():

    def __init__(self):
        self.states = []

    def addState(self, state):
        if isinstance(state, Start):
            self.start = state
        self.states.append(state)

    def run(self):
        state = self.start
        entryParam, exitParam = state.payload or (None, None)

        state.onEntry(entryParam)
        while True:
            state = state.step()
            if state.quit():
                break
        return state.onExit(exitParam)

class State():

    def __init__(self, name, onEntry=None, onExit=None, payload=None):
        self.name = name
        if onEntry is not None: self.onEntry = onEntry
        if onExit  is not None: self.onExit  = onExit
        self.payload = payload
        self.transitions = []

    def __str__(self):
        return str(self.name)

    def step(self):
        for transition in self.transitions:
            if transition.guard(transition.payload):
                exitParam = None
                if self.payload is not None: exitParam = self.payload[1]
                self.onExit(exitParam)
                entryParam = None
                if transition.end.payload is not None: entryParam = transition.end.payload[0]
                transition.end.onEntry(entryParam)
                return transition.end
        return self

    def onEntry(self, payload=None): pass

    def onExit(self, payload=None): pass

    def addTransition(self, transition):
        self.transitions.append(transition)

    def quit(self):
        return False

    def shuffle(self, lst):
        random.shuffle(lst)
        return lst

class Start(State): pass

class Play(State): pass

class Goal(State):
    def quit(self):
        return True

class Fail(State):
    def quit(self):
        return True

class Transition():
    def __init__(self, start, guard, end, payload=None):
        self.start = start
        self.guard = guard
        self.end   = end
        self.payload = payload

    def __str__(self):
        return str(self.start) + ":" + str(self.guard.__name__) + ":" + str(self.end)
