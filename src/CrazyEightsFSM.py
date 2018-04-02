from model.FiniteStateMachine import *
from model.cards import *
import time

def returnTrue(state):
    return True

class CrazyEightsFSM():

    NUMBER_AI_PLAYERS = 3
    ROUND_NUMBER_MAX = 400

    def true(self, state) : return True

    def __init__(self):
        self.fsm = FiniteStateMachine()
        start = Start("Setup CrazyEights", onEntry=self.setup)
        play = Play("Playing CrazyEights", onEntry=self.run)
        goal = Goal("Ended CrazyEights")

        startToPlay = Transition(start, self.true, play)
        playToGoal = Transition(play, self.true, goal)

        start.addTransition(startToPlay)
        play.addTransition(playToGoal)

        self.fsm.addState(start)
        self.fsm.addState(play)
        self.fsm.addState(goal)

        self.fsm.run()

    def setup(self, unused):
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

    def showGameBanner(self, unused):
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

    def checkWinCondition(self, player):
        return len(player.hand) == 0

    def run(self, unused):
        playerFSM = FiniteStateMachine()

        human = self.players[0]
        aiPlayer1 = self.players[1]
        aiPlayer2 = self.players[2]
        aiPlayer3 = self.players[3]

        start = Start("Start player loop", (None, human), self.showGameBanner, self.printNextRound)
        humanTurn = Play("Human Player", (self, aiPlayer1), human.makeMove, self.printNextRound)
        aiPlayer1Turn = Play("AI Player 1", (self, aiPlayer2), aiPlayer1.makeMove, self.printNextRound)
        aiPlayer2Turn = Play("AI Player 2", (self, aiPlayer3), aiPlayer2.makeMove, self.printNextRound)
        aiPlayer3Turn = Play("AI Player 3", (self, human), aiPlayer3.makeMove, self.printNextRound)
        humanWin = Goal("Win", self.announceWinner)
        humanLoss = Fail("Lose", self.announceWinner)

        # Begin player loop
        startToHuman = Transition(start, returnTrue, humanTurn)

        # Invalid input case
        humanToHuman = Transition(humanTurn, lambda state: not human.madeValidMove, humanTurn)

        # Defines the player loop
        humanToAI1   = Transition(humanTurn, human.madeValidMove, aiPlayer1Turn)
        ai1ToAI2     = Transition(aiPlayer1Turn, returnTrue, aiPlayer2Turn)
        ai2ToAI3     = Transition(aiPlayer2Turn, returnTrue, aiPlayer3Turn)
        ai3ToHuman   = Transition(aiPlayer3Turn, returnTrue, humanTurn)

        #Defines win/loss conditions
        humanToWin   = Transition(humanTurn, self.checkWinCondition, humanWin, human)
        ai1ToLose    = Transition(aiPlayer1Turn, self.checkWinCondition, humanLoss, aiPlayer1)
        ai2ToLose    = Transition(aiPlayer2Turn, self.checkWinCondition, humanLoss, aiPlayer2)
        ai3ToLose    = Transition(aiPlayer3Turn, self.checkWinCondition, humanLoss, aiPlayer3)

        # TODO: add priority so that certain transitions are checked over others
        humanTurn.addTransition(humanToWin)
        aiPlayer1Turn.addTransition(ai1ToLose)
        aiPlayer2Turn.addTransition(ai2ToLose)
        aiPlayer3Turn.addTransition(ai3ToLose)

        start.addTransition(startToHuman)
        humanTurn.addTransition(humanToHuman)
        humanTurn.addTransition(humanToAI1)
        aiPlayer1Turn.addTransition(ai1ToAI2)
        aiPlayer2Turn.addTransition(ai2ToAI3)
        aiPlayer3Turn.addTransition(ai3ToHuman)

        playerFSM.addState(start)
        playerFSM.addState(humanTurn)
        playerFSM.addState(aiPlayer1Turn)
        playerFSM.addState(aiPlayer2Turn)
        playerFSM.addState(aiPlayer3Turn)
        playerFSM.addState(humanWin)
        playerFSM.addState(humanLoss)

        playerFSM.run()

    def printNextRound(self, player):
        self.playPile.top().makeVisible()

        if player.isA(HumanPlayer):
            print("Deck: " + str(self.drawPile.top()))
            print("Play Pile: " + str(self.playPile.top()))
            print("Your hand: " + str(player.hand))
        elif player.isA(AIPlayer):
            print("Computer Player %s's Hand: %s" % (player.index, str(player.hand)))
        time.sleep(1)


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
        index = int(playerMove)
        if index > len(allMoves) or index <= 0:
            self.lastMoveWasValid = False
            return None
        self.lastMoveWasValid = True
        return allMoves[int(playerMove)-1].make()

    def madeValidMove(self, state):
        return self.lastMoveWasValid

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
