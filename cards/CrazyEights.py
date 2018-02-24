import os
from cards import *

class CrazyEights:

    NUMBER_AI_PLAYERS = 3

    def __init__(self):
        self.state = "running"

        self.players = []
        self.players.append(HumanPlayer())
        for i in range(0, CrazyEights.NUMBER_AI_PLAYERS):
            self.players.append(AIPlayer(i))

        deck = Deck()
        deck.shuffle()
        deck.distributeCardsToPlayers(5, self.players)

        self.drawPile = Pile(deck.listOfCards)
        self.playPile = Pile()
        self.drawPile.giveOneCard(self.playPile)

    def run(self):
        winner = None
        roundNumber = 1
        print(" -----------------------------------------------")
        print("|                CRAZY EIGHTS                   |")
        print(" -----------------------------------------------")
        #print("==================== Round %s ====================" % str(roundNumber))
        while self.state == "running":
            print("==================== Round %s ====================" % str(roundNumber))
            for player in self.players:
                self.state = self.advance(player)
                if (self.state == "gameover"):
                    if isinstance(player, HumanPlayer):
                        winner = "You"
                    else:
                        winner = "Computer Player " + str(player.index)
                    break
            roundNumber += 1
        print(winner, "won the game in %s rounds!" % str(roundNumber-1))

    def advance(self, player):
        self.playPile.top().visible = True

        if isinstance(player, HumanPlayer):
            print("Deck: " + str(self.drawPile.top()))
            print("Play Pile: " + str(self.playPile.top()))
            print("Your hand: " + str(player.hand))
        elif isinstance(player, AIPlayer):
            print("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        
        player.makeMove(self)
        
        if len(player.hand) == 0:
            return "gameover"
        if len(self.drawPile) == 0:
            self.drawPile = Pile(self.playPile.getContents())
            self.drawPile.makeAllCardsInvisible()
            random.shuffle(self.drawPile.getContents())
            self.drawPile.giveOneCard(self.playPile)

        return "running"

class AIPlayer(Player):
    def __init__(self, index):
        self.index = index
        self.hand = None
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.visible = False
        self.hand.receiveCard(card)

    def makeMove(self, game):
        allMoves = getMoves(self, game)
        allMoves[0].make()
        print("\t", allMoves[0])

class HumanPlayer(Player):
    def __init__(self):
        self.hand = None
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.visible = True
        self.hand.receiveCard(card)

    def makeMove(self, game):
        allMoves = getMoves(self, game)
        for index, move in enumerate(allMoves):
            print("   %i. %s" % (index+1, str(move)))
        playerMove = input("Choose your next move: ")
        # TODO add in type checking here since it is user input
        allMoves[int(playerMove)-1].make()

class Move:
    def __init__(self, card, fromPile, toPile, player, moveType):
        self.card = card
        self.fromPile = fromPile
        self.toPile = toPile
        self.player = player
        self.type = moveType

    def __repr__(self):
        if (self.type == "play"):
            return "Move " + str(self.card) + " to the play pile."
        elif (self.type == "draw"):
            return "Draw card from the deck."

    def make(self):
        self.fromPile.getContents().remove(self.card)
        if isinstance(self.player, HumanPlayer):
            self.card.visible = True
        elif isinstance(self.player, AIPlayer):
            self.card.visible = False
        self.toPile.receiveCard(self.card)

def getMoves(player, game):
    moves = []
    playPile = game.playPile
    topCard = playPile.top()
    for card in player.hand:
        canBePlayed = card.suit == topCard.suit or card.rank == topCard.rank or card.rank == 8
        if canBePlayed:
            moves.append(Move(card, player.hand, game.playPile, player, "play"))

    moves.append(Move(game.drawPile.top(), game.drawPile, player.hand, player, "draw"))

    return moves

game = CrazyEights()
game.run()