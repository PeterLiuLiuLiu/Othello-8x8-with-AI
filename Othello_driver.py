'''
CS5001 Fall 2021
LIU Chun Yan (Peter)
This is a milestone 3 of othello
'''
from GameEngine import *

def main():  


    try:
        # Create an instance of GameEngine, starts the game
        GameEngine(8, to_draw = True, play_with_AI = True)

    except TypeError as ex:
        print("TypeError has occured: ", ex)

    except ValueError as ex:
        print("ValueError has occured: ", ex)
#
#
#
if __name__ == "__main__":
    main()


# 