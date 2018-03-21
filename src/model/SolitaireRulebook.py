from .cards import *

class SolitaireRulebook(RuleBook):
    def getAllPossibleMoves(self, board):
        needs = self.getNeeds(board)
        plays = self.getPlays(board)

        moves = [Move(play.id, play.pile, need.pile) for play in plays for need in needs if need.accepts(play)]

        if not moves:
            future = self.getFuturePlays(board.waste.cards + board.stock.cards)
            futureMoves = [Move(play.id, play.id, need.id) for play in future for need in needs if need.accepts(play)]
            if not futureMoves:
                return []

        readableMoves = [(repr(move), 0) for move in moves]

        readableMoves += [("Show %s" % stack.name, 1) for stack in board.stacks if len(stack) and not stack.top().visible]

        if len(board.stock):
            readableMoves += [("Draw from Stock", 2)]
        else:
            readableMoves += [("Reshuffle Stock", 3)]

        readableMoves += [("Quit", 4)]

        return readableMoves

    def getNeeds(self, board):
        cards  = [self.getStackNeeds(stack) for stack in board.stacks]
        cards += [self.getSuitPileNeeds(pile) for pile in board.suitPiles]
        cards  = [x for i in cards for x in i]
        return cards

    def getStackNeeds(self, stack):
        if not len(stack):
            return self.allSuits(ranks[-1], stack.name)
        elif not stack.top().visible or stack.top().rank == "1":
            return []
        else:
            nextRank = ranks[ranks.index(stack.top().rank) - 1]
            return self.allColor(nextRank, stack.top().isRed, stack.name)

    def getSuitPileNeeds(self, pile):
        if not len(pile):
            return [PlayableCard("1%s" % pile.name[0], True, pile.name)]
        elif pile.top().rank == ranks[-1]:
            return []
        else:
            nextRank = ranks[ranks.index(pile.top().rank) + 1]
            return [PlayableCard(nextRank + pile.name[0], True, pile.name)]

    def allSuits(self, rank, name):
        return [PlayableCard(rank + suit[0], None, name) for suit in suits]

    def allColor(self, rank, isRed, name):
        return self.allBlack(rank, name) if isRed else self.allRed(rank, name)

    def allRed(self, rank, name):
        redSuits = ["Hearts", "Diamonds"]
        return [PlayableCard(rank + suit[0], None, name) for suit in redSuits]

    def allBlack(self, rank, name):
        blackSuits = ["Spades", "Clubs"]
        return [PlayableCard(rank + suit[0], None, name) for suit in blackSuits]

    def getPlays(self, board):
        cards  = [self.getStackPlays(stack) for stack in board.stacks]
        cards += [self.getWastePlays(board.waste)]
        cards  = [x for i in cards for x in i]
        return cards

    def getStackPlays(self, stack):
        cards = []
        for card in stack:
            if card.visible:
                if card == stack.top():
                    cards += [PlayableCard(card.rank + card.suit[0], True, stack.name)]
                else:
                    cards += [PlayableCard(card.rank + card.suit[0], False, stack.name)]
        return cards

    def getWastePlays(self, pile):
        return [PlayableCard(pile.top().rank + pile.top().suit[0], True, pile.name)] if len(pile) else []

    def getFuturePlays(self, pile):
        return [PlayableCard(card.rank + card.suit[0], True, "Future") for card in pile]


class PlayableCard(object):
    def __init__(self, id, top, pile):
        self.id = id
        self.top = top
        self.pile = pile

    def __repr__(self):
        return "{id: %s, top: %s, pile: %s}" % (self.id, self.top, self.pile)

    def accepts(self, other):
        if not isinstance(other, PlayableCard):
            return False
        elif self.id != other.id:
            return False
        elif self.pile == other.pile:
            return False
        elif self.top == None or other.top == None:
            return True
        else:
            return self.top == other.top


class Move(object):
    def __init__(self, card, start, end):
        self.card = card
        self.start = start
        self.end = end

    def __repr__(self):
        return "Move %s from %s to %s" % (self.card, self.start, self.end)
