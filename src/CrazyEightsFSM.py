from model.FiniteStateMachine import *
from model.cards import *
import time

class CrazyEightsFSM():

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def true(self, state) : return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup CrazyEights", self.setup)
        play = Play("Playing CrazyEights", self.run)
        goal = Goal("Ended CrazyEights")

        startToPlay = Transition(start, self.true, play)
        playToGoal = Transition(play, self.true, goal)

        start.addTransition(startToPlay)
        play.addTransition(playToGoal)

        self.fsm.addState(start)
        self.fsm.addState(play)
        self.fsm.addState(goal)

        self.fsm.run()

    def setup(self):
        self.state = "running"

        self.players = []
        self.players.append(HumanPlayer())
        for i in range(0, CrazyEightsFSM.NUMBER_AI_PLAYERS):
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

    def showGameBanner(self):
        print("\n"*2)
        print(" -----------------------------------------------")
        print("|                CRAZY EIGHTS                   |")
        print(" -----------------------------------------------")

    def showRoundNumber(self, roundNumber):
        print("\n")
        print("==================== Round %s ====================" % str(roundNumber))
        print("\n")

    def isOver(self):
        return self.state == "gameover"

    def announceWinner(self):
        if player.isA(HumanPlayer):
            winner = "You"
        else:
            winner = "Computer Player " + str(player.index)

    def run(self):
        game = self
        try:
            winner = "nobody "
            roundNumber = 1
            game.showGameBanner()
            while game.state == "running" and roundNumber < self.ROUND_NUMBER_MAX:
                game.showRoundNumber(roundNumber)
                for player in self.players:
                    game.state = self.advance(player)
                    if (game.isOver()):
                        winner = player.name
                        break
                roundNumber += 1
            print(winner, "won the game in %s rounds!" % str(roundNumber-1))
        except KeyboardInterrupt:
            print("\nGame Exited")

    def advance(self, player):
        self.playPile.top().makeVisible()

        if player.isA(HumanPlayer):
            print("Deck: " + str(self.drawPile.top()))
            print("Play Pile: " + str(self.playPile.top()))
            print("Your hand: " + str(player.hand))
        elif player.isA(AIPlayer):
            print("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        
        self.suitChange = player.makeMove(self)
        
        if player.hand.isEmpty():
            return "gameover"
        if self.drawPile.isEmpty():
            self.drawPile.replaceWith(self.playPile)
            self.drawPile.giveOneCard(self.playPile)

        time.sleep(1)
        return "running"

    def canPlay(self, card):
        playPile = self.playPile
        topCard = playPile.top()
        # If the last card played was an 8 and the suit was changed...
        if self.suitChange is not None:
            canBePlayed = (card.suit == self.suitChange) or (card.rank == "8")
        # Normal game condition; no 8 was played
        else: 
            canBePlayed = (card.suit == topCard.suit) or (card.rank == topCard.rank) or (card.rank == "8")
        return canBePlayed

class AIPlayer(Player):
    
    def __init__(self, index):
        self.index = index
        self.hand = None
        self.name = "Computer Player " + str(index)
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.makeInvisible()
        self.hand.receiveCard(card)

    def makeMove(self, game):
        allMoves = getMoves(self, game)
        allMoves[0].card.makeVisible()
        print("\t", allMoves[0])
        return allMoves[0].make()

class HumanPlayer(Player):
    name = "you"

    def __init__(self):
        self.hand = None
        Player.__init__(self, self.hand)

    def receiveCard(self, card):
        self.hand = self.hand or Pile()
        card.makeVisible()
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
        if self.player.isA(HumanPlayer):
            self.card.makeVisible()
        if self.player.isA(AIPlayer) and self.type == "draw":
            self.card.makeInvisible()
        self.toPile.receiveCard(self.card)

        if self.card.rank == "8" and self.type == "play":
            suitChoiceInput = None
            if self.player.isA(HumanPlayer):
                [print(str(i + 1) + ". ", suitCharacters[suits[i]]) for i in range(4)   ]
                suitChoiceInput = input("Choose which suit to switch to: ")
            elif self.player.isA(AIPlayer):
                suitChoiceInput = random.choice(range(1, 5))
            suitChoice = suits[int(suitChoiceInput)-1]
            print("Suit has been changed to ", suitCharacters[suitChoice])

            # I really don't like doing this, but I'm going to because it's a hacky, temporary fix.
            return suitChoice


def getMoves(player, game):
    playable_moves = []
    
    for card in player.hand:
        if game.canPlay(card):
            play_a_card = Move(card, player.hand, game.playPile, player, "play")
            playable_moves.append(play_a_card)

    game.suitChange = None
    draw_a_card = Move(game.drawPile.top(), game.drawPile, player.hand, player, "draw")
    playable_moves.append(draw_a_card)
    return playable_moves

def __main__():
    game = CrazyEightsFSM()
    game.run()

if __name__ == '__main__':
    __main__()
