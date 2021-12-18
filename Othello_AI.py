
import random
from GameBoard import *

TREE_LOOKUP_ITERATION = 2       # For normal laptop, recommend a max. search depth of 2 since it equals a search of white --> black --> white --> black --> white already
HARD_AI_CHANGE_TACTICS = 15     # Start to be aggressive whe there are less space in the tile

SWEET_16_FACTOR = 5
# prefered placement location of the piece at early phase of game, center 4x4 board
SWEET_16_TILES = (18, 19, 20, 21,
                  26, 27, 28, 29,
                  34, 35, 36, 37,
                  42, 43, 44, 45,
                 )

EDGE_TILE_EXCLUDE_HORRIBLE_4_X_FACTOR = 4
EDGE_TILE_EXCLUDE_HORRIBLE_4_X = ( 2,  3,  4,  5,
                                  16, 24, 43, 40,
                                  22, 30, 38, 46,
                                  58, 59, 60, 61,
                                   )
                 
HORRIBLE_4_X = (9, 14, 49, 54,) # NO NO, will easily let opponent capture corners, diagonals next to corners
HORRIBLE_4_X_FACTOR = -30

SECOND_HORRIBLE_8_X = (1, 8, 6, 15, 48, 57, 55, 62,) # Not preferred, horizontal and vertical adjecent to corners
SECOND_HORRIBLE_8_X_FACTOR = -10

CORNER_4 = (0, 7, 56, 63, ) # Must take, 4 corners of 8x8 board
CORNER_4_FACTOR = 100

WIN_FACTOR  =   10E20
LOSE_FACTOR =  -10E20

class Othello_AI():
    def __init__(self, difficulty):
        '''
        Method -- __init__:
            To be initialized when class is instantiated
        Parameter:
            difficulty: difficultyof AI 
        Return:
            none
        Possible Error raised:
            ValueError: difficulty must be either 'easy' or 'hard'
        '''
        if difficulty not in ["easy", "hard"]:
            raise ValueError("Difficulty scale of AI must be either 'easy' or 'hard'")


        self.difficulty = difficulty

        self.move_score_dict = dict()
        self.current_move_explored = -1        
        self.number_of_immediate_child = 0
#
#
#
    def get_move(self, game_board):
        '''
        Method -- get_move:
            this method is called external to get the AI move from calculation within this class
        Parameters:
            game_board: an object of GameBoard class
        Return: 
            an int, 1D address of the "best" move determined by the computer
        Possible Error raised:
            game_board class must be an instance of class GameBoard, and have a valid game_state
        '''

        if not isinstance(game_board, GameBoard) or not game_board.is_valid_game_state():
            raise ValueError("game_board must be of an object instaniated from GameBoard class")


        if self.difficulty == "easy" or game_board.get_game_board_size() != 8:
            # AI will be set to easy if it is not 8x8
            move_to_return = self.get_move_from_easy_AI(game_board)

        else:
            move_to_return = self.get_move_from_difficult_AI(game_board)
        
        return move_to_return
#
#
#
    def get_move_from_easy_AI(self, game_board):
        '''
        Method -- get_move_from_easy_AI:
            easy AI just always throw random moves picked forom all availble spots
        Parameters:
            game_board: an object of GameBoard class
        Return: 
            an int, 1D address of the "best" move determined by the computer
        Possible Error raised:
            game_board class must be an instance of class GameBoard, and have a valid game_state
        '''
        if not isinstance(game_board, GameBoard) or not game_board.is_valid_game_state():
            raise ValueError("game_board must be of an object instaniated from GameBoard class")


        return random.choice(list(game_board.get_all_possible_moves().keys()))
#
#
#
    def get_move_from_difficult_AI(self, game_board):
        '''
        Method -- get_move_from_difficult_AI:
            called by get_move, decide the move based on how full the board is, 
            if the space remaining is less than the threshold to change tactics, full on pounce and capture as many pieces as possible,
            else use recursive method to look at most 2 steps ahead and determine which move at current stage brings the most value to computer itself
        Parameters:
            game_board: an object of GameBoard class
        Return: 
            an int, 1D address of the "best" move determined by the computer
        Possible Error raised:
            game_board class must be an instance of class GameBoard, and have a valid game_state
        '''
        if not isinstance(game_board, GameBoard) or not game_board.is_valid_game_state():
            raise ValueError("game_board must be of an object instaniated from GameBoard class")


        spaces_remaining =  list(game_board.get_game_state().values()).count("e")
        # print(f"\t>>> {spaces_remaining} empty tiles remaining.... ")

        all_possible_moves = game_board.get_all_possible_moves()

        if spaces_remaining < HARD_AI_CHANGE_TACTICS:
            # Based on the quiet moves earlier, try to capture as much pieces as possible when the game is going to end
            move = self.find_random_max_flipping_moves(game_board.get_all_possible_moves())

        else:
            for index, temp_move in enumerate(all_possible_moves):
                print(f"\t--------------- Exploring {index + 1} / {len(all_possible_moves)} moves ---------------")
                self.move_score_dict[temp_move] = 0
                self.current_move_explored = temp_move

                # One TREE_LOOKUP_ITERATION looks in one human black moves, as well as how it can move based on human move, always stop at computer white move
                # Branch out to all possible moves at current game_board and check all possible moves by human, and explore all possible moves based on computer based on every human moves, for ONE recursion
                self.recursive_lookup(game_board, temp_move, TREE_LOOKUP_ITERATION)

                # number_of_immediate_child looks at all possible moves of human player and divide them to get the average value given the temp_move, if equals zero, 
                # it means the game will end, no need to explore further, no need to take the average of possible moves dividing black
                # for instsance, possible moves by cpt is 18, 20, 35, and now looping 18; based on move of 18, human can then play 4 moves, 19, 20, 34, 50,
                # Each of the 4 moves will have a value and calculate back to the move 18, which then needs to average out by 4 since move 20 may have 10 moves, 
                # Without averaging, the value of 20 which has 10 black moves may have larger (positive or negative) value compared to 18 which leads to a move of 4 by human
                if self.number_of_immediate_child != 0:
                    self.move_score_dict[temp_move] /= self.number_of_immediate_child

                # reset to zero for another move to explore and populate at other temp_move
                self.number_of_immediate_child = 0

            print("\n")
            
            # return the key (move) with move value after recursive calculations
            move = max(self.move_score_dict, key=self.move_score_dict.get)
            self.move_score_dict = dict()

        return move
#
#
#
    def find_random_max_flipping_moves(self, all_possible_moves):
        '''
        Method -- find_random_max_flipping_moves:
            each possible moves will inflict opponent to be flipped, find the one that flips the move opponent
        Parameter:
            a dictionary containing keys: legal moves, and values: the flips of opponent resulting from playing the lagel move in key
        Return:
            an int, 1D address of the random move determined among all legal moves
        Possible Error raised
            all_possible_moves must be of type dictionary, and key within must all within 0 to 63
        '''
        if not isinstance(all_possible_moves, dict):
            raise TypeError("all_possible_moves must be of type dict")

        
        max_nos_of_flips = -1
        max_move_key = -1
        for key, value in all_possible_moves.items():
            if not isinstance(key, int) or key < 0 or key > 63:
                raise ValueError("key must be between 0 to 63 inclusive")

            if len(value) > max_nos_of_flips:
                    max_move_key = key
                    max_nos_of_flips = len(value)

        max_value_moves = list()
        for key, value in all_possible_moves.items():
            if len(value) == max_nos_of_flips:
                max_value_moves.append(key)

        return random.choice(max_value_moves)
#
#
#
    def recursive_lookup(self, game_board, move, lookup):
        '''
        Method -- recursive_lookup:
            Recursively looking for moves with best mobility given the move
            make penalty or reward based on constants of tile position that is strategically beneficial or determental
            Goes to the bottom of the tree and climb back up to return value to the caller
            change the class attritube self.move_score_dict and self.number_of_immediate_child for later calculations in main loop
        Parameter:
            game_board: an object of GameBoard class
            move: a move projected to traverse the subtree
            lookup: the depth of tree currently traversing, 
                    only reduce depth once white move is hit, no reduction when black move is hit since we would like to explore the ultimate white move possible,
                    Climb back up the tree if that particular loop is done with recursion with lower subtree, and go up only at black's turn
                    Only go up at black since only the black's turn signal end of all white's turn at lower subtree
        Return:
            depth of tree, an int
        Possible Error raised:
            game_board class must be an instance of class GameBoard, and have a valid game_state
            move: must be an int and between 0 to 64
            lookup must be of type int and smaller or equal to TREE_LOOKUP_ITERATION
        '''
        if not isinstance(game_board, GameBoard) or not game_board.is_valid_game_state():
            raise ValueError("game_board must be of an object instaniated from GameBoard class")

        if not isinstance(move, int):
            raise TypeError("move must be of type int")

        if not isinstance(lookup, int):
            raise TypeError("lookup must be of type int")
            
        if lookup > TREE_LOOKUP_ITERATION:
            raise ValueError("Invalid value for lookup")

        # First level to be traversed
        if lookup == TREE_LOOKUP_ITERATION and game_board.get_current_player() == "black":
            # nos. of immediate black moves for averaging
            self.number_of_immediate_child += 1

        # Base case
        if lookup == 0:
            # base of tree reached, traverse back up to other leaf node of white moves
            self.move_score_dict[self.current_move_explored] += 1
            return lookup + 1

        # custom deep copy of game_board object
        temp_game_board = game_board.copy_object()

        # if current player is black, all constants must be flipped, i..e capture corner for black is determental to white so positive becomes negative
        if temp_game_board.get_current_player() == "black":
            value_to_add_for_special_tiles = -1
        else:
            value_to_add_for_special_tiles = 1
    
        # play the projected move
        result = temp_game_board.update_game_state(move)

        # in case the move at search state will lead to a lost for AI
        self.assign_score_end_game_move(result)

        # calculate the possible moves based on projected game_state
        all_possible_moves = temp_game_board.get_all_possible_moves(False)

        # reward or punish, also give more weight to more recentl moves since they have less branch, since the number of leaf node is exponental to it's stem, will ignore the recent move without the power given to them
        self.assign_score_with_special_tiles(move, value_to_add_for_special_tiles, lookup)

        for projected_move in all_possible_moves:
            if temp_game_board.get_current_player() == "white":
                # count as lookup done only if we explored AI's moves, not human's move
                lookup -= 1
            # print("  " * (TREE_LOOKUP_ITERATION - lookup) + f"Exploring projected move on {projected_move}th tile, {temp_game_board.get_current_player()}'s turn")
            lookup = self.recursive_lookup(temp_game_board, projected_move, lookup)
            # print()

        # Base case
        if lookup != TREE_LOOKUP_ITERATION and temp_game_board.get_current_player() == "black":
            # Climb back up the tree if that particular loop is done with recursion with lower subtree, and go up only at black's turn
            # Only go up at black since only the black's turn signal end of all white's turn at lower subtree
            return lookup + 1

        return lookup
#
#
#
    def assign_score_end_game_move(self, result):
        '''
        Method -- assign_score_end_game_move:
            to assign WIN and LOSE factor to move that results in win or lose for white
        Parameters:
            result: BLACK or WHITE
        Return:
            none, just add or substract to the self.move_score_dict
        Possible Error raised:
            ValueError: result must be either "black" or "WHITE" or "continue" or "TIE"
        '''
        expected_result_value = ["BLACK", "WHITE", "CONTINUE", "TIE"]
        if result not in expected_result_value:
            raise ValueError(f"result must be one of the following: {expected_result_value}")


        if result == "BLACK": 
            self.move_score_dict[self.current_move_explored] += LOSE_FACTOR
        elif result == "WHITE":
            self.move_score_dict[self.current_move_explored] += WIN_FACTOR
#
#
#
    def assign_score_with_special_tiles(self, move, value_to_add_for_special_tiles, lookup):
        '''
        Method -- assign_score_with_special_tiles:
            assign the self.move_score_dict when move is at strategic locations, to add or substract from the accumlated values
        Parameters:
            move: the move to be evaluted
            value_to_add_for_special_tiles: 1 or -1, depends on if it is benefitial to white
            lookup: the depth of exploration used for power of constants
        Return:
            none, just add or substract to the self.move_score_dict
        Possible Error Raised:
            move: must be between 0 to 63 inclusive
            value_to_add_for_special_tiles: must be either 1 or -1
            lookup: must be an int smaller than or equal to TREE_LOOKUP_ITERATION
        '''
        if move < 0 or move > 63:
            raise ValueError("move must be between 0 to 63 inclusive")
        
        if value_to_add_for_special_tiles != 1 and value_to_add_for_special_tiles != -1:
            raise ValueError("value_to_add_for_special_tiles must be either 1 or -1")

        if lookup > TREE_LOOKUP_ITERATION:
            raise ValueError("lookup must be smaller than or equal to TREE_LOOKUP_ITERATION")

        
        if move in SWEET_16_TILES:
            self.move_score_dict[self.current_move_explored] += value_to_add_for_special_tiles * self.power_with_sign_remained(SWEET_16_FACTOR, lookup + 1)
        elif move in EDGE_TILE_EXCLUDE_HORRIBLE_4_X:
            self.move_score_dict[self.current_move_explored] += value_to_add_for_special_tiles * self.power_with_sign_remained(EDGE_TILE_EXCLUDE_HORRIBLE_4_X_FACTOR, lookup + 1)
        elif move in CORNER_4:
            self.move_score_dict[self.current_move_explored] += value_to_add_for_special_tiles * self.power_with_sign_remained(CORNER_4_FACTOR, lookup + 1)
        elif move in HORRIBLE_4_X:
            self.move_score_dict[self.current_move_explored] += value_to_add_for_special_tiles * self.power_with_sign_remained(HORRIBLE_4_X_FACTOR, lookup + 1)
        elif move in SECOND_HORRIBLE_8_X:
            self.move_score_dict[self.current_move_explored] += value_to_add_for_special_tiles * self.power_with_sign_remained(SECOND_HORRIBLE_8_X_FACTOR, lookup + 1)
#
#
#
    def power_with_sign_remained(self, num, pow):
        '''
        Method -- power_with_sign_remained
            just a utils method that preserves the sign when doing power
        Parameter:
            two numbers: num, pow
        Return:
            an int or float
        Possible Error raised:
            num, pow must be of type int or float
        '''
        if not isinstance(num, int) and not isinstance(num, float):
            raise TypeError("num must be of type int or float")

        if not isinstance(pow, int) and not isinstance(pow, float):
            raise TypeError("pow must be of type int or float")


        if num < 0:
            return - abs(num) ** pow
        else:
            return num ** pow
#
#
#
    def calculate_game_state_score(self, game_board):
        '''
        Method -- calculate_game_state_score:
            at base case, calculate the score of projected move based on how many possible moves
        Parameters:
            game_board: an object of GameBoard class
        Return: 
            an int, the amount of possible moves given a game_state
        Possible Error raised:
            game_board class must be an instance of class GameBoard, and have a valid game_state
        '''
        if not isinstance(game_board, GameBoard) or not game_board.is_valid_game_state():
            raise ValueError("game_board must be of an object instaniated from GameBoard class")


        return len(game_board.get_all_possible_moves())
#
#
#
