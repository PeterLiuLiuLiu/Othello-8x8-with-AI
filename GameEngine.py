

import turtle
from DisplayTurtleGame import *
from GameBoard import *
from StoreTileChanged import *
from Othello_AI import *


STARTING_COLOR = 'b'
SCORE_FILE_TO_SAVE = "score.txt"


class GameEngine():
    '''
    The core of the game that:
        1. create an instance of GameBoard which acts as the core of the game's data model
        2. interact between model (GameBoard), view (displayTurtleGame) and controller (screen.onclick(get_move))
            and pass information wto each instances of MVC classes
        3. Triggered by main Othello driver instantiation

    Attribute:
        game_board_size: 
            total number of tile per side on the square game board
        starting_player_to_move: 
            "b" or "w" player to move, defaulted as "b"
        game_board:
            an instance of GameBoard class which contains all the data of the game_board
        display_turtle_game: 
            if to_draw_on_turtle, this instance of displayeTurtleGame is created
        tile_tuple:   
            all the tile class stored in a tuple for information of coordinates

    Method:
        __init__: 
            initialize class attritibutes and check for class attritube input errors
        __eq__: 
            compare this GameEngine instance with another and return a boolean
        __str__: 
            return a string representation of this class
        place_move: place a move on the tile when the x, y are specified from user input, 
            convert 2D coordinate into 1D and calls place_move_1D function to update the instance of GameBoard class,
            and get the result of the move, a string
        place_move_1D: 
            update the instance of GameBoard class with the 1D coordinate, 
            from 0 = upper left to self.game_board_size ** 2 - 1 = lower right,
            and get the result of the move, a string
        pass_move_into_model_and_check_winner:
            pass the move made by user into GameBoard to update, if valid, return result and print the next or or announce winner
    '''
#
    def __init__(self, game_board_size, to_draw = False, play_with_AI = True, difficulty = "hard"):
        '''
        Method -- __init__
            To be initialized when class is instantiated
        Parameter:
            game_board_size: positive integer denoting the side length of board
                In fact it must be a positive even numbered integer larger than 2
        Return:
            none
        Possible Error raised:
            TypeError: game_board_size is not int
            TypeError: to_draw_on_turtle must be of type bool
            ValueError: game_board_size must be either 4 or 8
            ValueError: difficulty must be either 'easy' or 'hard'
        ''' 

        if not isinstance(game_board_size, int):
            raise TypeError("game_board_size must be of type int.")

        if game_board_size < 0 or game_board_size % 2 != 0:
            raise ValueError("game_board_size for __init__ must be a positive even whole number")

        if not isinstance(to_draw, bool):
            raise TypeError("to_draw must be of instance bool")
        
        if difficulty not in ["easy", "hard"]:
            raise ValueError("difficulty scale of AI must be either 'easy' or 'hard'")
            

        self.to_draw = to_draw

        self.play_with_AI = play_with_AI

        self.start_color = STARTING_COLOR
        self.game_board_size = game_board_size
        self.game_board = GameBoard(game_board_size, starting_player_to_move = self.start_color)

        if play_with_AI:
            self.AI = Othello_AI(difficulty) # white

        # initialize a instance of AI class here, triggered by __init__, but play calculation is triggered in get_move method

        if self.to_draw and self.game_board_size > 0:
            # viewer class defined
            self.display_turtle_game = DisplayTurtleGame(self)
            
            # After initialization of graphics, display the first player to move, if the game has not ended before it starts
            # Handles edge case size == 2 game ends after initialization
            if self.game_board.get_game_board_size() != 2:
                print(f"{self.game_board.get_current_player()}'s move") 

            # To prevent turtle screen from closing, if there is yet to be a winner
            turtle.mainloop()
#         
#
#
    def __eq__(self, other):
        '''
        Method -- __eq__:
            equate the classes together
        Parameter:
            other: another instance of GameEngine
        Return: 
            true if their __str__ returned is identitical, 
                and all its elements are identitcal
            False if otherwise
        Possible Error raised:
            no error raised, return false if other is not an instance of GameEngine
        '''
        if not isinstance(other, GameEngine):
            return False


        return (self.__str__() == other.__str__()) and\
            (self.game_board == other.game_board)
#
#
#
    def __str__(self):
        '''
        Method -- __str__
            represent the object GameEngine as a string
        Parameter:
            none
        return:
            a string representation of the object
        Possible Error raised:
            none
        '''
        return f"A Game Engine of Othello with size {self.game_board_size} by {self.game_board_size}."
#
#
#       
    def place_move(self, move_x, move_y):
        '''
        Method -- place_move:
            treat the gameboard as 2D and input the coordinate as an address in an (x, y) input
            core of game, to determine if the updating is valid, replace slot with player_move if so
            else do nothing and raise error
            This method funnels back to place_move_1D by transforming (move_x, move_y) into move in 1D map [0, self.game_board_size ** 2)
        Parameter:
            move_x: horizontal coordinate of selected move at the board
            move_y: vertical coordinate of selected move at the board
        Return:
            return a string, indicate the state of game, either:
                CONTINUE: the game has to continue without a winner
                BLACK: black has won with no more legal moves on board
                WHITE: white has won with no more legal moves on board 
                TIE: both players has equal amount of pieces on the board with no more legal moves on boards
        Possible Error raised:
            TypeError: both must move_x and move_y must be of type int
            ValueError: both move_x and move_y must be within [0, self.game_board_size) 
        '''
        if not isinstance(move_x, int) or not isinstance(move_y, int):
            raise TypeError("move_x and move_y must be of type int")
    
        if move_x < 0 or move_x >= self.game_board_size or move_y < 0 or move_y >= self.game_board_size:
            raise ValueError(f"move_x and move_y must be without range [0, {self.game_board_size})")


        return self.place_move_1D(move_x + move_y * self.game_board_size)
#
#
#
    def place_move_1D(self, move):
        '''
        Method -- place_move_1D:
            treat the gameboard as 1D and input the coordinate as an address [0, self.game_board_size ** 2) input
            core of game, to determine if the updating is valid, replace slot with player_move if so
            else do nothing and raise error
        Parameter:
            move: 1D representation of game_board_size
        Return:
            return a string, indicate the state of game, either:
                CONTINUE: the game has to continue without a winner
                BLACK: black has won with no more legal moves on board
                WHITE: white has won with no more legal moves on board 
                TIE: both players has equal amount of pieces on the board with no more legal moves on boards
        Possible Error raised:
            TypeError: must move must be of type int
            ValueError: both move must be within [0, self.game_board_size ** 2) 
        ''' 
        if not isinstance(move, int):
            raise TypeError("move must be of type int")

        if move < 0 or move >= self.game_board_size ** 2:
            raise ValueError(f"move must be without range [0, {self.game_board_size** 2})")

               
        result = self.game_board.update_game_state(move)

        if self.to_draw:
            self.display_turtle_game.refresh_game_screen()

        return result
#
#
#
    def pass_move_into_model_and_check_winner(self, tile_index):
        '''
        Method -- pass_move_into_model_and_check_winner:
            pass the move made by user into GameBoard to update, if valid, return result and print the next or or announce winner
            if result is CONTINUE, either wait for player's move or if AI is enabled, call AI to move
        Parameters:
            tile_index: the 1D address of tile address where the user clicked
        Returns:
            none, just print the upcoming player to move, or announce the winner with counts for each color
        Possible Error:
            TypeError: tile_index must of type int
            ValueError: tile_index must be within [0, self.game_board_size ** 2)
        '''

        if not isinstance(tile_index, int):
            raise TypeError("tile_index pass in must be of type int")
        
        if tile_index < 0 or tile_index >= self.game_board_size ** 2:
            raise ValueError("tile_index must be withint [0, self.game_board_size ** 2)")


        result = self.place_move_1D(tile_index)
        
        # Probably throw the self.game_board into the AI class and get the return as 1D address for optimal move, pass into self.place_move_1D

        if result != "CONTINUE":
            result_count = self.game_board.get_result_count()
            if result == "TIE":
                print(f"GAME ENDS in TIE! Both black and white have {result_count['w']} pieces on board")
            elif self.play_with_AI:
                print(f"GAME ENDS, COMPUTER(WHITE) WINS with black: {result_count['b']} and white: {result_count['w']}!") 
            else:
                print(f"GAME ENDS, {result} WINS with black: {result_count['b']} and white: {result_count['w']}!") 

            # If the place_move method returns not continue, game ends after 3 seconds
            self.save_black_result_to_file()
            print(">>> Please click on the game console to exit game <<<")
            turtle.exitonclick()

        elif self.play_with_AI and self.game_board.get_current_player() == "white":
            self.call_AI_move()
#
#
#
    def call_AI_move(self):
        '''
        Method -- call_AI_move:
            get move from AI and call the move
        Parameter:
            none
        Return:
            none
        Possible Error raised:
            none
        '''
        move = self.AI.get_move(self.game_board)
        print(f"Computer (white) playing {move}th tile")
        self.pass_move_into_model_and_check_winner(move)
#
#
#
    def save_black_result_to_file(self, filename = SCORE_FILE_TO_SAVE):
        '''
        Method -- save_black_result_to_file:
            always save the black's score
        Parameters, Returns, Possible Error raise:
            none
        '''
        # Get a flatten list from result_count dictionary
        if not isinstance(filename, str):
            raise ValueError("Please input a string for filename to save")


        result_count = self.game_board.get_result_count()

        if result_count["w"] == 0 and result_count["b"] == 0:
            print("Game has not ended with a winner, no score saved.")
            return

        print("Saving score for human player...")
        player_name = input("Please pprovide your name so we can save your score: ")
        score = result_count["b"]
        if score > self.get_max_score_from_file():
            self.save_score_to_file(player_name, score, insert_front = True)
        else:
            self.save_score_to_file(player_name, score, insert_front = False)

#
#
#
    def get_max_score_from_file(self, filename = SCORE_FILE_TO_SAVE):
        '''
        Method -- get_max_score_from_file:
            FInd the maximum score, the first entry score of the file
        Parameters:
            filename: filename to explore
        Possible Error raise:
            errors from reading files
        Return:
            an int, maximum score of the file
        '''
        try:
            with open(filename, "r") as file:
                file_content = file.read()
                if file_content == "":
                    return 0
                else:
                    list_of_player = file_content.split("\n")
                    return int(list_of_player[0].split(" ")[1])
                
        except:
            # print("Something is wrong with the file...")
            return 0
#
#
#
    def save_score_to_file(self, player_name, score, insert_front = False, filename = SCORE_FILE_TO_SAVE):
        '''
        Method -- save_score_to_last_of_list:
            if game score is larger than the largest value on SCORE_FILE_TO_SAVE
        Parameters:
            player_name: a string name of player
            score: an int containing score
            insert_front: whether the info append at back of insert in front of file
            filename: if not testing, use default
        Returns: 
            none
        Possible Error raise:
            TypeError: player_name must be of type str
            TypeError: score must be of type int
            TypeError: insert_front must be of type bool
            ValueError: insert_front for winner only if the file contains no greater scores
            errors from reading files
        '''
        if not isinstance(player_name, str):
            raise TypeError("player_name must be of type str")
        
        if not isinstance(score, int):
            raise TypeError("score must be of type int")

        if not isinstance(insert_front, bool):
            raise TypeError("insert_front must be of type bool")

        if self.get_max_score_from_file(filename) >= score:
            if insert_front:
                raise ValueError("Player must be appended at the back of the file content")
        
        elif insert_front == False:
                raise ValueError("Player must be inserted at the front of the file content")


        content_to_write = f"{player_name} {score}\n"
        try:
            with open(filename, "r") as file:
                original_file_content = file.read()

            if insert_front:
                content_to_write += original_file_content
                with open(filename, "w") as file:
                    file.write(content_to_write)

            else:
                if original_file_content[-1] != "\n":
                    content_to_write = "\n" + content_to_write
                with open(filename, "a") as file:
                    file.write(content_to_write)
                
        except:
            print("Something is wrong with file...")
#
# 
#  
    def end_corrupted_game(self):
        '''
        Method - game_corrupted_end_console:
            called in DisplayTurtleGame when the player broke the game, triggered by except block in get__move
        Parameters, Return, Possible Error raise:
            none, just close turtle screen
        '''
        turtle.bye()
#
#
#