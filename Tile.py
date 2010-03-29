#overarching Tile class for map construction
#basis for Grass, Road, Tower, HomeBase, EnemyBase
class Tile(object):

    def __init__(self):
        
        
        #kind of tile
        self.kind = None
        #location on the grid
        self.location = None
        #list containing the units on this tile
        self.contains = None
        #graphical representation
        self.pic = None
