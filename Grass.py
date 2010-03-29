#grass Tile, doesn't do anything

from Tile import Tile
import pygame
from pygame.locals import *
class Grass(Tile):

    def __init__(self):

        Tile.__init__(self)
        self.kind = 'grass'
        self.pic = pygame.image.load('IMG/sand.png').convert()
