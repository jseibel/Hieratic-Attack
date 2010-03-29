#road tile to create path for enemies
#   Note - Using the undirected road will cause maps to improperly build

from Tile import Tile
import pygame
from pygame.locals import *


class Road(Tile):
    
    #constructor takes map location i=row and j=column
    def __init__(self,i,j):
        Tile.__init__(self)
        self.kind = 'road'
        self.dir = None
        self.loc = (i,j)
        self.next = None
        self.dam = False
        self.pic = pygame.image.load('IMG/sand.png').convert()
    
    #determine road image based on previous road in the chain
    def upd_pic(self,last):
        
        if self.dir == 'east':
            if (last == 'east'):
                self.pic.blit((pygame.image.load('IMG/water_we.png').convert_alpha()),(0,0))
            elif (last == 'south'):
                self.pic.blit((pygame.image.load('IMG/water_ne.png').convert_alpha()),(0,0))
            elif (last == 'north'):
                self.pic.blit((pygame.image.load('IMG/water_es.png').convert_alpha()),(0,0))
        elif self.dir == 'north':
            if (last == 'west'):
                self.pic.blit((pygame.image.load('IMG/water_ne.png').convert_alpha()),(0,0))
            elif (last == 'north'):
                self.pic.blit((pygame.image.load('IMG/water_ns.png').convert_alpha()),(0,0))
            elif (last == 'east'):
                self.pic.blit((pygame.image.load('IMG/water_nw.png').convert_alpha()),(0,0))
        elif self.dir == 'south':
            if (last == 'west'):
                self.pic.blit((pygame.image.load('IMG/water_es.png').convert_alpha()),(0,0))
            elif (last == 'south'):
                self.pic.blit((pygame.image.load('IMG/water_ns.png').convert_alpha()),(0,0))
            elif (last == 'east'):
                self.pic.blit((pygame.image.load('IMG/water_ws.png').convert_alpha()),(0,0))
        elif self.dir == 'west':
            if (last == 'north'):
                self.pic.blit((pygame.image.load('IMG/water_ws.png').convert_alpha()),(0,0))
            elif (last == 'south'):
                self.pic.blit((pygame.image.load('IMG/water_nw.png').convert_alpha()),(0,0))
            elif (last == 'west'):
                self.pic.blit((pygame.image.load('IMG/water_we.png').convert_alpha()),(0,0))


class RoadToEast(Road):
    
    def __init__(self,i,j):
        Road.__init__(self,i,j)
        self.next = (self.loc[0], self.loc[1]+1)
        self.dir = 'east'
        
    

class RoadToNorth(Road):
    
    def __init__(self,i,j):
        Road.__init__(self,i,j)
        self.next = (self.loc[0]-1, self.loc[1])
        self.dir = 'north'


class RoadToSouth(Road):
    
    def __init__(self,i,j):
        Road.__init__(self,i,j)
        self.next = (self.loc[0]+1, self.loc[1])
        self.dir = 'south'

class RoadToWest(Road):
    
    def __init__(self,i,j):
        Road.__init__(self,i,j)
        self.next = (self.loc[0], self.loc[1]-1)
        self.dir = 'west'
        


