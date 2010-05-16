#radial menu for tower building/upgrading

import pygame
frompygame.locals import *

class RadialMenu(object):

    def __init__(self):
        self.dam_radial = pygame.image.load('IMG/dam_radial.png').convert()
        self.tower1_radial = pygame.image.load('IMG/tower1_radial.png').convert()
        self.tower2_radial = pygame.image.load('IMG/tower2_radial.png').convert()
        self.tower3_radial = pygame.image.load('IMG/tower3_radial.png').convert()
        self.choices = list()
        self.location = (0,0)
   
    def NewMenu(self,center_tile,loc):
        self.choices = list()
        self.location = loc
        if center_tile.kind == 'road':
            self.choices.append(('Build Basic Tower',self.tower1_radial))
        elif center_tile.kind == 'tower':
            if center_tile.title == 'Basic Tower':
                self.choices.append(('Upgrade Tower',self.tower1_radial))
                self.choices.append(('Upgrade to Rapid Tower',self.tower2_radial))
                self.choices.append(('Upgrade to Sniper Tower',self.tower3_radial))
            elif center_tile.title == 'Rapid Tower':
                self.choices.append(('Upgrade Tower',self.tower2_radial))
            elif center_tile.title == 'Sniper Tower':
                self.choices.append(('Upgrade Tower',self.tower3_radial))
        elif center_tile.kind == 'road':
            self.choices.append(('Build Dam',self.dam_radial))

    def GetChoices(self):
        return self.choices

    def GetChoice(self,loc):
        selection = (0,0)
        if loc[0] > (self.location-20) and loc[0] <= 
