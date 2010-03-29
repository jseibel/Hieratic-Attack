#Starting tile for enemy path.  Similar to Road, enemies move in specific direction.

from Tile import Tile
import pygame
from pygame.locals import *

class EnemyBase(Tile):
        
    def __init__(self,i,j):
        Tile.__init__(self)
    
        self.kind = 'enemy base'
        self.loc = (i,j)
        self.next = None
        self.pic = pygame.Surface((30,30)).convert()
        self.pic.blit((pygame.image.load('IMG/pyramid.png').convert_alpha()), (-10,-10))
        
class EnemyToNorth(EnemyBase):
    
    def __init__(self,i,j):
        EnemyBase.__init__(self,i,j)
        self.next = (self.loc[0]-1, self.loc[1])
        self.dir = 'north'
        
class EnemyToSouth(EnemyBase):
    
    def __init__(self,i,j):
        EnemyBase.__init__(self,i,j)
        self.next = (self.loc[0]+1, self.loc[1])
        self.dir = 'south'

class EnemyToEast(EnemyBase):
    
    def __init__(self,i,j):
        EnemyBase.__init__(self,i,j)
        self.next = (self.loc[0], self.loc[1]+1)
        self.dir = 'east'

class EnemyToWest(EnemyBase):
    
    def __init__(self,i,j):
        EnemyBase.__init__(self,i,j)
        self.next = (self.loc[0], self.loc[1]-1)
        self.dir = 'west'

