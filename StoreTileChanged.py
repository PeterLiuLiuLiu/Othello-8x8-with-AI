
# Code from lab 4 problem #2 singleton used
# To be expaneded to store all flipped tiles for MILESTONE 2

class StoreTileChanged():
    ''' 
    a class that stores the new piece played and the player who played it, 
    shared among different class so comparison between old board and new board is not needed
    functions in this file creates the class if the class it not instantiated, otherwise, 
    stick to the class created and access the memory of where the singleton class stores data
    The class will be created once and only once for efficient use of memory by sharing the same memory and from the single source ??
    '''
    singleton = None

    def __init__(self):
        '''
        Method -- __init__
            define the attritube and initialize
        '''
        self.tile_index = -1
        self.player = "e"

    @classmethod
    def get_instance(cls):
        '''
        Similar to java's static class, where calling the method of the class requires no instantiation of the class itself ??
        '''
        if StoreTileChanged.singleton == None:
            StoreTileChanged.singleton = StoreTileChanged()
        return StoreTileChanged.singleton


def record_tile_index_changed(tile_index):
    '''
    Function: record_tile_index_changed
        setter, and store in singleton
    Parameter:
        tile_index: value to be stored
    Return:
        none
    Possible Error raised:
        TypeError: tile_index must be of type int or a list of int
    '''
    if isinstance(tile_index, list):
        for value in tile_index:
            if not isinstance(value, int):
                raise TypeError("tile_index must be of type int or list of int")

    elif not isinstance(tile_index, int):
        raise ValueError("tile_index must be of type int or list of int")

    instance = StoreTileChanged.get_instance()
    instance.tile_index = tile_index

def get_tile_index_changed():
    '''
    Function: get_tile_index_changed
        getter
    Parameter, Possible Error raised:
        none
    Returns:
        the tile_index, an int or a list of int
    '''
    instance = StoreTileChanged.get_instance()
    return instance.tile_index

def record_player(player):
    '''
    Function: record_player
        setter, and store in singleton
    Parameter:
        player: value to be stored
    Return:
        none
    Possible Error raised:
        TypeError: tile_index must be either 'w' or 'b'
    '''
    if player != 'w' and player != 'b':
        raise ValueError("player must be either 'b' or 'w'")

    instance = StoreTileChanged.get_instance()
    instance.player = player

def get_player_played():
    '''
    Function: get_player_played
        getter
    Parameter, Possible Error raised:
        none
    Returns:
        the player, a char string of either 'b' or 'w'
    '''

    instance = StoreTileChanged.get_instance()
    return instance.player