import math

class Tile():
    '''
    This contains the feature of the individual tile, all it need to draw it on turtle

    Attribute:
        as described in __init__

    Method:
        as shown below
    '''
#
    def __init__(self, tile_index, coordinate_2D, pixel_size_per_tile, pixel_space_in_tile):
        '''
        Method: __init__
            to initialize all distinct values of tile
        Parameters:
            tile_index: the index of tile, starting 0 from upper left, to the larger index at lower right
            coordinate_2D: a tuple storing (x, y) as pixel on turtle screen
            pixel_size_per_tile: the amount of pixel that a tile occupy on screen to display
            pixel_size_per_tile: the amount of pixel that a tile occupy on screen to display
            pixel_space_in_tile: the amonut of pixel of space between piece circumference and tile boarders
        Return:
            none, just initialize the class
        Possible Error Raise:
            tile_index must be of type int
            coordinate_2D must be float tuples for (x, y)
            pixel_size_per_tile must be of type int or type float
            pixel_space_in_tile must be of type int or float
            pixel_space_in_tile must be smaller than pixel_size_per_tile
        '''        
        if not isinstance(tile_index, int):
            raise TypeError("tile_index must be of type int")

        if not isinstance(pixel_size_per_tile, int) and not isinstance(pixel_size_per_tile, float):
            raise TypeError("pixel_size_per_tile must be of type int or float")

        if not isinstance(pixel_space_in_tile, int) and not isinstance(pixel_size_per_tile, float):
            raise TypeError("pixel_space_in_tiles must be of type int or float")

        if not isinstance(coordinate_2D, tuple):
            raise TypeError("coordinate_2D must be a tuple of (x, y)")

        if not isinstance(coordinate_2D[0], float) or not isinstance(coordinate_2D[1], float):
            raise TypeError("coordinate_2D must be a tuple containing float as pixel (x, y)")
        
        if pixel_size_per_tile < pixel_space_in_tile:
            raise ValueError("pixel_space_in_tile must be smaller than pixel_size_per_tile")


        self.pixel_size_per_tile = pixel_size_per_tile
        self.coordinate_2D = coordinate_2D
        self.tile_index = tile_index
        self.pixel_space_in_tile = pixel_space_in_tile
#
#
# 
    def __eq__(self, other):
        '''
        Method -- __eq__:
            check if the two Tiles are equal by going through all attributes
        Parameters:
            other: the other Tiles object
        Return:
            none
        Possible Error raised:
            none, return False if other is not of type Tiles
        '''
        if not isinstance(other, Tile):
            return False

        return (self.get_tile_index() == other.get_tile_index())
#
#
#
    def __str__(self):
        '''
        Method -- str:
            generate a string representation of the object
        Parameters:
            none
        Return:
            a string representation of object class Tile
        Possible Error raised:
            none
        '''
        return f"a tile at {self.tile_index}th place at game_board with length {self.pixel_size_per_tile} at {self.coordinate_2D}"
#
#
#
   
    def get_coordinate_2D(self):
        '''
        Method -- get_color:
            just a getting of coordinate_2D attritube
        Parameters, Possible Error raise:
            none
        Returns:
            a tuple of (x, y) in pixel, containing two floats
        '''
        return self.coordinate_2D
#
#
#
    def get_pixel_size_per_tile(self):
        '''
        Method -- get_color:
            just a getting of pixel_size_per_tile attritube
        Parameters, Possible Error raise:
            none
        Returns:
            the pixel that each tile occupies on screen, a float
        '''
        return self.pixel_size_per_tile
#
#
#
    def get_tile_index(self):
        '''
        Method -- get_color:
            just a getting of tile_index attritube
        Parameters, Possible Error raise:
            none
        Returns:
            The index of tile an integer, from 0 at upper left, to 15 for a 4 x 4 board at the lower right
        '''
        return self.tile_index
#
#
#
    def get_piece_starting_location_at_tile(self):
        '''
        Method -- get_tile_center:
            get centre of tile, downward negative
        Parameters, Possible Error raise:
            none
        Returns:
            a tuple of (x, y) of tile center in pixel, containing two floats
        '''
        x, y = self.coordinate_2D
        # piece starts from west side of circle
        return (x + self.pixel_space_in_tile, y - self.pixel_size_per_tile / 2)