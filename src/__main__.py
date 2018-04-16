from games.Solitaire import Solitaire
from games.CrazyEights import CrazyEights
from model.machine import GameMachine

def __main__():
    print("""
    You are alone, in the middle of the woods.
    You have no map.
    No compass.
    No friends.

    But what you do have, is a deck of cards and
    the knowledge of two fantastic games to get
    you through the night.

    ...Solitaire
    ...and Crazy Eights

    Which would you like to play?
    1) Solitaire
    2) Crazy Eights
    """)

    try:
        gameChoice = int(input())
        if gameChoice == 1:
            game = GameMachine(Solitaire())
        elif gameChoice == 2:
            game = GameMachine(CrazyEights())
        else:
            raise ValueError()

        print()
        game.startGame()
    except ValueError:
        print("Invalid Choice... Goodbye.")

if __name__ == '__main__':
    __main__()
