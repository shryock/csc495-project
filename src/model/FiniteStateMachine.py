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

        if entryParam is not None:
            state.onEntry(entryParam)
        else:
            state.onEntry()
        while True:
            state = state.step()
            if state.quit():
                break
        if exitParam is not None:
            return state.onExit(exitParam)
        else:
            return state.onExit()

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
        # TODO: this is too much duplicate code; doing it this way to handle default payload
        for transition in self.transitions:
            if transition.payload is not None:
                if transition.guard(transition.payload):
                    if self.payload is not None:
                        self.onExit(self.payload[1])
                    else:
                        self.onExit()
                    entryParam = None
                    if transition.end.payload is not None and transition.end.payload[0] is not None:
                        transition.end.onEntry(transition.end.payload[0])
                    else:
                        transition.end.onEntry()
                    return transition.end
            else:
                if transition.guard():
                    if self.payload is not None:
                        self.onExit(self.payload[1])
                    else:
                        self.onExit()
                    entryParam = None
                    if transition.end.payload is not None and transition.end.payload[0] is not None:
                        transition.end.onEntry(transition.end.payload[0])
                    else:
                        transition.end.onEntry()
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
