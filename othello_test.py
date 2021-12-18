
import unittest, os
from unittest.case import expectedFailure

from GameEngine import *
from GameBoard import *
from StoreTileChanged import *
from Piece import *
from Othello_AI import *
from Tile import *

class testGameEngine(unittest.TestCase):
# 
# Testing the __init__ method
    def test_init_with_valid_input_1_with_default(self):
        game = GameEngine(8)
        self.assertEqual(game, GameEngine(8))
        self.assertEqual(game.to_draw, False)
        self.assertEqual(game.start_color, "b")
        self.assertEqual(game.game_board, GameBoard(8, "b"))
    

    def test_init_with_valid_input_2_with_default(self):
        game = GameEngine(2)
        self.assertEqual(game, GameEngine(2))
    

    # Should raise Error in __init__ class
    def test_init_with_positive_game_board_size_as_string(self):
        with self.assertRaises(TypeError):
            game = GameEngine("8")


    def test_init_with_positive_odd_game_board_size(self):
        with self.assertRaises(ValueError):
            game = GameEngine(5)


    def test_init_with_positive_game_board_size_smaller_than_0(self):
        with self.assertRaises(ValueError):
            game = GameEngine(-1)


    def test_init_with_positive_game_board_size_as_float(self):
        with self.assertRaises(TypeError):
            game = GameEngine(8.5)
    

    def test_init_with_positive_game_board_size_as_float_from_fraction(self):
        # Python treats 8/4 as float even it should return an int, user to convert to int before class instantiation
        with self.assertRaises(TypeError):
            game = GameEngine(8/2)


    def test_init_with_to_draw_not_bool(self):
        with self.assertRaises(TypeError):
            game = GameEngine(4, to_draw = 4)
        with self.assertRaises(TypeError):
            game = GameEngine(4, to_draw = "e")
    #
    #
# Testing the __eq__ method
    def test_eq_with_valid_GameEngine_classes_True(self):
        game_1 = GameEngine(4)
        game_2 = GameEngine(4)
        self.assertTrue(game_1 == game_2)


    def test_eq_with_non_GameEngine_class_instance_False(self):
        game_1 = GameEngine(8)
        game_2 = "game_2"
        self.assertFalse(game_1 == game_2)   


    def test_eq_with_altered_game_board(self):
        # __eq__ compares not only the __str__ of instances,
        # but its state of all elements, move on slot 19 is effective and thus boards are not equal
        game_1 = GameEngine(8)
        game_2 = GameEngine(8)
        game_2.place_move(3, 2)
        self.assertFalse(game_1 == game_2) 
    #
    #
# Testing the __str__ method
    def test_str_with_valid_GameEngine_classes_with_default_player(self):
        game = GameEngine(8)
        self.assertEqual(str(game), "A Game Engine of Othello with size 8 by 8.")
    #
    #
# Testing the GameBoard initialization  
    def test_game_initialization_size_4(self):
        game_1 = GameEngine(4)
        game_2 = GameEngine(4)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        self.assertEqual(game_1, game_2)
        

    def test_game_state_initialization_with_size_4_set_game_state(self):
        game = GameEngine(4)
        game_expected_game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        self.assertEqual(game.game_board.get_game_state(), game_expected_game_state)


    def test_game_state_initialization_with_size_8(self):
        game = GameEngine(8)
        game_expected_game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game.game_board.get_game_state(), game_expected_game_state)


    def test_game_state_initialization_with_size_2(self):
        game = GameEngine(2)
        game_expected_game_state = {
             0: 'w',  1: 'b', 
             2: 'b',  3: 'w',
        }
        self.assertEqual(game.game_board.get_game_state(), game_expected_game_state)


    def test_game_state_initialization_with_size_0(self):
        game = GameEngine(0)
        game_expected_game_state = dict()
        self.assertEqual(game.game_board.get_game_state(), game_expected_game_state)
    #
    #
# Testing the place_move and place_move_1D_function with invalid move or wrong input
    def test_place_move_test_invalid_move_return_same_game_board(self):
        game_1 = GameEngine(4)
        game_1.place_move(1, 2) # invalid move by black since (1, 2) is occupied
        game_2 = GameEngine(4)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }  
        # game_1 and game_2 should be identitcal after invalid first move
        self.assertEqual(game_1, game_2)     


    def test_place_move_ineffective_move_according_to_rule(self):
        game_1 = GameEngine(8)
        game_2 = GameEngine(8)
        game_2.place_move(0, 0) # game_2 makes an ineffective move
        # move at slot (0, 0) should be invalid since no flipped is allowed
        self.assertEqual(game_1, game_2)


    def test_place_move_1D_ineffective_move_according_to_rule(self):
        game_1 = GameEngine(8)
        game_2 = GameEngine(8)
        game_2.place_move_1D(0)
        self.assertEqual(game_1, game_2)


    def test_place_move_invalid_negative_move(self):
        # Both move_x and move_y should be [0, 4) excluding 4 = self.game_board_size
        game = GameEngine(4)
        with self.assertRaises(ValueError):
            game.place_move(-1, 2)
        with self.assertRaises(ValueError):
            game.place_move(2, -2)


    def test_place_move_1D_invalid_negative_or_out_of_bounds_move(self):
        game = GameEngine(4)
        with self.assertRaises(ValueError):
            game.place_move_1D(-2)


    def test_place_move_invalid_move_is_str(self):
        # Both move_x and move_y should be of type int
        game = GameEngine(4)
        with self.assertRaises(TypeError):
            game.place_move(-1, "2")
        with self.assertRaises(TypeError):
            game.place_move("2", -2)


    def test_place_move_1D_invalid_move_is_str(self):
        # Both move_x and move_y should be of type int
        game = GameEngine(4)
        with self.assertRaises(TypeError):
            game.place_move_1D("19")
        with self.assertRaises(TypeError):
            game.place_move_1D(list())


    def test_place_move_invalid_larger_than_board_size(self):
        game = GameEngine(8)
        # Both move_x and move_yshould be [0, 8), excluding number >= 8 = self.game_board_size
        with self.assertRaises(ValueError):
            game.place_move(8, 3)
        with self.assertRaises(ValueError):
            game.place_move(3, 10)


    def test_place_move_1D_invalid_larger_than_board_size(self):
        game = GameEngine(6)
        with self.assertRaises(ValueError):
            game.place_move_1D(36)
# Testing the place_move and place_move_1D_function with flipping
    # Testing different flips results from the model recursive calculations
    # Including normal flips, wipe out, ties
    def test_place_move_normal_flip(self):

        game_1 = GameEngine(8)
        game_1.place_move(3, 2) # b's move
        game_1.place_move(2, 2) # w's move
        game_1.place_move(2, 3) # b's move
        game_1.place_move(2, 4) # w's move

        game_2 = GameEngine(8)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'w', 19: 'b', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'w', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'w', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        # After 4 moves for game, it should have the same state as game_1
        self.assertEqual(game_1, game_2)

    
    def test_place_move_normal_flip_with_edge(self):
        game_1 = GameEngine(8)
        game_1.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'b',  5: 'w',  6: 'w',  7: 'e',
             8: 'w',  9: 'w', 10: 'b', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'w', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        # should continue after flipping at edge cases, the second roll should not flip,
        # but only first roll does, and no winner
        self.assertEqual(game_1.place_move(7, 0), "CONTINUE")

        game_2 = GameEngine(8)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'b',  5: 'b',  6: 'b',  7: 'b',
             8: 'w',  9: 'w', 10: 'b', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'w', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        # Not equal since its different player's turn for game_1 and game_2
        self.assertFalse(game_1 == game_2)
        # purely comparing game_1 and game_2's game_state should yield equality
        self.assertEqual(game_1.game_board.get_game_state(), game_2.game_board.get_game_state())


    def test_place_move_game_end_with_black_wins_with_wipeout(self):
        game_1 = GameEngine(game_board_size = 8)
        game_1.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'b', 26: 'w', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'w', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'b', 43: 'e', 44: 'w', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'b', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game_1.place_move(4, 3), "BLACK")
        
        # resultant move from (4, 3) by black at game_1
        game_2 = GameEngine(game_board_size = 8)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'b', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'b', 43: 'e', 44: 'b', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'b', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        # Not equal since its different player's turn for game_1 and game_2
        self.assertFalse(game_1 == game_2)
        # purely comparing game_1 and game_2's game_state should yield equality
        self.assertEqual(game_1.game_board.get_game_state(), game_2.game_board.get_game_state())


    def test_place_move_game_end_with_white_wins_with_wipeout(self):
        # Just this time, the game starts with white since wipeout for white would be tested
        game_1 = GameEngine(game_board_size = 8)
        # manual altering the player to move for wipeout in controlled environment
        game_1.game_board.current_player_to_move = "w"
        game_1.game_board.opponent = "b" # need to force change the opponent as well
        game_1.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'b', 10: 'b', 11: 'b', 12: 'b', 13: 'b', 14: 'b', 15: 'w',
            16: 'b', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'b', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'b', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'b', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'b', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'w', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game_1.place_move(0, 1), "WHITE")
        
        # resultant move from (0, 1) by white at game_1
        # Two games are equal if and only if the game_state and the starting move is equal
        game_2 = GameEngine(game_board_size = 8)
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'w',  9: 'w', 10: 'w', 11: 'w', 12: 'w', 13: 'w', 14: 'w', 15: 'w',
            16: 'w', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'w', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'w', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'w', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'w', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'w', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        # After white player's force turn, becomes "b" turn and with same game_state
        self.assertTrue(game_1 == game_2)
        # purely comparing game_1 and game_2's game_state should yield equality
        self.assertEqual(game_1.game_board.get_game_state(), game_2.game_board.get_game_state())


    def test_place_move_game_end_with_tie_without_full_board(self):
        # No legal moves on board, with white and black each occupying 22 slots
        game_1 = GameEngine(game_board_size = 8)
        game_1.game_board.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        # should not be able to place, return a tie without full board
        self.assertEqual(game_1.place_move(7, 0), "TIE")
        
        game_2 = GameEngine(game_board_size = 8)
        game_2.game_board.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        self.assertEqual(game_1, game_2)
        

    def test_place_move_game_end_with_white_wins_with_full_board(self):
        # white wins with one extra "w" on 7th slot
        game_1 = GameEngine(game_board_size = 8)
        game_1.game_board.game_state = {
             0: 'w',  1: 'b',  2: 'w',  3: 'b',  4: 'w',  5: 'b',  6: 'w',  7: 'w',
             8: 'w',  9: 'b', 10: 'w', 11: 'b', 12: 'w', 13: 'b', 14: 'w', 15: 'b',
            16: 'w', 17: 'b', 18: 'w', 19: 'b', 20: 'w', 21: 'b', 22: 'w', 23: 'b', 
            24: 'w', 25: 'b', 26: 'w', 27: 'b', 28: 'w', 29: 'b', 30: 'w', 31: 'b', 
            32: 'w', 33: 'b', 34: 'w', 35: 'b', 36: 'w', 37: 'b', 38: 'w', 39: 'b', 
            40: 'w', 41: 'b', 42: 'w', 43: 'b', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'b', 50: 'w', 51: 'b', 52: 'w', 53: 'b', 54: 'w', 55: 'b', 
            56: 'w', 57: 'b', 58: 'w', 59: 'b', 60: 'w', 61: 'b', 62: 'w', 63: 'b',
        }
        # should not be able to place
        self.assertEqual(game_1.place_move(0, 0), "WHITE")
        
        game_2 = GameEngine(game_board_size = 8)
        game_2.game_board.game_state = {
             0: 'w',  1: 'b',  2: 'w',  3: 'b',  4: 'w',  5: 'b',  6: 'w',  7: 'w',
             8: 'w',  9: 'b', 10: 'w', 11: 'b', 12: 'w', 13: 'b', 14: 'w', 15: 'b',
            16: 'w', 17: 'b', 18: 'w', 19: 'b', 20: 'w', 21: 'b', 22: 'w', 23: 'b', 
            24: 'w', 25: 'b', 26: 'w', 27: 'b', 28: 'w', 29: 'b', 30: 'w', 31: 'b', 
            32: 'w', 33: 'b', 34: 'w', 35: 'b', 36: 'w', 37: 'b', 38: 'w', 39: 'b', 
            40: 'w', 41: 'b', 42: 'w', 43: 'b', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'b', 50: 'w', 51: 'b', 52: 'w', 53: 'b', 54: 'w', 55: 'b', 
            56: 'w', 57: 'b', 58: 'w', 59: 'b', 60: 'w', 61: 'b', 62: 'w', 63: 'b',
        }
        self.assertEqual(game_1, game_2)
    #
    #
# Testing the place_move and place_move_1D linkage
    def test_place_move_place_move_1D_linkage_if_get_same_state(self):
        game_1 = GameEngine(game_board_size = 8)
        game_1.game_board.current_player_to_move = "w"
        game_1.game_board.opponent = "b"
        game_1.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'b', 10: 'b', 11: 'b', 12: 'b', 13: 'b', 14: 'b', 15: 'w',
            16: 'b', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'b', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'b', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'b', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'b', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'w', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game_1.place_move(0, 1), "WHITE")

        game_2 = GameEngine(game_board_size = 8)
        game_2.game_board.current_player_to_move = "w"
        game_2.game_board.opponent = "b"
        game_2.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'b', 10: 'b', 11: 'b', 12: 'b', 13: 'b', 14: 'b', 15: 'w',
            16: 'b', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'b', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'b', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'b', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'b', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'w', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game_2.place_move_1D(8), "WHITE")
        
        game_3 = GameEngine(game_board_size = 8)
        game_3.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'w',  9: 'w', 10: 'w', 11: 'w', 12: 'w', 13: 'w', 14: 'w', 15: 'w',
            16: 'w', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'w', 25: 'e', 26: 'e', 27: 'e', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'w', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'w', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'w', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'w', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        
        # After force white move, move back to "b" with same game_state
        self.assertTrue(game_1 == game_3)
        # purely comparing game_1 and game_2's game_state should yield equality

        # After force white move, move back to "b" with same game_state
        self.assertTrue(game_2 == game_3)
        # purely comparing game_1 and game_2's game_state should yield equality
        self.assertEqual(game_2.game_board.get_game_state(), game_3.game_board.get_game_state())
    #
    #
# Testing the pass_move_into_model_and_check_winner_tile_index_TypeError_function error
    def test_pass_move_into_model_and_check_winner_tile_index_TypeError(self):
        game = GameEngine(game_board_size = 4)
        with self.assertRaises(TypeError):
            game.pass_move_into_model_and_check_winner(1.2)
        with self.assertRaises(TypeError):
            game.pass_move_into_model_and_check_winner("1")


    def test_pass_pass_move_into_model_and_check_winner_tile_index_ValueError(self):
        game = GameEngine(game_board_size = 4)
        with self.assertRaises(ValueError):
            game.pass_move_into_model_and_check_winner(-1)
        with self.assertRaises(ValueError):
            game.pass_move_into_model_and_check_winner(16)
    #
    #
# Testing the call_AI_move
        game = GameEngine(game_board_size = 8)
        game.game_board = GameBoard(8, "w")
        game.game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'w', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'b', 36: 'b', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'b', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'w', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        game.call_AI_move()

        # move 37 is expected to be made
        expected_game_board = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'w', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'w', 36: 'w', 37: 'w', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'b', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'w', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game.game_board.get_game_state(), expected_game_board)
    #
    #
# Testing the save_score_to_file, read through the saved file and see if getting desired result
    def test_save_score_to_file_insert_at_the_end(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8\n"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        game.save_score_to_file("Jacky", 9, insert_front = False, filename = "testing_score.txt")

        with open("testing_score.txt", "r") as file:
            file_content = file.read()
            self.assertEqual(file_content, "Peter 10\nVanessa 8\nJacky 9\n")
        os.remove("testing_score.txt")


    def test_save_score_to_file_insert_at_the_front(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8\n"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        game.save_score_to_file("Jacky", 11, insert_front = True, filename = "testing_score.txt")

        with open("testing_score.txt", "r") as file:
            file_content = file.read()
            self.assertEqual(file_content, "Jacky 11\nPeter 10\nVanessa 8\n")
        os.remove("testing_score.txt")


    def test_save_score_to_file_insert_at_back_without_newline(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        game.save_score_to_file("Jacky", 9, insert_front = False, filename = "testing_score.txt")

        with open("testing_score.txt", "r") as file:
            file_content = file.read()
            self.assertEqual(file_content, "Peter 10\nVanessa 8\nJacky 9\n")
        os.remove("testing_score.txt")


    def test_save_score_to_file_insert_at_front_without_newline(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        game.save_score_to_file("Jacky", 11, insert_front = True, filename = "testing_score.txt")

        with open("testing_score.txt", "r") as file:
            file_content = file.read()
            # No new line added at the back if originally \n was missed
            self.assertEqual(file_content, "Jacky 11\nPeter 10\nVanessa 8")
        os.remove("testing_score.txt")


    def test_save_score_to_file_insert_at_the_front_error(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8\n"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        with self.assertRaises(ValueError):
            # Raises ValueError since Jacky's score is greater than max in file, 10, insert_front must be True
            game.save_score_to_file("Jacky", 11, insert_front = False, filename = "testing_score.txt")
        
        with self.assertRaises(ValueError):
            # Raises ValueError since Jacky's score is smaller than max in file, 10, insert_front must be False
            game.save_score_to_file("Jacky", 8, insert_front = True, filename = "testing_score.txt")
        
        with self.assertRaises(ValueError):
            # Raises ValueError since Jacky's score is equal to the max in file, 10, insert_front must be False in case two equally large score are compared
            game.save_score_to_file("Jacky", 10, insert_front = True, filename = "testing_score.txt")
        
        with self.assertRaises(TypeError):
            game.save_score_to_file(5, 11, insert_front = True, filename = "testing_score.txt")
        
        with self.assertRaises(TypeError):
            game.save_score_to_file("Jacky", 11.1, insert_front = True, filename = "testing_score.txt")
        
        with self.assertRaises(TypeError):
            game.save_score_to_file("Jacky", 11, insert_front = 1, filename = "testing_score.txt")
        os.remove("testing_score.txt")
    #
    #
# Testing the get_max_score_from_file, read through the saved file and see if getting desired result
    def test_get_max_score_from_file_normal_file(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8\nJacky 9\n"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write(original_content)

        self.assertEqual(game.get_max_score_from_file("testing_score.txt"), 10)
        os.remove("testing_score.txt")

    def test_get_max_score_from_file_empty_file(self):
        game = GameEngine(game_board_size = 4)
        original_content = "Peter 10\nVanessa 8\nJacky 9\n"
        # create an empty file and write something onto it
        with open("testing_score.txt", "w") as file:
            file.write("")

        self.assertEqual(game.get_max_score_from_file("testing_score.txt"), 0)
        os.remove("testing_score.txt")
#
#
#
class testGameBoard(unittest.TestCase):
#
# Testing the __init__ method   
    def test_init_normal_setup_size_8_start_black(self):
        game_board = GameBoard(8, "b")
        expected_move_control = {
            "down": 8,
            "up": -8,
            "left": -1,
            "right": 1,
            "lower_right": 9,
            "lower_left": 7,
            "upper_right": -7,
            "upper_left": -9,
        }
        self.assertEqual(game_board.move_control, expected_move_control)
        self.assertEqual(game_board.size, 8)
        self.assertEqual(game_board.current_player_to_move, "b")
        self.assertEqual(game_board.opponent, "w")
        self.assertFalse(game_board.is_tree_search)


    def test_init_normal_setup_size_4_start_white(self):
        game_board = GameBoard(4, "w")
        expected_move_control = {
            "down": 4,
            "up": -4,
            "left": -1,
            "right": 1,
            "lower_right": 5,
            "lower_left": 3,
            "upper_right": -3,
            "upper_left": -5,
        }
        self.assertEqual(game_board.move_control, expected_move_control)
        self.assertEqual(game_board.size, 4)
        self.assertEqual(game_board.current_player_to_move, "w")
        self.assertEqual(game_board.opponent, "b")


    def test_init_setup_error_size_not_int(self):
        with self.assertRaises(TypeError):
            game_board = GameBoard(3.5, "b")
        with self.assertRaises(TypeError):
            game_board = GameBoard("4", "b")


    def test_init_setup_error_size_out_of_bounds_or_odd(self):
        with self.assertRaises(ValueError):
            game_board = GameBoard(-1, "b")
        with self.assertRaises(ValueError):
            game_board = GameBoard(3, "b")


    def test_init_setup_error_starting_player_to_move_not_w_or_b(self):
        with self.assertRaises(ValueError):
            game_board = GameBoard(4, "e")
        with self.assertRaises(ValueError):
            game_board = GameBoard(8, "3")
    #
    #
# Testing the __eq__ method 
    def test_eq_with_valid_GameBoard_normal(self):
        game_board = GameBoard(4, "b")
        self.assertTrue(game_board == GameBoard(4, "b"))


    def test_eq_with_other_not_gameboard_class(self):
        game_board_1 = GameBoard(4, "b")
        self.assertFalse(game_board_1 == GameEngine(4))
        game_board_2 = GameBoard(4, "b")
        self.assertFalse(game_board_2 == dict())


    def test_eq_with_different_starting_player(self):
        game_board = GameBoard(8, "b")
        self.assertFalse(game_board == GameBoard(8, "w"))


    def test_eq_with_different_game_state_after_1_move(self):
        game_board_1 = GameBoard(4, "b")
        game_board_1.update_game_state(1) # valid move only to game_board 1
        game_board_2 = GameBoard(4, "b")

        self.assertFalse(game_board_1 == game_board_2)

        game_board_2.update_game_state(1) # valid move to game_board 2 as well
        self.assertTrue(game_board_1 == game_board_2)


    def test_eq_with_same_game_state_after_ineffective_move(self):
        game_board = GameBoard(4, "b")
        game_board.update_game_state(0) # invalid move
        self.assertTrue(game_board == GameBoard(4, "b"))


    def test_eq_with_different_size(self):
        game_board = GameBoard(4, "b")
        self.assertFalse(game_board == GameBoard(6, "b"))
    #
    #
# Testing the __str__ method 
    def test_str_size_4(self):
        game_board = GameBoard(4, "b")
        self.assertEqual(str(game_board), \
            "A Game Board model of Othello with size 4 by 4 and a current move by player 'b'.")

    def test_str_size_8(self):
        game_board = GameBoard(4, "w")
        self.assertEqual(str(game_board), \
            "A Game Board model of Othello with size 4 by 4 and a current move by player 'w'.")
    #
    #

# Testing the copy_object method 
    def test_copy_object(self):
        game_board = GameBoard(8, "b")
        temp_game_board = game_board.copy_object()
        self.assertEqual(temp_game_board, game_board)
        self.assertEqual(temp_game_board.get_game_state(), game_board.get_game_state())

    
    def test_copy_object_with_move_on_new_board(self):
        game_board = GameBoard(8, "b")
        temp_game_board = game_board.copy_object()
        temp_game_board.update_game_state(19)
        # The temp_game_board's move should not copy to game_board's
        self.assertFalse(temp_game_board == game_board)
        self.assertFalse(temp_game_board.get_game_state() == game_board.get_game_state())
    #
    #
# Testing the init_game method 
    # No parameters and no return, no errors not much to test
    def test_init_game_set_on_initial_game_board(self):
        game_board = GameBoard(4, "b")
        expected_game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        self.assertEqual(game_board.get_game_state(), expected_game_state)
    #
    #
# Testing the is_valid_game_state method
    def test_is_valid_game_state_is_true_but_raise_error_after_illegal_game_state_alterations(self):
        game_board = GameBoard(4, "b")
        self.assertEqual(game_board.is_valid_game_state(), True)

        # game_state must be dict() type
        with self.assertRaises(TypeError):  
            game_board_1 = GameBoard(4, "b")
            game_board_1.game_state = list()
            self.assertNotEqual(game_board_1.is_valid_game_state(), True)

        # game_state's key value must be all int
        with self.assertRaises(TypeError):  
            game_board_2 = GameBoard(4, "b")
            game_board_2.game_state['15'] = 'e'
            self.assertNotEqual(game_board_2.is_valid_game_state(), True)

        # game_state's key value out of bounds
        with self.assertRaises(ValueError):  
            game_board_3 = GameBoard(4, "b")
            game_board_3.game_state[16] = 'w'
            self.assertNotEqual(game_board_3.is_valid_game_state(), True)

        # game_state's key value out of bounds
        with self.assertRaises(ValueError):  
            game_board_4 = GameBoard(4, "b")
            game_board_4.game_state[0] = 'a'
            self.assertNotEqual(game_board_4.is_valid_game_state(), True)

        # game_state's value not 'w', 'b' or 'e'
        with self.assertRaises(ValueError):  
            game_board_5 = GameBoard(4, "b")
            game_board_5.game_state[0] = 'a'
            self.assertNotEqual(game_board_5.is_valid_game_state(), True)

        # game_state's key value not positive even whole number
        with self.assertRaises(ValueError):  
            game_board_6 = GameBoard(4, "b")
            game_board_6.size = 5
            self.assertNotEqual(game_board_6.is_valid_game_state(), True)

        # game_state's size of game_state is incorrect
        with self.assertRaises(ValueError):  
            game_board_7 = GameBoard(8, "b")
            game_board_7.game_state[64] = "w"
            self.assertNotEqual(game_board_7.is_valid_game_state(), True)
    #
    #
# Testing the is_valid_move method
    def test_is_valid_move_is_true_after_game_state_alterations(self):
        game_board = GameBoard(8, "b")
        self.assertTrue(game_board.is_valid_move(0))

        with self.assertRaises(TypeError):
            game_board_1 = GameBoard(8, "b")
            self.assertNotEqual(game_board_1.is_valid_move('8'), True)

        with self.assertRaises(ValueError):
            game_board_1 = GameBoard(8, "b")
            self.assertNotEqual(game_board_1.is_valid_move(64), True)

        with self.assertRaises(ValueError):
            game_board_2 = GameBoard(8, "b")
            self.assertNotEqual(game_board_1.is_valid_move(-1), True)
    #
    #
# Testing the get_game_state method
    def test_get_game_state(self):
        game_board = GameBoard(4, "b")
        self.assertTrue(game_board.is_valid_move(0))
        expected_return = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        self.assertEqual(expected_return, game_board.get_game_state())
    
    def test_get_game_state_error(self):
        with self.assertRaises(TypeError):
            game_board = GameBoard(8, "b")
            game_board.get_game_state(1)
    #
    #
# Testing the get_game_board_size method
    def test_get_game_board_size(self):
        game_board = GameBoard(6, "b")
        self.assertEqual(game_board.get_game_board_size(), 6)
    #
    #
# Testing the updated_game_state method, error_raised by is_valid_move is tested before
    def test_update_game_state_flip_effect_moves_size_8(self):
        game_board_1 = GameBoard(8, "b")
        game_board_1.update_game_state(19) # b's move
        game_board_1.update_game_state(18) # w's move
        game_board_1.update_game_state(26) # b's move
        result = game_board_1.update_game_state(34) # w's move
        self.assertEqual(result, "CONTINUE") # current game_board is black's turn

        game_board_2 = GameBoard(8, "b")
        game_board_2.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'w', 19: 'b', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'w', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'w', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        # After 4 moves for game, it should have the same state as game_board_1
        self.assertEqual(game_board_1, game_board_2)


    def test_update_game_state_flip_effective_flip(self):
        game_board_1 = GameBoard(4, "b")
        result = game_board_1.update_game_state(1) # b's move
        self.assertEqual(result, "CONTINUE")

        game_board_2 = GameBoard(4, "w")
        game_board_2.game_state = {
             0: 'e',  1: 'b',  2: 'e',  3: 'e',
             4: 'e',  5: 'b',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }

        # After 1 move ineffective for game, game_board_1 should be as freshly initialized with white player force to start
        self.assertEqual(game_board_1, game_board_2)


    def test_update_game_state_ineffective_flip(self):
        game_board_1 = GameBoard(4, "b")
        result = game_board_1.update_game_state(0)
        self.assertEqual(result, "CONTINUE")

        game_board_2 = GameBoard(4, "b")
        game_board_2.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        } 


    def test_update_game_state_flip_error_move(self):
        game_board = GameBoard(4, "b")
        with self.assertRaises(ValueError):
            game_board.update_game_state(-1)
        with self.assertRaises(ValueError):
            game_board.update_game_state(16)
        with self.assertRaises(TypeError):
            game_board.update_game_state("-1")
    #
    #
# Testing the record_graphic_tiles_to_flip method
    def test_record_graphic_tiles_to_flip_if_value_is_stored(self):
        game_board = GameBoard(4, "b")
        game_board.final_tiles_to_flip = [1, 5, 9] # simulate a move (0, 1) is placed
        game_board.current_player_to_move = "b"
        game_board.record_graphic_tiles_to_flip()

        self.assertEqual(get_tile_index_changed(), [1, 5, 9])
        self.assertEqual(get_player_played(), "b")
    #
    #
# Testing the is_no_legal_moves method
    def test_is_no_legal_moves_is_true(self):
        # no legal move on both game_board_1 and game_board_2 despite board not full
        game_board_1 = GameBoard(8, "b")
        game_board_1.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        self.assertTrue(game_board_1.is_no_legal_moves())

        game_board_2 = GameBoard(4, "b")
        # set up for a full wipeout
        game_board_2.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'b',  6: 'w',  7: 'e',
             8: 'e',  9: 'w', 10: 'b', 11: 'e', 
            12: 'b', 13: 'e', 14: 'e', 15: 'e', 
        }
        result = game_board_2.update_game_state(3)
        self.assertTrue(game_board_2.is_no_legal_moves())
        self.assertEqual(result, "BLACK")

    
    def test_is_no_legal_moves_is_false(self):
        game_board = GameBoard(4, "b")
        game_board.is_no_legal_moves()
        self.assertFalse(game_board.is_no_legal_moves())
    #
    #
# Testing the is_game_board_full method
    def test_is_game_board_full_is_true(self):
        game_board = GameBoard(8, "b")
        game_board.game_state = {
             0: 'w',  1: 'b',  2: 'w',  3: 'b',  4: 'w',  5: 'b',  6: 'w',  7: 'b',
             8: 'w',  9: 'b', 10: 'w', 11: 'b', 12: 'w', 13: 'b', 14: 'w', 15: 'b',
            16: 'w', 17: 'b', 18: 'w', 19: 'b', 20: 'w', 21: 'b', 22: 'w', 23: 'b', 
            24: 'w', 25: 'b', 26: 'w', 27: 'b', 28: 'w', 29: 'b', 30: 'w', 31: 'b', 
            32: 'w', 33: 'b', 34: 'w', 35: 'b', 36: 'w', 37: 'b', 38: 'w', 39: 'b', 
            40: 'w', 41: 'b', 42: 'w', 43: 'b', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'b', 50: 'w', 51: 'b', 52: 'w', 53: 'b', 54: 'w', 55: 'b', 
            56: 'w', 57: 'b', 58: 'w', 59: 'b', 60: 'w', 61: 'b', 62: 'w', 63: 'b',
        }
        self.assertTrue(game_board.is_game_board_full())
    
    
    def test_is_game_board_full_is_false(self):
        game_board = GameBoard(4, "b")
        self.assertFalse(game_board.is_game_board_full())
    #
    #
# Testing the check_winner method
    def test_check_winner_four_results(self):
        game_board_1 = GameBoard(8, "b")
        # 24 nos. of 'w' and 'b' respectively
        game_board_1.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        self.assertEqual(game_board_1.check_winner(), "TIE")
        self.assertEqual(game_board_1.get_result_count(), {"w": 24, "b": 24})
    
        game_board_2 = GameBoard(4, "b")
        # set up for a full wipeout
        game_board_2.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'b',  6: 'w',  7: 'e',
             8: 'e',  9: 'w', 10: 'b', 11: 'e', 
            12: 'b', 13: 'e', 14: 'e', 15: 'e', 
        }
        result = game_board_2.update_game_state(3)
        # manually initialize result_count since it was populated upon update_game_state return not "CONTINUE"
        game_board_2.result_count = {"w": 0, "b": 0}
        self.assertEqual(game_board_2.check_winner(), "BLACK")
        self.assertEqual(game_board_2.get_result_count(), {"w": 0, "b": 6})
    
        game_board_3 = GameBoard(4, "w")
        # set up for a full wipeout, forced white to play
        game_board_3.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'w', 13: 'e', 14: 'e', 15: 'e', 
        }
        result = game_board_3.update_game_state(3)
        # manually initialize result_count since it was populated upon update_game_state return not "CONTINUE"
        game_board_3.result_count = {"w": 0, "b": 0}
        self.assertEqual(game_board_3.check_winner(), "WHITE")
        self.assertEqual(game_board_3.get_result_count(), {"w": 6, "b": 0})

        game_board_4 = GameBoard(4, "b")
        game_board_4.update_game_state(1)
        self.assertEqual(game_board_4.check_winner(), "CONTINUE")
        self.assertEqual(game_board_4.get_result_count(), {"w": 0, "b": 0})
    #
    #
# Testing the calculate_four_board_center_slots method
    def test_calculate_four_board_center_slots(self):
        game_board_1 = GameBoard(8, "b")
        game_board_2 = GameBoard(6, "b")
        game_board_3 = GameBoard(4, "b")
        game_board_4 = GameBoard(2, "b")
        game_board_5 = GameBoard(0, "b")
        
        self.assertEqual(game_board_1.calculate_four_board_center_slots(), [27, 28, 35, 36])
        self.assertEqual(game_board_2.calculate_four_board_center_slots(), [14, 15, 20, 21])
        self.assertEqual(game_board_3.calculate_four_board_center_slots(), [5, 6, 9, 10])
        self.assertEqual(game_board_4.calculate_four_board_center_slots(), [0, 1, 2, 3])
        self.assertEqual(game_board_5.calculate_four_board_center_slots(), [])
    #
    #
# Testing the update_current_player method
    def test_update_current_player(self):
        game_board = GameBoard(4, "b")
        game_board.update_current_player() # player changed without move placed
        self.assertEqual(game_board.current_player_to_move, "w")
        self.assertEqual(game_board.opponent, "b")
        
        game_board.update_game_state(13) # players switched automatically upon move placed effectively by white
        self.assertEqual(game_board.current_player_to_move, "b")
        self.assertEqual(game_board.opponent, "w")
    #
    #
# Testing the get_all_possible_moves method
    def test_get_all_possible_moves_with_startup_board(self):
        game_board = GameBoard(8, "b")
        expected_legal_move = {19: [27, 35], 26: [27, 28], 37: [36, 35], 44: [36, 28]}
        self.assertEqual(game_board.get_all_possible_moves(), expected_legal_move)


    def test_get_all_possible_moves_with_full_board(self):
        game_board = GameBoard(8, "b")
        game_board.game_state = {
             0: 'w',  1: 'b',  2: 'w',  3: 'b',  4: 'w',  5: 'b',  6: 'w',  7: 'b',
             8: 'w',  9: 'b', 10: 'w', 11: 'b', 12: 'w', 13: 'b', 14: 'w', 15: 'b',
            16: 'w', 17: 'b', 18: 'w', 19: 'b', 20: 'w', 21: 'b', 22: 'w', 23: 'b', 
            24: 'w', 25: 'b', 26: 'w', 27: 'b', 28: 'w', 29: 'b', 30: 'w', 31: 'b', 
            32: 'w', 33: 'b', 34: 'w', 35: 'b', 36: 'w', 37: 'b', 38: 'w', 39: 'b', 
            40: 'w', 41: 'b', 42: 'w', 43: 'b', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'b', 50: 'w', 51: 'b', 52: 'w', 53: 'b', 54: 'w', 55: 'b', 
            56: 'w', 57: 'b', 58: 'w', 59: 'b', 60: 'w', 61: 'b', 62: 'w', 63: 'b',
        }
        # no full board returns an empty dict
        self.assertEqual(game_board.get_all_possible_moves(), dict())

    def test_get_all_possible_moves_with_no_legal_moves_without_full_board(self):
        game_board = GameBoard(8, "b")
        game_board.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        # no legal move returns an empty dict
        self.assertEqual(game_board.get_all_possible_moves(), dict())


    def test_get_all_possible_moves_with_wrong_(self):
        game_board = GameBoard(8, "b")
        with self.assertRaises(TypeError):
            game_board.get_all_possible_moves(1)
    #
    #
# Testing the look_up_direction, the recursive method
    def test_look_up_direction_size_4_direction_down_valid_move(self):
        game_board = GameBoard(4, "b")
        game_board.look_up_direction(1, 4, True) # 1 is the 1D address of tile, 4 is the tiles to add for downward traversal
        self.assertEqual(game_board.temp_direction, [5, 9])

        
    def test_look_up_direction_size_8_direction_up_out_of_bounds_too_small(self):
        game_board = GameBoard(8, "b")
        game_board.look_up_direction(1, -8, True)
        self.assertEqual(game_board.temp_direction, [-1])

        
    def test_look_up_direction_size_8_direction_right_out_of_bounds_too_big(self):
        game_board = GameBoard(8, "b")
        game_board.look_up_direction(63, 1, True)
        self.assertEqual(game_board.temp_direction, [-1])

        
    def test_look_up_direction_size_4_direction_left(self):
        game_board = GameBoard(4, "b")
        game_board.game_state = {
             0: 'e',  1: 'b',  2: 'w',  3: 'w',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        game_board.look_up_direction(4, -1, True) # should not be able to find the discontinued left over the left edge
        self.assertEqual(game_board.temp_direction, [-1])

        
    def test_look_up_direction_size_4_direction_right_lower(self):
        game_board = GameBoard(4, "w")
        game_board.game_state = {
             0: 'e',  1: 'b',  2: 'w',  3: 'w',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        game_board.look_up_direction(4, 5, True) # should not be to get a valid move right lower, will get -1 after one traversal, tile 9
        self.assertEqual(game_board.temp_direction, [9, -1])


    def test_look_up_dircection_size_8_direction_not_valid_traversal(self):
        game_board = GameBoard(8, "w")
        with self.assertRaises(ValueError):
            game_board.look_up_direction(1, 4, True)


    def test_look_up_dircection_size_8_first_lookup_invalid_type(self):
        game_board = GameBoard(8, "w")
        with self.assertRaises(TypeError):
            game_board.look_up_direction(1, 8, 0)

    #
    #
# Testing the check_edge_of_board_for_neighbors, ensure in 1D setting, the search will not continue throught the edge
    def test_check_edge_of_board_for_neighbors_return_without_touching_edge(self):
        game_board = GameBoard(8, "w")
        self.assertEqual(game_board.check_edge_of_board_for_neighbors(5, 1), 6)
        self.assertEqual(game_board.check_edge_of_board_for_neighbors(15, -1), 14) 

    
    def test_check_edge_of_board_for_neighbors_return_negative_return_at_edges(self):
        game_board = GameBoard(8, "w")
        self.assertEqual(game_board.check_edge_of_board_for_neighbors(15, 1), -1) # at right edgem should not be able to explore more right
        self.assertEqual(game_board.check_edge_of_board_for_neighbors(24, -9), -1) # at left edge, should not be able to explore more left


    def test_check_edge_of_board_for_neighbors_return_error_invalid_diection_traversasl(self):
        game_board = GameBoard(8, "w")
        with self.assertRaises(ValueError):
            self.assertEqual(game_board.check_edge_of_board_for_neighbors(4, 2), 6)
    #
    #
# Testing the get_possible_flips method
    def test_get_possible_flips_4_direction_3_possible_direction_flips(self):
        game_board = GameBoard(4, "b")
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'w',  3: 'b',
             4: 'w',  5: 'w',  6: 'w',  7: 'e',
             8: 'e',  9: 'w', 10: 'w', 11: 'b', 
            12: 'e', 13: 'b', 14: 'e', 15: 'e', 
        }
        possible_flips = game_board.get_possible_flips(1) # should not be to get a valid move right lower, will get -1 after one traversal, tile 9
        expected_possible_flip = {
            "right": [2, 3],
            "down": [5, 9, 13],
            "lower_right": [6, 11],
        }
        self.assertEqual(possible_flips, expected_possible_flip)

    
    def test_get_possible_flips_4_direction_no_possible_direction_flips(self):
        game_board = GameBoard(4, "b")
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',
             4: 'e',  5: 'w',  6: 'b',  7: 'e',
             8: 'e',  9: 'b', 10: 'w', 11: 'e', 
            12: 'e', 13: 'e', 14: 'e', 15: 'e', 
        }
        possible_flips = game_board.get_possible_flips(0) # no flip found
        self.assertEqual(possible_flips, dict())

    
    def test_get_possible_flips_4_direction_1_possible_direction_flips_without_crossing_edge(self):
        game_board = GameBoard(4, "b")
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'w',
             4: 'w',  5: 'b',  6: 'w',  7: 'e',
             8: 'e',  9: 'w', 10: 'w', 11: 'b', 
            12: 'e', 13: 'b', 14: 'b', 15: 'e', 
        }
        possible_flips = game_board.get_possible_flips(2) # should not be able to return valid right move, discontinued throught right edge
        expected_possible_flip = {
            "down": [6, 10, 14],
        }
        self.assertEqual(possible_flips, expected_possible_flip)


    def test_get_possible_flips_invalid_coordinate_to_check(self):
        game_board = GameBoard(4, "b")
        with self.assertRaises(TypeError):
            game_board.get_possible_flips("2")

        with self.assertRaises(ValueError):
            game_board.get_possible_flips(16)

        with self.assertRaises(ValueError):
            game_board.get_possible_flips(-1)
    #
    #
# Testing the flatten_dictionary_values
    def test_flatten_dictionary_values_lists_flatten_dictionary(self):
        game_board = GameBoard(4, "b")
        dictionary_1 = {"1": 1, "2": 2, "3": 3}
        self.assertEqual(game_board.flatten_dictionary_values_lists(dictionary_1), [1, 2, 3])

        dictionary_2 = {"1": [1, 2, 3], "2": [4, 5, 6], "3": [7, 8, 9]}
        self.assertEqual(game_board.flatten_dictionary_values_lists(dictionary_2), [1, 2, 3, 4, 5, 6, 7, 8, 9])

        dictionary_3 = {"1": 1, "2": [2, 3, 4], "3": [5], "4": 6}
        self.assertEqual(game_board.flatten_dictionary_values_lists(dictionary_3), [1, 2, 3, 4, 5, 6])
    #
    #
# Testing the get_current_player, a getter
    def test_get_current_player(self):
        game_board = GameBoard(4, "b")
        self.assertEqual(game_board.get_current_player, "b")

        game_board.update_game_state(0) # invalid move
        self.assertEqual(game_board.get_current_player, "b")

        game_board.update_game_state(1) # move, should switch to white
        self.assertEqual(game_board.get_current_player, "w")
    #
    #
# Testing the get_result_count, a getter
    def test_get_current_player(self):
        game_board = GameBoard(8, "b")
        self.assertEqual(game_board.get_result_count(), {"w": 0, "b": 0})

        game_board.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        self.assertEqual(game_board.check_winner(), "TIE")
        self.assertEqual(game_board.get_result_count(), {"w": 24, "b": 24})
    #
    #
# Testing the get_color_conversion, a getter
    def test_get_current_player(self):
        game_board = GameBoard(8, "b")
        color_conversion = {
            "w": "white",
            "b": "black",
        }
        self.assertEqual(game_board.get_color_conversion(), color_conversion)
#
#
#
class testTile(unittest.TestCase):
#
# Testing the __init__ method:
    def test_normal_init_Tile(self):
        test_tile = Tile(0, (10.0, 20.0), 50, 5)
        self.assertEqual(test_tile.pixel_size_per_tile, 50)
        self.assertEqual(test_tile.coordinate_2D, (10.0, 20.0))
        self.assertEqual(test_tile.tile_index, 0)
        self.assertEqual(test_tile.pixel_space_in_tile, 5)
    
    
    def test_init_TypeError_Tile(self):
        with self.assertRaises(TypeError):
            test_tile = Tile("0", (10.0, 20.0), 50, 5)
    
        with self.assertRaises(TypeError):
            test_tile = Tile(0, (10, 20), 50, 5)
    
        with self.assertRaises(TypeError):
            test_tile = Tile(0, (10.0, 20.0), "50", 5)
    
        with self.assertRaises(TypeError):
            test_tile = Tile(0, (10.0, 20), 50, "5")
    
    
    def test_init_ValueError_Tile(self):
        with self.assertRaises(ValueError):
            test_tile = Tile(0, (10.0, 20.0), 5, 6)
    #
    #
# Testing the __eq__ method:
    def test_eq_is_True(self):
        test_tile_1 = Tile(0, (10.0, 20.0), 50, 5)
        test_tile_2 = Tile(0, (30.0, 20.0), 40, 6)
        self.assertTrue(test_tile_1 == test_tile_2)


    def test_eq_is_False(self):
        test_tile_1 = Tile(0, (10.0, 20.0), 50, 5)
        test_tile_2 = Tile(1, (10.0, 20.0), 50, 5)
        self.assertFalse(test_tile_1 == test_tile_2)


    def test_eq_is_False_is_not_tile_object(self):
        test_tile_1 = Tile(0, (10.0, 20.0), 50, 5)
        self.assertFalse(test_tile_1 == 2)
    #
    #
# Testing the __eq__ method:
    def test_str(self):
        test_tile = Tile(0, (10.0, 20.0), 50, 5)
        self.assertEqual(str(test_tile), "a tile at 0th place at game_board with length 50 at (10.0, 20.0)")
    #
    #
# Testing the getters:
    def test_getters_Tile(self):
        test_tile = Tile(0, (10.0, 20.0), 100, 10)
        self.assertEqual(test_tile.get_coordinate_2D(), (10.0, 20.0))
        self.assertEqual(test_tile.get_tile_index(), 0)
        self.assertEqual(test_tile.get_pixel_size_per_tile(), 100)
        self.assertEqual(test_tile.get_piece_starting_location_at_tile(), (20.0, -30.0))
#
#
#
class testPiece(unittest.TestCase):
#
# Testing the __init__ method:
    def test_normal_init_Piece_black(self):
        test_piece = Piece("black", (10.0, 20.0), 50)
        self.assertEqual(test_piece.coordinate_2D, (10.0, 20.0))
        self.assertEqual(test_piece.color, "black")
        self.assertEqual(test_piece.radius, 50)


    def test_normal_init_Piece_black(self):
        test_piece = Piece("white", (10.0, 20.0), 50)
        self.assertEqual(test_piece.coordinate_2D, (10.0, 20.0))
        self.assertEqual(test_piece.color, "white")
        self.assertEqual(test_piece.radius, 50)
    
    
    def test_init_TypeError_Piece(self):
        with self.assertRaises(TypeError):
            test_piece = Piece("black", (10, 20.0), 50)
    
        with self.assertRaises(TypeError):
            test_piece = Piece("black", (10.0, 20.0), "50")
    
    
    def test_init_ValueError_Piece(self):
        with self.assertRaises(ValueError):
            test_piece = Piece("blac", (10.0, 20.0), 50)

        with self.assertRaises(ValueError):
            test_piece = Piece("black", (10.0, 20.0), 0)

        with self.assertRaises(ValueError):
            test_piece = Piece("black", (10.0, 20.0), -1)
    #
    #
# Testing the __eq__ method:
    def test_eq_is_True(self):
        test_piece_1 = Piece("black", (10.0, 20.0), 50)
        test_piece_2 = Piece("black", (10.0, 20.0), 50)
        self.assertTrue(test_piece_1 == test_piece_2)


    def test_eq_is_False(self):
        test_piece_1 = Piece("black", (10.0, 20.0), 50)
        test_piece_2 = Piece("black", (10.0, 20.0), 49)
        self.assertFalse(test_piece_1 == test_piece_2)


    def test_eq_is_False_is_not_tile_object(self):
        test_piece_1 = Piece("black", (10.0, 20.0), 50)
        self.assertFalse(test_piece_1 == 2)
    #
    #
# Testing the __str__ method:
    def test_str(self):
        test_piece = Piece("black", (10.0, 20.0), 50)
        self.assertEqual(str(test_piece), "a black piece with radius 50 at (10.0, 20.0)")
    #
    #
# Testing the getters:
    def test_getters_Piece(self):
        test_piece = Piece("black", (10.0, 20.0), 50)
        self.assertEqual(test_piece.get_coordinate_2D(), (10.0, 20.0))
        self.assertEqual(test_piece.get_radius(), 50)
        self.assertEqual(test_piece.get_color(), "black")
#
#
#
class testDislpayTurtleGame(unittest.TestCase):
#
# Best way to explore the Display class is to visually judge the position
    pass
#
#
#
class testOthelloAI(unittest.TestCase):
#
# Testing the __init__ method:
    def test_init_easy_AI(self):
        ai = Othello_AI("easy")
        self.assertEqual(ai.difficulty, "easy")
        self.assertEqual(ai.number_of_immediate_child, 0)
        self.assertEqual(ai.current_move_explored, -1)
        self.assertEqual(ai.move_score_dict, dict())

    
    def test_init_hard_AI(self):
        ai = Othello_AI("hard")
        self.assertEqual(ai.difficulty, "hard")
    #
    #
# Testing the get_move_from_easy_AI method:
    def test_get_move_from_easy_AI(self):
        game_board = GameBoard(8, "b", is_tree_search = True)
        game_board.update_game_state(19)
        ai = Othello_AI("easy")
        
        expected_all_possible_moves = [18, 20, 34]
        for _ in range(1000):
            self.assertTrue(ai.get_move_from_easy_AI(game_board) in expected_all_possible_moves)
    #
    #
# Testing the find_random_max_flipping_moves method:
    def test_find_random_max_flipping_moves_with_same_value_lengths_except_one_move(self):
        ai = Othello_AI("hard")

        all_possible_moves = {19: [27, 38], 26: [27, 28, 30], 37: [36, 35, 45], 44: [36, 28, 1]}
        expected_random_moves = [26, 37, 44]
        for _ in range(1000):
            # will give random moves without 19
            self.assertTrue(ai.find_random_max_flipping_moves(all_possible_moves) in expected_random_moves)
    #
    #
# Testing the power_with_sign_remained method:
    def test_power_with_sign_remained(self):
        ai = Othello_AI("easy")
        self.assertEqual(ai.power_with_sign_remained(3, 4), 81)
        self.assertEqual(ai.power_with_sign_remained(3, 3), 27)
        self.assertEqual(ai.power_with_sign_remained(-3, 4), -81)
        self.assertEqual(ai.power_with_sign_remained(-3, 3), -27)
    #
    #
# Testing the calculate_game_state_score method:
    def test_calculate_game_state_score_at_start_up(self):
        ai = Othello_AI("easy")
        game_board = GameBoard(8, "b", is_tree_search = True)
        self.assertEqual(ai.calculate_game_state_score(game_board), 4)


    def test_calculate_game_state_score_at_full_board(self):
        ai = Othello_AI("easy")
        game_board = GameBoard(8, "b", is_tree_search = True)
        game_board.game_state = {
             0: 'w',  1: 'b',  2: 'w',  3: 'b',  4: 'w',  5: 'b',  6: 'w',  7: 'b',
             8: 'w',  9: 'b', 10: 'w', 11: 'b', 12: 'w', 13: 'b', 14: 'w', 15: 'b',
            16: 'w', 17: 'b', 18: 'w', 19: 'b', 20: 'w', 21: 'b', 22: 'w', 23: 'b', 
            24: 'w', 25: 'b', 26: 'w', 27: 'b', 28: 'w', 29: 'b', 30: 'w', 31: 'b', 
            32: 'w', 33: 'b', 34: 'w', 35: 'b', 36: 'w', 37: 'b', 38: 'w', 39: 'b', 
            40: 'w', 41: 'b', 42: 'w', 43: 'b', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'b', 50: 'w', 51: 'b', 52: 'w', 53: 'b', 54: 'w', 55: 'b', 
            56: 'w', 57: 'b', 58: 'w', 59: 'b', 60: 'w', 61: 'b', 62: 'w', 63: 'b',
        }
        self.assertEqual(ai.calculate_game_state_score(game_board), 0)


    def test_calculate_game_state_score_at_no_legal_move_without_full_board(self):
        ai = Othello_AI("easy")
        game_board = GameBoard(8, "b", is_tree_search = True)
        game_board.game_state = {
             0: 'w',  1: 'e',  2: 'w',  3: 'e',  4: 'w',  5: 'e',  6: 'b',  7: 'e',
             8: 'w',  9: 'b', 10: 'b', 11: 'w', 12: 'w', 13: 'b', 14: 'b', 15: 'b',
            16: 'w', 17: 'e', 18: 'b', 19: 'e', 20: 'w', 21: 'e', 22: 'b', 23: 'e', 
            24: 'w', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'b', 31: 'b', 
            32: 'w', 33: 'e', 34: 'b', 35: 'e', 36: 'b', 37: 'e', 38: 'b', 39: 'e', 
            40: 'w', 41: 'b', 42: 'w', 43: 'w', 44: 'w', 45: 'b', 46: 'w', 47: 'b', 
            48: 'w', 49: 'e', 50: 'w', 51: 'e', 52: 'b', 53: 'e', 54: 'b', 55: 'e', 
            56: 'w', 57: 'w', 58: 'w', 59: 'w', 60: 'w', 61: 'w', 62: 'w', 63: 'b',
        }
        self.assertEqual(ai.calculate_game_state_score(game_board), 0)
    #
    #
# Testing the assign_score_end_game_move method:
    def test_assign_score_end_game_move(self):
        ai = Othello_AI("hard")
        self.assertEqual(ai.move_score_dict, dict())

        ai.current_move_explored = 19
        result = "BLACK"
        ai.assign_score_end_game_move(result)
        self.assertEqual(ai.move_score_dict,{19: -100000})

        ai.current_move_explored = 20
        result = "WHITE"
        ai.assign_score_end_game_move(result)
        self.assertEqual(ai.move_score_dict,{19: -100000, 20: 100000})
                
        ai.current_move_explored = 22
        result = "TIE"
        ai.assign_score_end_game_move(result)
        self.assertEqual(ai.move_score_dict, {19: -100000, 20: 100000})
    #
    #
    def test_assign_score_end_game_move(self):
        ai = Othello_AI("hard")
        with self.assertRaises(ValueError):
            ai.assign_score_end_game_move(1)
    #
    #
# Testing the assign_score_with_special_tiles method:
    def test_assign_score_with_special_tile(self):
        ai = Othello_AI("hard")
        self.assertEqual(ai.move_score_dict, dict())
        
        ai.current_move_explored = 19
        # move in SWEET_16_TILES
        ai.move_score_dict[ai.current_move_explored] = 0
        ai.assign_score_with_special_tiles(19, 1, 2)
        self.assertEqual(ai.move_score_dict, {19: 5**(2+1)})
        
        ai.current_move_explored = 19
        # move in EDGE_TILE_EXCLUDE_HORRIBLE_4_X
        ai.assign_score_with_special_tiles(2, -1, 2)
        self.assertEqual(ai.move_score_dict, {19: 125 - 4 ** 3})
        
        ai.current_move_explored = 20
        # move in HORRIBLE_4_X
        ai.move_score_dict[ai.current_move_explored] = 0
        ai.assign_score_with_special_tiles(9, 1, 1)
        self.assertEqual(ai.move_score_dict, {19: 61, 20: -900})
        
        ai.current_move_explored = 20
        # move in SECOND_HORRIBLE_8_X
        ai.assign_score_with_special_tiles(1, 1, 2)
        self.assertEqual(ai.move_score_dict, {19: 61, 20: -900 - 10**3})
        
        ai.current_move_explored = 21
        # move in CORNER_4 
        ai.move_score_dict[ai.current_move_explored] = 0
        ai.assign_score_with_special_tiles(63, -1, 0)
        self.assertEqual(ai.move_score_dict, {19: 61, 20: -1900, 21: -100})

        with self.assertRaises(ValueError):
            ai.assign_score_with_special_tiles(64, -1, 0)

        with self.assertRaises(ValueError):
            ai.assign_score_with_special_tiles(64, -2, 0)

        with self.assertRaises(ValueError):
            ai.assign_score_with_special_tiles(63, 1, 3)
    #
    #
# Testing the recurssive lookup method:
    def test_recursive_lookup(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "b", is_tree_search = True)
        game_board.update_game_state(19)
        expected_game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'b', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(game_board.get_game_state(), expected_game_state)

        self.assertTrue(18 in game_board.get_all_possible_moves())
        ai.current_move_explored = 18
        ai.move_score_dict[18] = 0
        ai.recursive_lookup(game_board, 18, 2)
        self.assertEqual(ai.move_score_dict, {18: 7502})
        self.assertEqual(ai.number_of_immediate_child, 4)
    #
    #
# Testing the get_move_from_difficult_AI method:
    def test_get_move_from_difficult_AI_capture_corner(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'b', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'b', 20: 'e', 21: 'b', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'w', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()

        lst_of_moves = [7, 18, 20, 34]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)
            ai.current_move_explored = move
            ai.move_score_dict[move] = 0
            ai.recursive_lookup(game_board, move, 2)
            ai.move_score_dict[move] /= ai.number_of_immediate_child

        self.assertEqual(ai.move_score_dict, {7: 252397.75, 18: 10390.666666666666, 20: 7649.928571428572, 34: 4338.473684210527})

        # AI will advice capturing of corner tile at tile 7 with most value 252397.75
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 7)
    #
    #
    def test_get_move_from_difficult_AI_capture_SWEET_16_not_HORRIBLE_4_X(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'b', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'b', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'w', 43: 'e', 44: 'e', 45: 'b', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()
        # will capture tiles within SWEET 16 but not 54, the HORRIBLE_4_X
        lst_of_moves = [18, 20, 21, 34, 54]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)
            ai.current_move_explored = move
            ai.move_score_dict[move] = 0
            ai.recursive_lookup(game_board, move, 2)
            ai.move_score_dict[move] /= ai.number_of_immediate_child

        self.assertEqual(ai.move_score_dict, {18: 8848.833333333334, 20: 1017.4545454545455, 21: -250.42857142857142, 34: 607.5, 54: -48041.09090909091})

        # AI will NOT advice capturing of corner tile at tile 54 with least value -48041.09090909091 since strategically it is ia bad move
        self.assertNotEqual(ai.get_move_from_difficult_AI(game_board), 54)
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 18)
    #
    #
    def test_get_move_from_difficult_AI_capture_SECOND_HORRIBLE_8_X_not_HORRIBLE_4_X(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'b', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'w', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'e', 36: 'b', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'b', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()
        # will capture tiles within SECOND_HORRIBLE_8_X but not 54, the HORRIBLE_4_X
        lst_of_moves = [8, 54]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)
            ai.current_move_explored = move
            ai.move_score_dict[move] = 0
            ai.recursive_lookup(game_board, move, 2)
            ai.move_score_dict[move] /= ai.number_of_immediate_child

        self.assertEqual(ai.move_score_dict, {8: 699.0, 54: -13605.0})

        # AI will NOT advice capturing of corner tile at tile 54 with least value -13605.0 since strategically it is ia bad move, capture 8 which isnt as bad
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 8)
    #
    #
    def test_get_move_from_difficult_AI_capture_SECOND_HORRIBLE_8_X_not_HORRIBLE_4_X_2(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'b', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'e', 28: 'w', 29: 'e', 30: 'e', 31: 'e', 
            32: 'w', 33: 'e', 34: 'e', 35: 'e', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'b', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()
        lst_of_moves = [14, 48]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)
            ai.current_move_explored = move
            ai.move_score_dict[move] = 0
            ai.recursive_lookup(game_board, move, 2)
            ai.move_score_dict[move] /= ai.number_of_immediate_child

        self.assertEqual(ai.move_score_dict, {14: -27064.0, 48: -562.5})

        # will capture tiles 14 actually will make computer white lose the corner 7, lookup ahea will detect and avoid
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 48)
    #
    #
    def test_get_move_from_difficult_AI_capture_EDGE_not_SWEET_16(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'b', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'e', 35: 'b', 36: 'e', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'b', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'b', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()
        # will capture tiles within SWEET 16 but not 54, the HORRIBLE_4_X
        lst_of_moves = [29, 59]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)

        # AI will advice EDGE 59 instead of 29 in SWEET_16 since exploring the second layer of tree, it gives more mobility to the latter one
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 59)
    #
    #    
    def test_get_move_from_difficult_AI_capture_WIN_MOVE(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'w', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'b', 36: 'b', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'b', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'w', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }

        all_possible_moves = game_board.get_all_possible_moves()
        # will capture tiles within SWEET 16 but not 54, the HORRIBLE_4_X
        lst_of_moves = [37, 45, 52]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)

        # AI will advice 37 leading to direct win in 2 steps
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 37)
    #
    #
    def test_get_move_from_difficult_AI_capture_move_without_lost_in_2_steps(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'b', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'b', 19: 'w', 20: 'b', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'b', 26: 'b', 27: 'b', 28: 'b', 29: 'b', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'e', 36: 'w', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'e', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'e', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
    }
        # move at 35 will lead to lose if black takes 43 subsequently, so move 35 is an absolute NO NO, actuall 17 and 21 will leave to a full wipe out too
        all_possible_moves = game_board.get_all_possible_moves()
        lst_of_moves = [3, 9, 10, 12, 13, 16, 17, 21, 22, 33, 35, 37]
        for move in lst_of_moves:
            self.assertTrue(move in all_possible_moves)
            ai.current_move_explored = move
            ai.move_score_dict[move] = 0
            ai.recursive_lookup(game_board, move, 2)
            ai.move_score_dict[move] /= ai.number_of_immediate_child

        self.assertEqual(ai.move_score_dict, {3: 2177.777777777778, 9: -31141.70588235294, 10: 4211.5, 12: 101.80645161290323, 
        13: -88.84615384615384, 16: 458.3125, 17: -1.7241379310344827e+19, 21: -1.4705882352941177e+19, 22: 350.57142857142856, 
        33: 133.26506024096386, 35: -1.111111111111111e+19, 37: 61.927083333333336})

        # move 35 has the lowest value since it leads to a full wipeout after 2 steps, imgaination is what makes the return of large negative value possible
        # move 17 and 21 will lead to a wipeout after 2 steps, upon setting this up, I only noticed move 35 is a lose for white, and upon calculating and double-checking the values for 17 and 21,
        # Therefore the preferred looking steps ahead should make the AI avoid choice of 17, 21, and 35
        # The most important thing here is how NOT to lose
        self.assertEqual(ai.get_move_from_difficult_AI(game_board), 10)
    #
    #
# Testing the get_move method:
    def test_get_move_calling_easy_AI(self):
        ai = Othello_AI("easy")
        game_board = GameBoard(8, "b", is_tree_search = True)
        game_board.update_game_state(19)
        expected_all_possible_moves = [18, 20, 34]
        for _ in range(1000):
            self.assertTrue(ai.get_move(game_board) in expected_all_possible_moves)
    #
    #
    def test_get_move_calling_hard_AI(self):
        ai = Othello_AI("hard")
        game_board = GameBoard(8, "w", is_tree_search = True)
        game_board.game_state = {
             0: 'e',  1: 'e',  2: 'e',  3: 'e',  4: 'e',  5: 'e',  6: 'e',  7: 'e',
             8: 'e',  9: 'e', 10: 'e', 11: 'e', 12: 'e', 13: 'e', 14: 'e', 15: 'e',
            16: 'e', 17: 'e', 18: 'e', 19: 'w', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 
            24: 'e', 25: 'e', 26: 'e', 27: 'w', 28: 'e', 29: 'e', 30: 'e', 31: 'e', 
            32: 'e', 33: 'e', 34: 'w', 35: 'b', 36: 'b', 37: 'e', 38: 'e', 39: 'e', 
            40: 'e', 41: 'e', 42: 'e', 43: 'b', 44: 'e', 45: 'e', 46: 'e', 47: 'e', 
            48: 'e', 49: 'e', 50: 'e', 51: 'w', 52: 'e', 53: 'e', 54: 'e', 55: 'e', 
            56: 'e', 57: 'e', 58: 'e', 59: 'e', 60: 'e', 61: 'e', 62: 'e', 63: 'e',
        }
        self.assertEqual(ai.get_move(game_board), 37)
    #
    #
    # ========================= END OF TESTING =========================
#
#
#
#
#
def main():
     unittest.main(verbosity = 3)
#
#
#
if __name__ == "__main__":
    main()
