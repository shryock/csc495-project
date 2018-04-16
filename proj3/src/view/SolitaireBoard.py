from model.cards import *

class SolitaireBoard(Board):
    def __repr__(self):
        return self.printTopRow() + '\n\n'+ self.printStacks()

    def printTopRow(self):
        return ' '.join([self.printSuitPiles(), '    ', self.printWaste(), self.printDeck()])

    def printSuitPiles(self):
        return ' '.join(['%4s' % repr(pile.top()) if len(pile) else "%4s" % "[ ]" for pile in self.suitPiles])

    def printWaste(self):
        return '%4s' % repr(self.waste.top()) if len(self.waste) else "%4s" % "[ ]"

    def printDeck(self):
        return '%4s' % repr(self.deck.top()) if len(self.deck) else "%4s" % "[ ]"

    def printStacks(self):
        maxCount = max([len(stack) for stack in self.stacks])
        return "\n".join([self.printStackRow(i) for i in range(maxCount)])

    def printStackRow(self, index):
        return " ".join(['{:>4}'.format(repr(stack[index])) if len(stack) > index else "    " for stack in self.stacks])

    def setup(self):
        self.stacks = self.piles[:7]
        self.suitPiles = self.piles[7:11]
        self.waste = self.piles[11]
        self.deck = self.piles[12]

        for i in range(len(self.stacks)):
            self.stacks[i].name = 'Stack {}'.format(i + 1)
            self.stacks[i].top().visible = True
        for i in range(len(self.suitPiles)):
            self.suitPiles[i].name = suits[i]
        self.waste.name = "Waste"
        self.deck.name = "Deck"
