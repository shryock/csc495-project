import random
import model.Logger as Logger

suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suitCharacters = {"Hearts": "\u2665", "Spades": "\u2660", "Clubs": "\u2663", "Diamonds": "\u2666"}

class Game():
    """Game model using a board, rulebook, list of players, and dictionary of moves to manage state

    Attributes:
        name (str): Name of game
        board (Board): Game board used for managing and displaying piles
        rulebook (Rulebook): Rules of game used as guards in machine
        players (list): List of players in game
        moves (dict): Dictionary of moves with move names as keys and corresponding functions as values
        showRounds (boolean): Boolean used for printing, or not printing, round numbers

    Note:
        The dictionary of moves should always contain a QUIT key with value set to the quitGame method,
        unless a game does not allow the player such an option
    """
    def __init__(self):
        self.name = 'Game'
        self.board = None
        self.rulebook = None
        self.players = []
        self.moves = {}
        self.showRounds = False

        # The following attributes should be untouched and are used for management by a game machine
        self.moveCount = 0
        self.invalid = False
        self.currentPlayer = -1
        self.playerMoves = []
        self.selectedMove = -1
        self.quit = False

    def setup(self):
        """Setup relevant game attributes and initial values

        Note:
            The setup method should be used instead of overriding constructor as to not remove any
            important attributes needed for running the game machine
        """
        raise NotImplementedError

    def goal(self):
        """Prints generic win message and closes logger for program exit"""
        if not self.quit:
            # Winning message only printed if a player did not quit
            Logger.log('Player {} has won the game'.format(self.currentPlayer + 1))
        self.closeLogger()

    def quitGame(self, move):
        """Sets quit flag to true

        Args:
            move (Move): Representation of player-selected move
        """
        self.quit = True

    def chooseMove(self):
        """Asks player to select a move from the available move list"""
        self.selectedMove = self.players[self.currentPlayer].chooseMove()

    def executeMove(self):
        """Executes player-selected move when valid"""
        move = self.playerMoves[self.selectedMove]
        if not self.playerIsHuman():
            # Print move selected by AI so human players can see selection
            Logger.log(' ' * 4, repr(move), '\n')
        # Execute move using type defined in moves dictionary
        self.moves[move.moveType](move)

    def playerIsHuman(self):
        """Returns true if player is human, false if AI"""
        return self.players[self.currentPlayer].isA(HumanPlayer)

    def printBanner(self):
        """Prints banner containing name of game"""
        Logger.log('-' * 50)
        Logger.log('|', self.name.center(48), '|')
        Logger.log('-' * 50, '\n')

    def printRound(self):
        """Prints round number if game allows rounds to be displayed"""
        # Round numbers are only printed after reaching the first player once per iteration
        if self.showRounds and self.currentPlayer == 0 and not self.invalid:
            roundNum = int(self.moveCount / len(self.players) + 1)
            Logger.log(' Round {} '.format(roundNum).center(50, '='), '\n')

    def printHand(self):
        """Prints player hand if any cards present"""
        if len(self.players[self.currentPlayer].hand):
            Logger.log("Player {}'s Hand: {}\n".format(
                self.currentPlayer + 1,
                repr(self.players[self.currentPlayer].hand)))

    def printBoard(self):
        """Prints game board for human players to analyze

        Note:
            Board layout and printing should be handled through the repr() method of a game's
            associated Board class
        """
        if self.playerIsHuman():
            Logger.log(repr(self.board), '\n')

    def printMoves(self):
        """Retrieves possible moves for current player and prints list only for human players"""
        self.playerMoves  = self.rulebook.getMoves(self)
        # Always add quit option to move list; can be overrided if game does not allow quits
        self.playerMoves += [Move(None, None, None, 'QUIT')]
        if self.playerIsHuman():
            for i in range(len(self.playerMoves)):
                Logger.log('{:>4}. {}'.format(i + 1, repr(self.playerMoves[i])))
            Logger.log('')

    def printQuit(self):
        """Prints quit message and associated player"""
        Logger.log('Player {} has quit the game'.format(self.currentPlayer + 1))

    def printInvalidMoveMessage(self):
        """Prints invalid move message"""
        Logger.log('Invalid move selection. Please try again.', '\n')

    def closeLogger(self):
        """Closes logger, used at program exit"""
        Logger.close()


class Card():
    """Representation of ordinary card found in a 52-card deck

    Attributes:
        rank (str): Rank of card (e.g., 10, Jack, King, Queen)
        suit (str): Suit of card (e.g., hearts, diamonds)
        visible(boolean, optional): Visibility flag for card, used when printing
    """

    def __init__(self, rank, suit, visible=False):
        self.rank = rank
        self.suit = suit
        self.visible = visible
        if suit == 'Hearts' or suit == 'Diamonds':
            self.isRed = True
        else:
            self.isRed = False

    def __repr__(self):
        if self.visible:
            # Returns string of rank and suit character if visible
            return '{}{}'.format(self.rank, suitCharacters[self.suit])
        else:
            # Returns string of empty square brackets to represent face-down card
            return '[ ]'

    def face(self):
        """Returns face value of card (i.e., rank and suit character)"""
        return '{}{}'.format(self.rank, suitCharacters[self.suit])

    def makeVisible(self):
        """Sets visibility of card to true"""
        self.visible = True

    def makeInvisible(self):
        """Sets visibility of card to false"""
        self.visible = False


class Deck():
    """Representation of 52-card deck, used for initializing piles and hands

    Attributes:
        cards (list): List of cards containing each combination of rank and suit

    Note:
        Deck is shuffled when initialized, thus, does not require further shuffling
    """

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffles deck in random order"""
        random.shuffle(self.cards)

    def distributeCardsToPlayers(self, howManyEach, players):
        """Distributes a given number of cards to each player in player list

        Args:
            howManyEach (int): Number of cards to distribute to each player
            players (list): List of players able to receive cards
        """
        for player in players:
            for card in range(howManyEach):
                player.receiveCard(self.cards.pop())

    def distributeCardsToPiles(self, howManyEach, piles):
        """Distributes cards to piles based off values in given list of integers

        Args:
            howManyEach (list): List of number of cards to distribute to each corresponding pile
            piles (list): List of piles that will receive cards

        Note:
            Length of howManyEach list must be less than or equal to length of piles list
        """
        for i in range(len(piles)):
            for card in range(howManyEach[i]):
                piles[i].receiveCard(self.cards.pop())


class Pile():
    """Representation of collection of cards in game (e.g., deck, hand, waste)

    Attributes:
        name (str): Name of pile, used for printing moves
        cards (list, optional): List of cards, may be added later from deck or other piles
    """

    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards or []

    def __repr__(self):
        return repr(self.cards)

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def indexOf(self, card):
        """Returns the index of the card whose face value matches the given string, or -1 otherwise

        Args:
            card (str): Face value of card to find in pile
        Returns:
            Index of card with matching face value, or -1 otherwise
        """
        for i in range(len(self.cards)):
            if self.cards[i].face() == card:
                return i
        return -1

    def remove(self, index):
        """Removes card at given index, if within list boundaries

        Args:
            index (int): Index of card in pile
        Returns:
            Removed card, or None
        """
        if index in range(len(self.cards)):
            return self.cards.pop(index)
        else:
            return None

    def receiveCard(self, card):
        """Appends given card to pile

        Args:
            card (Card): Card to be added to pile
        """
        self.cards.append(card)

    def top(self):
        """Returns top card of pile"""
        return self.cards[-1]

    def giveOneCard(self, otherPile):
        """Gives the top card of the pile to another pile

        Args:
            otherPile (Pile): Pile to receive top card
        """
        otherPile.receiveCard(self.cards.pop())

    def giveSetOfCards(self, indexToGive, otherPile):
        """Gives set of cards, beginning with given index, to another pile

        Args:
            indexToGive (int): Index representing start of cards to give
            otherPile (Pile): Pile to receive set of cards
        """
        remainingCards = len(self.cards) - indexToGive

        # Removes remaining cards, ignoring out of bounds indexes by using range
        for i in range(remainingCards):
            otherPile.receiveCard(self.cards.pop(indexToGive))

    def makeAllCardsVisible(self):
        """Sets visibility of all cards in pile to true"""
        for card in self.cards:
            card.makeVisible()

    def makeAllCardsInvisible(self):
        """Sets visibility of all cards in pile to false"""
        for card in self.cards:
            card.makeInvisible()

    def isEmpty(self):
        """Returns true if no cards in pile"""
        return len(self.cards) == 0

    def shuffle(self):
        """Shuffles pile in random order"""
        random.shuffle(self.cards)


class Board():
    """Game board used for managing and printing piles

    Attributes:
        piles (list, optional): List of piles; can be added later during setup
    """

    def __init__(self, piles=None):
        self.piles = piles or []
        self.setup()

    def __repr__(self):
        raise NotImplementedError

    def setup(self):
        """Sets up piles in game board, assigning pile names and any needed variables"""
        raise NotImplementedError


class Rulebook():
    """Rules of game used as guards in machine; also used for finding possible moves for players

    Note:
        All functions should accept a game object as a parameter and return a boolean, apart from the getMoves()
        method used for retrieving all possible moves for the current player
    """

    def true(self, game):
        """Guard which always returns true"""
        return True

    def validMove(self, game):
        """Guard for validating moves; move selection must be within the bounds of the player's move list"""
        return game.selectedMove >= 0 and game.selectedMove < len(game.playerMoves)

    def quit(self, game):
        """Guard for determining whether a player has quit the game"""
        return game.quit

    def win(self, game):
        """Guard for determining whether the game has been won"""
        raise NotImplementedError

    def getMoves(self, game):
        """Returns list of possible moves for the current player"""
        raise NotImplementedError


class Move():
    """Representation of a possible move by the current player

    Attributes:
        cardIndex (int): Index of card to move in from pile
        fromPile (Pile): Pile in which card is currently located
        toPile (Pile): Pile which will receive the movable card
        moveType (str): Type of move as defined in the game's move dictionary
    """

    def __init__(self, cardIndex, fromPile, toPile, moveType):
        self.cardIndex = cardIndex
        self.fromPile = fromPile
        self.toPile = toPile
        self.moveType = moveType

    def __repr__(self):
        # All additional game moves not listed below, along with their corresponding string representations,
        # should be added as a switch case in the conditions below
        if self.moveType == 'DRAW':
            return 'Draw card from Deck'
        elif self.moveType == 'RESHUFFLE':
            return 'Reshuffle Deck'
        elif self.moveType == 'SHOW':
            return 'Show {}'.format(self.fromPile.name)
        elif self.moveType == 'QUIT':
            return 'Quit'
        else:
            return '{} {} from {} to {}'.format(
                self.moveType.title(),
                self.fromPile[self.cardIndex].face(),
                self.fromPile.name,
                self.toPile.name)


class Player():
    """Representation of a player in a game

    Attributes:
        hand (Pile): Player's current hand of cards
    """

    def __init__(self):
        self.hand = Pile('Hand')

    def __repr__(self):
        return '{{type: {}, hand: {}}}'.format(self.__class__.__name__, repr(self.hand))

    def isA(self, type):
        """Returns whether the player instance is of a particular type; useful for determining which players are human or AI"""
        return isinstance(self, type)

    def receiveCard(self, card):
        """Appends given card to player hand"""
        raise NotImplementedError

    def chooseMove(self):
        """Selects move from list of possible moves

        Returns:
            Selected move as index in player moves list
        """
        raise NotImplementedError

    def chooseSuit(self):
        """Selects suit form list of possible suits

        Returns:
            Selected suit as index in list of suits
        """
        raise NotImplementedError


class HumanPlayer(Player):
    def receiveCard(self, card):
        # Cards of human players are made visible
        card.makeVisible()
        self.hand.receiveCard(card)

    def chooseMove(self):
        try:
            Logger.log('Choose your next move:')
            userInput = input()
            # Attempt to force user input as integer
            selectedMove = int(userInput) - 1
            Logger.log(str(selectedMove + 1), printLog=False)
        except ValueError:
            # Set input as invalid selection if error occurs
            selectedMove = -1
            Logger.log(userInput, printLog=False)
        Logger.log('')
        return selectedMove

    def chooseSuit(self):
        # Prints suits as list of options
        suitOptions = ''
        for i in range(len(suits)):
            suitOptions += '{:>4}. {}\n'.format(i + 1, suitCharacters[suits[i]])

        # Continue asking for selected suit until valid input received
        selectedSuit = -1
        while selectedSuit < 0:
            Logger.log(suitOptions, '\n', 'Choose suit to switch to:')
            try:
                userInput = input()
                # Attempt to force use input as integer
                selectedSuit = int(userInput) - 1
                Logger.log(str(selectedSuit + 1), printLog=False)
            except ValueError:
                # Set input as invalid selection if error occurs
                selectedSuit = -1
                Logger.log(userInput, printLog=False)
            Logger.log('')

            if not selectedSuit in range(0, 4):
                # Print invalid selection message if index out of bounds
                Logger.log('Invalid suit selection. Please try again.', '\n')
                selectedSuit = -1

        Logger.log('Suit has been changed to {}\n'.format(suits[selectedSuit]))
        return selectedSuit

class AIPlayer(Player):
    def receiveCard(self, card):
        # Cards of AI players are made invisible
        card.makeInvisible()
        self.hand.receiveCard(card)

    def chooseMove(self):
        # Always select first option in list of moves
        return 0

    def chooseSuit(self):
        # Randomly select suit to play
        selectedSuit = random.choice(range(0, 4))
        Logger.log('Suit has been changed to {}\n'.format(suits[selectedSuit]))
        return selectedSuit
