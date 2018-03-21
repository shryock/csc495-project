import os
import time
from model.cards import *

class CrazyEights:

    NUMBER_AI_PLAYERS = 3

    def __init__(self):
        self.state = "running"

        self.players = []
        self.players.append(HumanPlayer())
        for i in range(0, CrazyEights.NUMBER_AI_PLAYERS):
            self.players.append(AIPlayer(i))

        self.suitChange = None

        deck = Deck()
        deck.shuffle()
        deck.distributeCardsToPlayers(5, self.players)

        self.drawPile = Pile(deck.listOfCards)
        while (self.drawPile.top().rank == "8"):
            print("There was an 8 at the top of the pile, so it was reshuffled.")
            random.shuffle(self.drawPile.getContents())

        self.playPile = Pile()
        self.drawPile.giveOneCard(self.playPile)

    def run(self):
        try:
            winner = None
            roundNumber = 1
            print("\n"*2)
            print(" -----------------------------------------------")
            print("|                CRAZY EIGHTS                   |")
            print(" -----------------------------------------------")
            while self.state == "running":
                print("\n")
                print("==================== Round %s ====================" % str(roundNumber))
                print("\n")
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
        except KeyboardInterrupt:
            print("\nGame Exited")

    def advance(self, player):
        self.playPile.top().visible = True

        if isinstance(player, HumanPlayer):
            print("Deck: " + str(self.drawPile.top()))
            print("Play Pile: " + str(self.playPile.top()))
            print("Your hand: " + str(player.hand))
        elif isinstance(player, AIPlayer):
            print("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        
        self.suitChange = player.makeMove(self)
        
        if len(player.hand) == 0:
            return "gameover"
        if len(self.drawPile) == 0:
            self.drawPile = Pile(self.playPile.getContents())
            self.drawPile.makeAllCardsInvisible()
            random.shuffle(self.drawPile.getContents())
            self.drawPile.giveOneCard(self.playPile)

        time.sleep(1)

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
        allMoves[0].card.visible = True
        print("\t", allMoves[0])
        return allMoves[0].make()

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
        while True:
            try:
                index = int(playerMove)
                if index > len(allMoves) or index <= 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                playerMove = input("Choose your next move: ")
        return allMoves[int(playerMove)-1].make()

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
        if (isinstance(self.player, HumanPlayer)):
            self.card.visible = True
        if isinstance(self.player, AIPlayer) and self.type == "draw":
            self.card.visible = False
        self.toPile.receiveCard(self.card)

        if self.card.rank == "8" and self.type == "play":
            suitChoiceInput = None
            if isinstance(self.player, HumanPlayer):
                print("1. ", suitCharacters["Hearts"])
                print("2. ", suitCharacters["Spades"])
                print("3. ", suitCharacters["Clubs"])
                print("4. ", suitCharacters["Diamonds"])
                suitChoiceInput = input("Choose which suit to switch to: ")
            elif isinstance(self.player, AIPlayer):
                suitChoiceInput = random.choice(range(1, 5))
            suitChoice = suits[int(suitChoiceInput)-1]
            print("Suit has been changed to ", suitCharacters[suitChoice])

            # I really don't like doing this, but I'm going to because it's a hacky, temporary fix.
            return suitChoice

def getMoves(player, game):
    moves = []
    playPile = game.playPile
    topCard = playPile.top()
    for card in player.hand:
        # If the last card played was an 8 and the suit was changed...
        if game.suitChange is not None:
            canBePlayed = (card.suit == game.suitChange) or (card.rank == "8")
        # Normal game condition; no 8 was played
        else: 
            canBePlayed = (card.suit == topCard.suit) or (card.rank == topCard.rank) or (card.rank == "8")
        if canBePlayed:
            moves.append(Move(card, player.hand, game.playPile, player, "play"))

    game.suitChange = None
    moves.append(Move(game.drawPile.top(), game.drawPile, player.hand, player, "draw"))

    return moves

game = CrazyEights()
game.run()
