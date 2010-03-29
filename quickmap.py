#Program will display a map view read from a text file
#test class to view map design, not used in game

import pygame
from pygame.locals import *
from Field import Field
import sys

filename = sys.argv[1]      #read command line argument for map file name
source = file(filename)

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption(filename)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(((255, 255, 255)))

the_map = Field(filename)
map_surface = the_map.get_map().convert()
background.blit(map_surface, (0,0))

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    screen.blit(background, (0,0))
    pygame.display.flip()
