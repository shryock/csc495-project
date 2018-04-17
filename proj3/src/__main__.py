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

    machine = None
    
    try:
        gameChoice = int(input())
        if gameChoice == 1:
            machine = GameMachine(Solitaire())
        elif gameChoice == 2:
            machine = GameMachine(CrazyEights())
        else:
            raise ValueError()

        print()
        machine.startGame()
    except ValueError:
        print('Invalid Choice... Goodbye.')
    except KeyboardInterrupt:
        if machine and machine.game:
            machine.game.closeLogger()
        print('\nGame exited')


if __name__ == '__main__':
    __main__()
