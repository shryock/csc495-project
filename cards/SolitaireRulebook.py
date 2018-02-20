from cards import *


class SolitaireRulebook(RuleBook):
    def getAllPossibleMoves(self, board):
        needs = self.getNeeds(board)
        plays = self.getPlays(board)

        moves = [(play[0], play[1], need[1]) for play in plays for need in needs if play[0] == need[0] and play[1] != need[1]]

        if not moves:
            future = self.getFuturePlays(board.waste.cards + board.stock.cards)
            futureMoves = [(play[0], play[1], need[1]) for play in future for need in needs if play[0] == need[0]]
            if not futureMoves:
                return []

        readableMoves = [("Move %s from %s to %s" % move, 0) for move in moves]

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
            return self.allSuits(nextRank, stack.name)

    def getSuitPileNeeds(self, pile):
        if not len(pile):
            return [("1%s" % pile.name[0], pile.name)]
        elif pile.top().rank == ranks[-1]:
            return []
        else:
            nextRank = ranks[ranks.index(pile.top().rank) + 1]
            return [(nextRank, pile.name)]

    def allSuits(self, rank, name):
        return [(rank + suit[0], name) for suit in suits]

    def getPlays(self, board):
        cards  = [self.getStackPlays(stack) for stack in board.stacks]
        cards += [self.getWastePlays(board.waste)]
        cards  = [x for i in cards for x in i]
        return cards

    def getStackPlays(self, stack):
        return [(card.rank + card.suit[0], stack.name) for card in stack if card.visible]

    def getWastePlays(self, pile):
        return [(pile.top().rank + pile.top().suit[0], pile.name)] if len(pile) else []

    def getFuturePlays(self, pile):
        return [(card.rank + card.suit[0], "Future") for card in pile]
