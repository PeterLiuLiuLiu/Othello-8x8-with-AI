
import turtle
from Piece import *
from Tile import *
from StoreTileChanged import *

PIXEL_SIZE_PER_TILE = 50    # recommended range (50 - 75)
PIXEL_SPACE_IN_TILE = 5     # recommended range (4 - 6)
DISPLAY_FACTOR = 2        # recommended range(1.3 - 2)

TILE_OFFSET_FACTOR_HORIZONTAL = 2   # no change recommended
TILE_OFFSET_FACTOR_VERTICAL = 5   # the smaller the value the larger the offset
TURTLE_SPEED = 0                    # no change recommended, 0 fastest
GAME_TITLE = "Peter's Othello"

GAME_BOARD_LINE_WEIGHT = 1.5
GAME_BOARD_BORDER_COLOR = "black"
GAME_BOARD_BASE_COLOR = "green"
PIECE_LINE_WEIGHT = 0

class DisplayTurtleGame():
    '''
    This class displays the model to turtle, the class is the viewer of the game

    Attribute:
        game_board: 
            an instance of game_board as parameter, must implement copy.deepcopy ,
            or it will change when update_game_state at GameBoard class is called 
            since it is referencing the same memory
        game_board_size:
            number of tiles per side
        turtle: 
            an instance of turtle.Turtle class
        screen:
            an instance of turtle.Screen class
        piece_radius:
            radius of piece
        board_width:
            board width display in pixel
        board_height:
            board height display in pixel
        screen_width:
            screen_width of the whole turtle screen displayed in pixel
        screen_height:
            screen_height of the whole turtle screen displayed in pixel
        tile_offset_horizontal: 
            x direction offset of each tile for the center draw of overall game_board
        tile_offset_vertical: 
            y direction offset of each tile for the center draw of overall game_board
        piece_offset_horizontal:
            x direction offset of each piece for the center draw of overall game_board
        piece_offset_vertical:
            y direction offset of each piece for the center draw of overall game_board
        color_conversion:
            a dictionary matching the symbol used in game_state pure char, to real color to be displayed in turtle
        new_piece_played:
            a dictionary containing the difference in previous self.game_board to the new_game_board,
            new_piece_played compares and update after refresh_game_screen is run, by  comparing the new_game_board passed into
        piece_classes:
            a dictionary containing piece classes, 
            from the occupied slot in game_state into piece_class with it's own feature for drawing
        tile_classes:
            dictionary containing tile_index as key, and tile class as values 
        etc    
    Method:
        as shown below
    '''
#
    def __init__(self, game):
        '''
        Method -- __init__:
            To be initialized when class is instantiated, also call screen.setup and init_game_visuals to start drawing on turtle
        Parameter:
            game: 
                an instance of gameEngine as parameter
        Returns:
            none
        Possible Error raise:
            GameEngine must be valid upon passing and must be an instance of GameEngine class
        '''
        if not game.game_board.is_valid_game_state():
            raise ValueError("Invalid game_state for game_board.")

        self.game_engine = game

        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()

        self.game_board = game.game_board

        self.game_board_size = self.game_board.get_game_board_size()

        self.turtle.speed(TURTLE_SPEED)
        self.turtle.hideturtle()
        self.screen.title(GAME_TITLE)
        
        self.piece_radius = PIXEL_SIZE_PER_TILE / 2 - PIXEL_SPACE_IN_TILE

        self.board_width = PIXEL_SIZE_PER_TILE * self.game_board_size
        self.board_height = PIXEL_SIZE_PER_TILE * self.game_board_size

        self.screen_width = self.board_width * DISPLAY_FACTOR
        self.screen_height = self.board_height * DISPLAY_FACTOR

        self.tile_offset_horizontal = - self.board_width / TILE_OFFSET_FACTOR_HORIZONTAL # left is negative
        self.tile_offset_vertical = - self.board_height / TILE_OFFSET_FACTOR_VERTICAL # down is positive

        self.piece_offset_horizontal = self.tile_offset_horizontal + PIXEL_SIZE_PER_TILE / 2 
        self.piece_offset_vertical = self.tile_offset_vertical + (- PIXEL_SIZE_PER_TILE + PIXEL_SPACE_IN_TILE)

        self.piece_classes = dict()
        self.new_piece_played = dict()
        self.tile_classes = dict()
        self.game_board_internal_lines = dict()
        self.game_board_external_boundary_starting = tuple()

        self.screen.setup(self.screen_width, self.screen_height)
        self.init_game_visuals()

        self.turn_on_turtle_click()
#
#
#
    def get_move(self, x, y):
        '''
        Method -- get_move
            the method is to be binded with self.turtle for on click event
            just record the x, y and turn into tile played, trigger the place_move and print if there is a winner
        Parameters:
            x: x coordinate on turtle screen that the user's mouse has been to, 
                if used in on click, then its the clicked x coordinate
            y: y coordinate on turtle screen that the user's mouse has been to, 
                if used in on click, then its the clicked y coordinate
        Return: 
            none, just record x, y
        Possible Error raised:
            TypeError: x, y should be of type float
        '''
        if not isinstance(x, float) or not isinstance(y, float):
            raise TypeError("x, y must be of type float")

        x_boundary = self.get_gameboard_pixel_boundary()[0]
        y_boundary = self.get_gameboard_pixel_boundary()[1]

        if (x < x_boundary[0] or x > x_boundary[1]) or (y < y_boundary[0] or y > y_boundary[1]):
            # Not to show this error, just do nothing when the player clicked in invalid locations
            pass
            # print("Please click a valid tile without game board shown")
            # print(f"{self.game_board.get_current_player()}'s move") 
            # raise ValueError("Location clicked out of bounds")
        
        # user clicked inside game_board
        else:
            for tile in self.tile_classes.values():
                tile_x, tile_y = tile.get_coordinate_2D()
                tile_size = tile.get_pixel_size_per_tile()
                # to find whcih tile matches the click pixel and pass into the game_board for model calculations
                if (tile_x > x - tile_size and tile_x <= x) and (tile_y > y and tile_y <= y + tile_size):
                    # Try except block used here since violence clicked in manual testing will induce error from turtle upon getting multiple clicks
                    try:
                        if tile.get_tile_index() in self.game_board.get_all_possible_moves():
                            self.game_engine.pass_move_into_model_and_check_winner(tile.get_tile_index())
                        
                    except:
                        print("Error occured, the console will be closed. Please restart the game")
                        self.game_engine.end_corrupted_game()
#
#
#
    def get_gameboard_pixel_boundary(self):
        '''
        Method -- get_gameboard_pixel_boundary
            This method returns the x and y boundary of the game_board pixel on screen
        Parameters:
            none
        Returns:
            nested tuple, ((x_min, x_max), (y_min, y_max)), contains float within it
        Possible Error raised:
            none
        '''
        x_y_lower_left = self.tile_classes[self.game_board_size ** 2 - self.game_board_size].get_coordinate_2D()
        x_y_upper_right = self.tile_classes[self.game_board_size - 1].get_coordinate_2D()
        # x_min locates at the left most
        x_min = x_y_lower_left[0]
        # x_min locates at the right most
        x_max = x_y_upper_right[1]

        # y_min locates at the lower most
        y_min = x_y_lower_left[0]
        # y_max locates at the upper most
        y_max = x_y_upper_right[1]

        return ((x_min, x_max), (y_min, y_max))   
#
#
#
    def init_game_visuals(self):
        '''
        Method -- init_game_visuals:
            to initialize the game by calling function, draw blank board and put 4 initial pieces onto it
        Parameters, Returns, Possible Error raise:
            none
        '''
        print(f"Please wait for the game to initialize...")
        
        self.draw_blank_game_board()
        # assume the new piece played is the initial 4, 2w 2b
        self.refresh_game_screen(True)
#
#
#
    def generate_pixel_coordinates_on_screen(self, offset_horizontal = 0, offset_vertical = 0):
        '''
        Method -- generate_pixel_coordinates_on_screen:
            to generate a dictionary of the all slots 0 to self.game_board_size ** 2 - 1 on screen, with predefined offset in both directions
        Parameters:
            offset_horizontal -- how much offset to  left and right
            offset_vertical -- how much offset to  up and down
        Return: 
            a dictionary containing all game_board_size ** 2 nos. of coordinate
            key: [0, game_board_size ** 2 - 1)
            value: tuple containing (x, y) with pixel on screen offset
        Possible Error raise:
            TypeError: offset_horizontal and offset_vertical must be of type int or float
        '''
        if not isinstance(offset_horizontal, int) and not isinstance(offset_horizontal, float):
            raise TypeError("offset_horizontal must be of type int or float")

        if not isinstance(offset_vertical, int) and not isinstance(offset_vertical, float):
            raise TypeError("offset_vertical must be of type int or float")

        
        # can be for tile or piece
        coordinate_dict = dict()

        # vertical is fliped since the the game_board counts from up to down, 
        # but the screen pixel counts from down to up
        for vertical in range(self.game_board_size): 
            for horizontal in range(self.game_board_size):
                # Create a tuple of (x, y) in pixel
                # The key of dictionary is reversely populated since the game board is definied from top to bottom,
                # while the screen pixel goes up from negative to positive
                coordinate_dict[(self.game_board_size - 1 - vertical) * self.game_board_size + horizontal] = \
                    (horizontal * PIXEL_SIZE_PER_TILE + offset_horizontal, \
                        vertical * PIXEL_SIZE_PER_TILE + offset_vertical)

        return coordinate_dict
#
#
#
    def refresh_game_screen(self, is_initializing = False):
        '''
        Method -- refresh_game_screen:
            to be called externally by GameEngine's place_move upon valid move is made, and the game model is updated
            Since singletone class stores the tile flipped, this method can access it and flip the cooresponding tiles in turtle by accessing singleton
        Parameter:
            is_initializing: a boolean for if the game is is_initializing the first 4 pieces, if yes,, no comparison to be done
        Return:
            none, call method to draw new piece
        Possible Error raise:
            TypeError: is_initializing must be of type bool
            ValueError: wrong value stored in singleton for tile_index to be flipped
        '''

        if not isinstance(is_initializing, bool):
            raise TypeError("is_initializing must be of type bool")


        if not is_initializing:
            # get stored tile_move from singleton
            if isinstance(get_tile_index_changed(), int):
                self.new_piece_played[get_tile_index_changed()] = get_player_played()

            elif isinstance(get_tile_index_changed(), list):
                for value in get_tile_index_changed():
                    if not isinstance(value, int):
                        raise ValueError("singleton stored tile_index must be of int of list of int")
                    else:
                        self.new_piece_played[value] = get_player_played()

            else:
                raise ValueError("singleton stored tile_index must be of int of list of int")


        else:
            self.new_piece_played = self.game_board.get_game_state()

        # turn off clicking function when new pieces are drawn and flipped
        # turn the clicking back on when the turtle is done drawing
        self.turn_off_turtle_click()
        self.draw_new_piece()
        # if self.game_board.check_winner() == "CONTINUE":
        self.turn_on_turtle_click()

#
#
#
    def draw_new_piece(self):  
        '''
        Method -- draw_new_piece:
            draw all the new piece from self.new_piece_played by initialing new Piece class
        Parameters, Returns, Possible Error raise:
            none
        '''

        piece_coordinate_dict = self.generate_pixel_coordinates_on_screen(self.piece_offset_horizontal, self.piece_offset_vertical)
        
        self.turtle.pensize(PIECE_LINE_WEIGHT)

        for index, piece_type in self.new_piece_played.items():
            # piece_type is the color, "w", "b" or "e" ("e" may not be a color, but it is denoted empty)
            if piece_type != "e":
                new_piece = Piece(self.game_board.color_conversion[piece_type], piece_coordinate_dict[index], self.piece_radius)
                self.piece_classes[index] = new_piece
                self.turtle.fillcolor(new_piece.get_color())
                # piece boundary same color with fill color
                self.turtle.pencolor(new_piece.get_color())

                self.turtle.penup()
                # new piece's index equals tile_index
                self.turtle.setposition(self.tile_classes[index].get_piece_starting_location_at_tile())
                self.turtle.pendown()

                self.turtle.begin_fill()
                self.turtle.circle(new_piece.get_radius())
                self.turtle.end_fill()    

        self.new_piece_played = dict() 
#
#       
#
    def draw_blank_game_board(self):
        '''
        Method -- draw_blank_game_board:
            draw all clean_board graphics at game initialization stage, 
            call populate_game_board_coordinate_and_tile_classes to get pixel coordinates
        Parameters, Returns, Possible Error raise:
            none
        '''
        self.populate_game_board_drawing_coordinate_and_tile_classes()

        self.turtle.pensize(GAME_BOARD_LINE_WEIGHT)
        self.turtle.pencolor(GAME_BOARD_BORDER_COLOR)
        self.turtle.fillcolor(GAME_BOARD_BASE_COLOR)

        self.turtle.penup()
        self.turtle.setposition(self.game_board_external_boundary_starting)
        self.turtle.pendown()

        total_side_length_of_game_board = self.game_board_size * PIXEL_SIZE_PER_TILE
        self.turtle.begin_fill()
        # draw game_board outter boundarys
        for _ in range(4):
            self.turtle.forward(total_side_length_of_game_board)
            self.turtle.right(90)
        self.turtle.end_fill()

        for coordinate, direction in self.game_board_internal_lines.items():
            if direction == "down":
                self.turtle.setheading(270) # 270 denotes down
            else: # direction == "right":
                self.turtle.setheading(0) # 270 denotes down
            self.turtle.penup()
            self.turtle.setposition(coordinate)
            self.turtle.pendown()
            self.turtle.forward(total_side_length_of_game_board)
#
#
#
    def populate_game_board_drawing_coordinate_and_tile_classes(self):
        '''
        Method -- populate_game_board_drawing_coordinate_and_tile_classes:
            populate necessary coordinates for clean_game_board_drawings
        Parameters, Returns, Possible Error raise:
            none
        '''
        tile_coordinate_dict = self.generate_pixel_coordinates_on_screen(self.tile_offset_horizontal, self.tile_offset_vertical)
        
        for tile_index, tile_2D_coordinate in tile_coordinate_dict.items():

            tile = Tile(tile_index, tile_2D_coordinate, PIXEL_SIZE_PER_TILE, PIXEL_SPACE_IN_TILE)
            self.tile_classes[tile_index] = tile

            # populate internal line starting point
            if tile_index > 0:
                if tile_index < self.game_board_size: # first row's, populate internal vertical lines starting points
                    self.game_board_internal_lines[tile_2D_coordinate] = "down"
                
                elif tile_index % self.game_board_size == 0: # first column's, populate internal horizontal lines starting points
                    self.game_board_internal_lines[tile_2D_coordinate] = "right"

            # populate external boundary game_board square starting point
            else:
                self.game_board_external_boundary_starting = tile_2D_coordinate
#
#
#
    def get_tile_classes(self):
        '''
        Method -- get_tile_classes:
            tile_classes dictionary getter
        Parameters, Possible Error raise:
            none
        Returns:
            a dictionary containing tile_index as key, and tile class as values 
        '''
        return self.tile_classes
#
#
#
    def get_piece_classes(self):
        '''
        Method -- get_piece_classes:
            pile_classes dictionary getter
        Parameters, Possible Error raise:
            none
        Returns:
            a dictionary of tile as its key, pile class instance as its value
        '''
        return self.piece_classes
#
#
#
    def turn_off_turtle_click(self):
        '''
        Method -- turn_off_turtle_click:
            deregister clicking event handler
        Parameters, Returns, Possible Error raise:
            none
        '''
        self.screen.onclick(None)
#
#
#
    def turn_on_turtle_click(self):
        '''
        Method -- turn_on_turtle_click:
            register clicking event handler to get_move
        Parameters, Returns, Possible Error raise:
            none

        '''
        self.screen.onclick(self.get_move)
#
#
#


