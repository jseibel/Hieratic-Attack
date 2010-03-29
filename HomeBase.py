#Home Base for defense, end of enemy movement path

from Tile import Tile
import pygame
from pygame.locals import *

class HomeBase(Tile):
        
    def __init__(self,i,j):
        Tile.__init__(self)
    
        self.kind = 'home base'
        self.next = None
        self.dir = ''
        self.loc = (i,j)
        self.pic = pygame.Surface((30,30)).convert()
        self.pic.fill((0,105,40))
        self.pic1 = pygame.image.load('IMG/hut.png').convert_alpha()
        self.pic.blit(self.pic1, (0,0))
        
    def update_pic(self, a, b):
        return None
