from Piece import *
from StoreTileChanged import *

class GameBoard():
    '''
    This contains is the game board object, the class upon instantiation, the class is the the model of game

    Atttribute:
        size: number of tile per side of the square game board
        current_player_to_move:
            "b" or "w" player's turn
        opponent:  
            the opposite of current_player_to_move
        game_state:
            the core dictionary which stores the state of each tile 
            key: [0, size ** 2 - 1)
            value: "w" = white; "b" = black; "e" = empty
        valid_moves:
            dictionary that checks and record all the valid moves based on game_state and current_player_to_move
        move_control:
            dictionary that stores the way to traverse in a size x size board
        result_count:
            count the number of 'b' and 'w' piece on the board, can be returned by getter in case game ends
        temp_direction:
            list that appends the tile number when traversing the board via move_control, -1 denotes invalid slot,
            which eventually makes that temporary direction explored invalid    

    Method:
        __init__, init_game, is_valid_game_state, is_valid_move, get_game_state, get_game_board_size, update_game_state,
        get_possible_flips, look_up_direction, check_edge_of_board_for_neighbors, is_game_board_full, 
        is_no_legal_moves, check_winner, calculate_four_board_center_slots, update_current_player, get_current_player etc....
    '''
#
    def __init__(self, size, starting_player_to_move, is_tree_search = False):
        '''
        Method -- __init__
            To be initialized when class is instantiated, also call init_game method to initialize the game
        Parameter:
            size: number of tile per side of the square game board
            starting_player_to_move: "b" or "w" to start the game, has been defaulted to "b"
        Return:
            none
        Possible Error raised:
            TypeError: is_tree_search must be of type bool
            TypeError: size must be of type int
            ValueError: size must be either 4 or 8
            ValueError: starting_player_to_move must be either "b" or "w"
        '''
        if not isinstance(size, int):
            raise TypeError("size for __init__ must be of type int")
            
        if size < 0 or size % 2 != 0:
            raise ValueError("size for __init__ must be a positive even whole number")

        if starting_player_to_move != "b" and starting_player_to_move != "w":
            raise ValueError("starting_player_to_move must be either 'w' or 'b'")

        if not isinstance(is_tree_search, bool):
            raise TypeError("is_tree_search must be of type bool")


        self.size = size

        # starting player is black by default
        self.current_player_to_move = starting_player_to_move
        if starting_player_to_move == "w": self.opponent = "b"
        else: self.opponent = "w"

        self.game_state = dict()
        self.valid_moves = dict()
        self.move_control = {# To traverse from a said coordinate to eight directions
            "down": size,
            "up": - size,
            "left": -1,
            "right": 1,
            "lower_right": size + 1,
            "lower_left": size - 1,
            "upper_right": 1 - size,
            "upper_left": -1 - size,
        }


        self.color_conversion = {
            "w": "white",
            "b": "black",
        }
    
        self.result_count = {"w": 0, "b": 0}
        self.setting_board = "e"
        self.temp_direction = list()
        self.final_tiles_to_flip = list()

        self.is_tree_search = is_tree_search

        self.init_game()
#
#
#
    def __eq__(self, other):
        '''
        Method -- __eq__:
            equate the classes together
        Parameter:
            other: another instance of GameBoard
        Return: 
            true if their __str__ returned is identitical, 
                and all its elements in gamestate are identitcal
            False if otherwise
        Possible Error raised:
            no error raised, return false if other is not an instance of GameBoard
        '''
        if not isinstance(other, GameBoard):
            return False


        return (self.__str__() == other.__str__()) and\
            (self.get_game_state() == other.get_game_state())
#
#
#
    def __str__(self):
        '''
        Method -- __str__
            represent the object GameBoard as a string
        Parameter:
            none
        return:
            a string representation of the object
        Possible Error raised:
            none
        '''
        return f"A Game Board model of Othello with size {self.size} by {self.size} and a current move by player '{self.current_player_to_move}'."
#
#
#
    def copy_object(self):
        '''
        Method -- copy_object:
            to do a deep copy of game_board, not a shallow copy
        Parameters, Returns, Possible Error raised:
            none
        '''
        obj = GameBoard(self.size, self.current_player_to_move, is_tree_search = True)
        obj.game_state = dict()
        for key in self.game_state:
            # deep copying the dictionary to another address
            # Orelse the the memoery address of obj.game_state will change the original self.game_state as well
            obj.game_state[key] = self.game_state[key]
        return obj
#
#
#
    def init_game(self):
        '''
        Method -- init_game
            To initialize the whole board to empty piece, "e"
            except the 4 slots in center with "b" and "w"
        Parameter:
            none
        Return:
            none
        Possible Error raised:
            none
        '''
        move = dict()
        for coordinate in range(self.size ** 2):
            self.game_state[coordinate] = "e"

        center_four_slots = self.calculate_four_board_center_slots()
        for index, first_move in enumerate(center_four_slots):
            if index == 0 or index == 3:
                self.game_state[first_move] = "w"
            else:
                self.game_state[first_move] = "b"
#
#  
#  
    def is_valid_game_state(self):
        '''
        Method -- is_valid_game_state
            checking the validity of dictionary data stored in this class
        Parameter:
            none
        Return:
            Raise Error or return True is game_state is valid
        Possible Error raise:
            TypeError: self.game_state must be of type dict
            ValueError: self.game_state must have all int keys
            ValueError: self.game_state must have values of either "w", "b" or "e"
            ValueError: self.size must be a positive even whole number, i.e. 0, 2, 4, 6, 8,...
            ValueError: the length of dictionary self.game_state must be the square of self.size
        '''
        valid_value = ("e", "w", "b")

        if not isinstance(self.game_state, dict):
            raise TypeError("dictionary must be of type dict")
    
        for key, value in self.game_state.items():
            if not isinstance(key, int):
                raise TypeError("keys of self.game_state must be of type int")
            
            if key < 0 or key >= self.size ** 2:
                raise ValueError("keys value is not valid")
            
            if value not in valid_value:
                raise ValueError(f"value is of {key} not valid")

        if not isinstance(self.size, int):
            raise TypeError("self.size must be of type int")

        if self.size < 0 or self.size % 2 != 0:
            raise ValueError("self.size of game must be a positive even whole number")

        if len(self.game_state) != self.size ** 2:
            raise ValueError("length of self.game_state dictionary must be the square of self.size")


        return True
#
#
#
    def is_valid_move(self, move):
        '''
        Method -- is_valid_move
            checking the validity of move
        Parameter:
            none
        Return:
            Raise Error or return True if move is valid
        Possible Error raise:
            TypeError: move must be of type int
            ValueError: move must be within the range of [0, self.size ** 2)
        '''
        if not isinstance(move, int):
            raise TypeError("move must be of type int")

        if move < 0 or move >= self.size ** 2:
            raise ValueError("move must be within the range of [0, self.size ** 2)")


        return True
#
#
#
    def get_game_state(self, to_print = False):
        '''
        Method -- get_game_state
            to testing debug and print dictionary to console, row by row
            to visualize without turtle module
            a getter for game_state up-to-date dictionary
        Parameter:
            to_print: a boolean, True prints the game_state, False skips printing
        return:
            a dictionary of current game_state
        Possible Error raised:
            TypeError: to_print must be of type bool
        '''
        if not isinstance(to_print, bool):
            raise TypeError("to_print must be of type bool")


        if to_print:
            print()
            for key, value in self.game_state.items():
                print(value, end = " ")
                if key % self.size == self.size - 1:
                    print()
            print()

        return self.game_state
#
#
#
    def get_game_board_size(self):
        '''
        Method -- get_game_board_size:
            a getter for size attribute
        Parameter:
            none
        Return:
            int of size attritube class instantiated
        Posible Error raise:
            none
        '''
        return self.size
#
#
#
    def update_game_state(self, move):
        '''
        Method -- update_game_state:
            call get_possible_flip method to get a dictionary of all possible flips based on input, print invalid message if no flipping found
            store value in singleton class for graphics
            switch current players and opponent
        Parameter:
            move: 1D address of tile
        Return:
            gives result of move by trigger the self.check_winner function, either:
            CONTINUE: the game has not ended, continue to play
            BLACK: the game has ended both players not able to make any more moves, and black has the most piece count
            WHITE: the game has ended both players not able to make any more moves, and white has the most piece count
            TIE: the game has ended both players not able to make any more moves, and both players has equal counts
        Possible Error raised:
            Error raised by self.is_valid_move
        '''
        if self.is_valid_move(move):

            tiles_to_flip = self.get_possible_flips(move)
            if len(tiles_to_flip) > 0:
            # Got opponents to flip
                # first flip the original slot move
                self.game_state[move] = self.current_player_to_move
                for slots_to_flip in tiles_to_flip.values():
                    for slot_to_flip in slots_to_flip:
                        self.game_state[slot_to_flip] = self.current_player_to_move

                if not self.is_tree_search:
                # populate the finalized tiles to flip for grpahics
                # the original clicked position to be inserted in front of a flattened list to flip first in turtle for natural animation
                    self.final_tiles_to_flip.append(move)
                    self.final_tiles_to_flip.extend(self.flatten_dictionary_values_lists(tiles_to_flip))
                    self.record_graphic_tiles_to_flip()
        
                    self.final_tiles_to_flip = list()

                self.update_current_player() 

            else:
                # Do nothing in case there are invalid moves
                # print("Invalid move, a move must flip at least one opponent piece.") 
                pass

            # Return this all the way back to place_move return value
            return self.check_winner()
#
#
#   
    def record_graphic_tiles_to_flip(self):
        '''
        Method -- record_graphic_tiles_to_flip:
            store the piece flipped to singleton for DisplayTurtleGame class instance and draw
        Parameters, Returns, Possible Error raised:
            none
        '''
        record_tile_index_changed(self.final_tiles_to_flip)
        record_player(self.current_player_to_move)
#
#
#
    def is_no_legal_moves(self):
        '''
        Method -- is_no_legal_moves
            Check if there is no legal move, even when the board is not full
            Loop through the board [0, self.game_board_size ** 2) and call self.get_possible_flip 
            for all tiles on board to see if it returns an possible move dictionary with content, or an empty dictionary
            will always return False
        Parameter:
            none
        Return:
            boolean:
                True if looped through all tile's get_possible_flip and all returns an empty dictionary
                False if at least one coordinate's get_possible_flip function return's a non-empty dictionary
        Possible Error raised:
            none
        '''
        for coordinate in self.game_state.keys():
            if len(self.get_possible_flips(coordinate)) > 0:
                # If the self.get_possible_flip returns value moves, return False
                return False
        return True  
#
#
#
    def is_game_board_full(self):
        '''
        Method -- is_game_board_full
            Check if the gameboard is full by checking if there is empty "e" in the board
        Parameter:
            none
        Return:
            a boolean denoting the existence of "e"
        Possible Error raise:   
            none
        '''
        return "e" not in set(self.game_state.values())
#
#
#
    def check_winner(self):
        '''
        Method -- get_winner
            check and return the winner in case the game ends, populate self.result_count, 
            reset self.result_count if no winner found
        Parameter:
            none
        Return:
            return WHITE: if white won
            return BLACK: if black won
            reutrn TIE: if the game ends in a tie
            return CONTINUE: if there is no winner and the game as to continue
        Possible Error raised:
            none
        '''
        if self.is_game_board_full() or self.is_no_legal_moves():
            # Indeed the game ends, find result
            for player in self.game_state.values():
                if player == "w":
                    self.result_count["w"] += 1
                elif player == "b":
                    self.result_count["b"] += 1

            max_count = max(self.result_count.values())
            winner = ""
            
            if self.result_count["w"] == max_count and self.result_count["b"] == max_count:
                return "TIE"
            elif self.result_count["w"] == max_count:
                return "WHITE"
            elif self.result_count["b"]:
                return "BLACK"

        else:
            self.result_count = {"w": 0, "b": 0}
            if not self.is_tree_search:
                print(f"{self.get_current_player()}'s move") 

            return "CONTINUE"
#
#
#
    def calculate_four_board_center_slots(self):
        '''
        Method -- calculate_four_board_center_slots
            calculate the four slots in the center for initialization during instantiation
        Parameters:
            none
        Return:
            a list in 1D addressing the 4 center slots to where 2"w" and 2"b" are to be placed
        Possible Error raise:
            none
        '''
        if not isinstance(self.size, int):
            raise TypeError("game_board_size must be of type int")
        
        if self.size < 0 or self.size % 2 != 0:
            raise ValueError("game_board_size must be a positive even whole number")

        # Nothing to initizlie in case size of game_board is 0
        if self.size == 0:
            return list()


        int_to_record = [(self.size - 2) / 2, self.size / 2]
        center_slots = []

        for column in range(self.size):
            for row in range(self.size):
                # if the row or column is the middle two of row and middle of column
                if row in int_to_record and column in int_to_record:
                    # append according to row
                    center_slots.append(row + column * self.size)
        
        return center_slots
#
#
#
    def update_current_player(self):
        '''
        Method -- update_current_player
            to update current player and opponent by switching, either from "w" to "b" or otherwise
        Parameters:
            none
        Return:
            none
        Possible Error raise:
            none
        '''
        if self.current_player_to_move == "w":
            self.current_player_to_move = "b"
            self.opponent = "w"
        else:
            self.current_player_to_move = "w"
            self.opponent = "b"
            
#
#
#
    def get_all_possible_moves(self, to_print = False):
        '''
        Method -- get_all_possible_moves:
            Populate all possible moves given current board situation
        Parameters:
            to_print: True if debugging
        Return:
            a dictionary containing key (possible moves), and value (flips on opponents resulting key move)
        Possible Error raisedL
            to_print must be of type bool
        '''
        if not isinstance(to_print, bool):
            raise TypeError("to_print must be of type bool")


        possible_moves = {}
        for coordinate in self.game_state.keys():
            flip_dictionary = self.get_possible_flips(coordinate)
            if len(flip_dictionary) > 0:
                possible_moves[coordinate] = self.flatten_dictionary_values_lists(flip_dictionary)
        
        if to_print: 
            print(possible_moves)

        return possible_moves 
#
#
#       
    def look_up_direction(self, coordinate_to_check, direction_to_check, first_lookup):
        '''
        Method -- look_up_direction
            Recursively call itself to populate self.temp_direction until reach -1 (invalid move) or any valid non-negative number
            calls self.check_edge_of_board_for_neighbors to check if it is an edge case and we are detecting left or right move, invalid move if at either edge
            populate self.temp_direction
        Parameter:
            coordinate_to_check: the coordinate for checking while traversing the board's 8 directions
            direction_to_check: an int containing the direction to move, of one of the 8 directions to traverse the board
        Return:
            none, just poplate self.temp_direction
        Possible Error raise:
            Error raised by self.is_valid_move
            ValueError: direction_to_check must be one of the 8 direction contained in self.move_control.values()
            TypeError: first_lookup must be of type bool
        '''
        if direction_to_check not in self.move_control.values():
            raise ValueError("direction_to_check must be a description of one of the eight direction listed in the key of self.move_control")

        if not isinstance(first_lookup, bool):
            raise TypeError("first_lookup must be of type bool")


        if self.is_valid_move(coordinate_to_check):

            projected_coordinate = self.check_edge_of_board_for_neighbors(coordinate_to_check, direction_to_check)
            
            # check for right or left edge right and left move projections (-1), or if the projected tile makes index out of bound
            if (projected_coordinate >= self.size ** 2) or (projected_coordinate < 0):
                return self.temp_direction.append(-1)

            # if the move has an opponent as a neighour, possible valid move regardless of first move or not, explore if so
            # new coordinate to start exploring is the projecfted coordinate
            if self.game_state[projected_coordinate] == self.opponent:
                self.temp_direction.append(projected_coordinate)
                return self.look_up_direction(projected_coordinate, direction_to_check, first_lookup = False)

            if first_lookup:
                # Base case of lookup recurrsion
                if self.game_state[projected_coordinate] == self.current_player_to_move or self.game_state[projected_coordinate] == "e":
                    # Check if friend piece or empty next to the slot for the first move, invalid direction if so
                    return self.temp_direction.append(-1)

            else:
                # base case of lookup recurrsion in case the project met a friend piece of same color, lookup list is valid
                if self.game_state[projected_coordinate] == self.current_player_to_move:
                    # End of recurrsion if there is a friend piece after sandwiching opponent
                    return self.temp_direction.append(projected_coordinate)

                # Base case of lookup recurrsion in case the project ends in empty piece 'e', invalid
                elif self.game_state[projected_coordinate] == "e":
                    return self.temp_direction.append(-1)      
#
#
#
    def check_edge_of_board_for_neighbors(self, coordinate_to_check, direction_to_check):
        '''
        Method -- check_edge_of_board_for_neighbors
            Check if the edge is reached in since this class process 1D spot only, need to be converted into 2D for checking
            if at the left edge and direction_to_check contains left component, return -1 denoting invalid direction_to_check
            similar case for right edhe and right component moves
        Parameters:
            coordinate_to_check: the coordinate for checking while traversing the board's 8 directions
            direction_to_check: an int containing the direction to move, of one of the 8 directions to traverse the board
        Return:
            either:
                -1: when at edge and the direction moves out of game_board
                summation of current coordinate and the project direction_to_check for traversal if the direction to explore is valid not out of bounds
        Possible Error raise:
            Error raised by self.is_valid_move
            ValueError: direction_to_check must be one of the 8 direction contained in self.move_control.values()
            >>> ??? <<<
        '''
        if self.is_valid_move(coordinate_to_check):

            if direction_to_check not in self.move_control.values():
                raise ValueError("direction_to_check must be a description of one of the eight direction listed in the key of self.move_control")


            moves_not_allowed_at_right_edge = ["right", "upper_right", "lower_right"]
            moves_not_allowed_at_left_edge = ["left", "upper_left", "lower_left"]

            # when it is at the right edge, cannot look for moves with any right movement compoenent
            if coordinate_to_check % self.size == self.size - 1:
                for right_move in moves_not_allowed_at_right_edge:
                    if self.move_control[right_move] == direction_to_check:
                        return -1

            # when it is at the left edge, cannot look for moves with any left movement compoenent
            if coordinate_to_check % self.size == 0:
                for left_move in moves_not_allowed_at_left_edge:
                    if self.move_control[left_move] == direction_to_check:
                        return -1

            return coordinate_to_check + direction_to_check
#
#
#
    def get_possible_flips(self, coordinate_to_check):
        '''
        Method -- get_possible_flips
            call self.look_up_direction to populate the self.temp_direction list with for loop looping through self.move_control traversing all 8 directions
            check if list return ends with -1, which means the entire list is invalid, no appending to all possible flips if so
            if it ends with a non-negative number, it means the move in that particular direction is valid
            append direction as key, the list of tile index it went through as values, while list of temp_direction to be flipped
        Parameter:
            coordinate_to_check: int of 1D address
        Return:
            a dictionary recording the key, value pair od all possible flips
            key: the direction of valid move, a string
            value: a list of flips to be made by current player's move, whole list will be deemed valid if it ends with not -1
                note that the value list does not contain the original move played
            i.e. for a game_board n = 8, original move = 17, all_possible_flip = {
                "down": [25, 33, 41] # valid, to be flipped by self.update_game_state_if_check_rule
                ....
                "right": [18, 19, 20, 21, -1] # invalid
                .... continue for all 8 directions
            }
        Possible Error raise:
            Error raised by self.is_valid_move
        '''
        if self.is_valid_move(coordinate_to_check):

            all_possible_flips = dict()
            for direction, direction_to_check in self.move_control.items():
                if self.game_state[coordinate_to_check] == "e": 
                    # Check if the move is on an occupied slot in all 8 directions
                    # Recursively loopup and extend along all 8 and get a list on that direction
                    # Bind it all together in all_possible_flip dictionary
                    self.look_up_direction(coordinate_to_check, direction_to_check, first_lookup = True)
                    # list ending with -1 means a friendly piece is not found, no flipping along that list
                    if self.temp_direction[-1] != -1: 
                        all_possible_flips[direction] = self.temp_direction
                    self.temp_direction = []

            return all_possible_flips
#        
#
#
    def flatten_dictionary_values_lists(self, dictionary):
        '''
        Method -- flatten_dictionary_values:
            This functions flattens the dictionary value (list of int or int) into 1D list
        Parameters:
            dictionary: a dictionary to flatten    
        Returns:
            a 1D list, flattened and joined
        Possible Error raise:
            if the values of dictionary is not of type list, or dictionary is not of type dictionary
        '''
        if not isinstance(dictionary, dict):
            raise TypeError("dictionary must be of type dict")

        for value in dictionary.values():
            if not isinstance(value, list) and not isinstance(value, int):
                raise TypeError("all values in dictionary's value must be of type list containing int, or pure int")

        flattened_list = list()
        for value in dictionary.values():
            if isinstance(value, list):
                flattened_list += value
            else:
                flattened_list.append(value)
        
        return flattened_list
#
#
#
    def get_current_player(self):        
        '''
        Method -- get_current_player:
            just a getter for current player
        Parameters, Possible Error raise:
            none
        Returns:
            returns a string, the the conversion and complete color of self.current_player
        '''
        return self.color_conversion[self.current_player_to_move]
#
#
#
    def get_result_count(self):        
        '''
        Method -- get_result_count:
            just a getting of result_count attritube
        Parameters, Possible Error raise:
            none
        Returns:
            returns a dictionary of self.result_count for 'w' and 'b' as key ,
            and nos. of pieces on screen as values
        '''
        return self.result_count
#
#
#
    def get_color_conversion(self):        
        '''
        Method -- get_color_conversion:
            just a getting for dictionary of color_conversion
        Parameters, Possible Error raise:
            none
        Returns:
            returns a dictionary, for 'w' = ? abd 'b' = ?
        '''
        return self.color_conversion

