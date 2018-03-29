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
        state.onEntry()
        while True:
            state = state.step()
            if state.quit():
                break
        return state.onExit()

class State():

    def __init__(self, name, onEntry=None, onExit=None):
        self.name = name
        if onEntry is not None: self.onEntry = onEntry
        if onExit  is not None: self.onExit  = onExit
        self.transitions = []

    def __str__(self):
        return str(self.name)

    def step(self):
        for transition in self.shuffle(self.transitions):
            if transition.guard(self):
                self.onExit()
                transition.end.onEntry()
                return transition.end
        return self

    def onEntry(self):
        print("Arriving at %s" % str(self))

    def onExit(self):
        print("Leaving %s" % str(self))

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
    def __init__(self, start, guard, end):
        self.start = start
        self.guard = guard
        self.end   = end
