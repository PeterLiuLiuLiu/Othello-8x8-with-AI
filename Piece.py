import Tile

class Piece():
    '''
    This contains the feature of the individual piece, all it need to draw it on turtle

    Attribute:
        as described in __init__

    Method:
        as shown below
    '''
#
    def __init__(self, color, coordinate_2D, radius):
        '''
        Method: __init__
            to initialize all distinct values of tile
        Parameters:
            color: color of piece, must be either black or white
            coordinate_2D: a tuple storing (x, y) as pixel on turtle screen
            radius: the amount of pixel that a piece radius occupies on screen
        Return:
            none, just initialize the class
        Possible Error Raise:
            the piece of color must be either be black or white
            radius must be int or float
            coordinate_2D must be float tuples for (x, y)
        '''
        if color.lower() != "black" and color.lower() != "white":
            raise ValueError("Wrong color for the piece, please set it to white of black")

        if not isinstance(radius, int) and not isinstance(radius, float):
            raise TypeError("piece's radius must be of type int or float")

        if not isinstance(coordinate_2D[0], float) or not isinstance(coordinate_2D[1], float):
            raise TypeError("coordinate_2D must be a tuple containing float as pixel (x, y)")

        if radius <= 0:
            raise ValueError("radius of piece must be greater than zero")

        self.color = color
        # (x, y) is the starting position of turtle circle, NOT square center, 
        # turtle starts drawing from upper left corner
        self.coordinate_2D = coordinate_2D
        self.radius = radius
#
#
#
    def __eq__(self, other):
        '''
        Method -- __eq__:
            check if the two Pieces are equal by going through all attributes
        Parameters:
            other: the other Piece object
        Return:
            none
        Possible Error raised:
            none, return False if other is not of type Piece
        '''
        if not isinstance(other, Piece):
            return False

        return (self.get_coordinate_2D() == other.get_coordinate_2D()) and \
            (self.get_color() == other.get_color()) and (self.get_radius() == other.get_radius())
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
            a string representation of object class Piece
        Possible Error raised:
            none
        '''
        return f"a {self.color} piece with radius {self.radius} at {self.coordinate_2D}"
#
#
#
    def get_color(self):
        '''
        Method -- get_color:
            just a getting of color attritube
        Parameters, Possible Error raise:
            none
        Returns:
            a string of color of piece
        '''
        return self.color
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
    def get_radius(self):
        '''
        Method -- get_color:
            just a getting of radius attritube
        Parameters, Possible Error raise:
            none
        Returns:
            the pixel that each piece occupies on screen, a float
        '''
        return self.radius
#
#
#
