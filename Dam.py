import pygame
from pygame.locals import *

#dam class - prevents enemies from advancing for 6 seconds
class Dam(object):
    
    def __init__(self,i,j):
        self.pic = pygame.image.load('IMG/dam.png').convert_alpha()
        self.valid = True
        self.timer = 6.00
        self.loc = (i,j)
    
    #updates timer, invalidates after 6 seconds pass
    def update(self,time):
        self.timer-= time
        
        if self.timer <= 0:
            self.valid = False
            
    
