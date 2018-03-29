import Solitaire as sol
import CrazyEights as crazy
import CrazyEightsFSM as ceFSM

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
    3) Crazy Eights (FSM)

    """)

    gameChoice = int(input())
    if gameChoice == 1:
        sol.__main__()
    elif gameChoice == 2:
        crazy.__main__()
    elif gameChoice == 3:
        ceFSM.__main__()
    else:
        print("Invalid Choice... Goodbye.")

if __name__ == '__main__':
    __main__()
