from model.game import *

class SolitaireRulebook(Rulebook):
    def win(self, game):
        for pile in game.board.suitPiles:
            if len(pile) < 13:
                return False
        return True

    def getMoves(self, game):
        needs = self.getNeeds(game.board)
        plays = self.getPlays(game.board)

        moves = [Move(play.pile.indexOf(play.card), play.pile, need.pile, 'MOVE')
                    for play in plays for need in needs if need.accepts(play)]

        moves += [Move(len(stack) - 1, stack, None, 'SHOW')
                    for stack in game.board.stacks if len(stack) and not stack.top().visible]

        if len(game.board.deck):
            moves += [Move(-1, None, None, 'DRAW')]
        elif len(game.board.waste):
            moves += [Move(-1, None, None, 'RESHUFFLE')]

        return moves

    def getNeeds(self, board):
        cards  = [self.getStackNeeds(stack) for stack in board.stacks]
        cards += [self.getSuitPileNeeds(pile) for pile in board.suitPiles]
        cards  = [x for i in cards for x in i]
        return cards

    def getStackNeeds(self, stack):
        if not len(stack):
            return self.allSuits('K', stack)
        elif not stack.top().visible or stack.top().rank == '1':
            return []
        else:
            nextRank = ranks[ranks.index(stack.top().rank) - 1]
            return self.allColor(nextRank, stack.top().isRed, stack)

    def getSuitPileNeeds(self, pile):
        if not len(pile):
            return [PlayableCard('1{}'.format(suitCharacters[pile.name]), True, pile)]
        elif pile.top().rank == ranks[-1]:
            return []
        else:
            nextRank = ranks[ranks.index(pile.top().rank) + 1]
            return [PlayableCard(nextRank + suitCharacters[pile.name], True, pile)]

    def allSuits(self, rank, stack):
        return [PlayableCard(rank + suitCharacters[suit], None, stack) for suit in suits]

    def allColor(self, rank, isRed, stack):
        return self.allBlack(rank, stack) if isRed else self.allRed(rank, stack)

    def allRed(self, rank, stack):
        redSuits = ["Hearts", "Diamonds"]
        return [PlayableCard(rank + suitCharacters[suit], None, stack) for suit in redSuits]

    def allBlack(self, rank, stack):
        blackSuits = ["Spades", "Clubs"]
        return [PlayableCard(rank + suitCharacters[suit], None, stack) for suit in blackSuits]

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
                    cards += [PlayableCard(card.face(), True, stack)]
                else:
                    cards += [PlayableCard(card.face(), False, stack)]
        return cards

    def getWastePlays(self, pile):
        return [PlayableCard(pile.top().face(), True, pile)] if len(pile) else []


class PlayableCard(object):
    def __init__(self, card, top, pile):
        self.card = card
        self.top = top
        self.pile = pile

    def __repr__(self):
        return '{{card: {}, top: {}, pile: {}}}'.format(self.card, self.top, self.pile.name)

    def accepts(self, other):
        if not isinstance(other, PlayableCard):
            return False
        elif self.card != other.card:
            return False
        elif self.pile.name == other.pile.name:
            return False
        elif self.top == None or other.top == None:
            return True
        else:
            return self.top == other.top
