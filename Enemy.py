#base enemy class, will be expanded upon in the future once enemies are decided

import pygame
from pygame.locals import *

class Enemy(object):

    #takes path from map as constructor
    def __init__(self,enemy_type,level,path,world_level):
        
        self.path = path
        #starts at enemy base
        self.tile = path[0]
        self.next_tile = path[1]
        #tracks path tile index
        self.path_num = 0
        #location of center in actual pixels
        self.loc = ((self.tile.loc[1]+1)*30, self.tile.loc[0]*30+15)
        #movement speed of enemy in pixels/second
        self.speed = 50
        self.type = enemy_type
        self.pic = pygame.image.load( ('IMG/' + self.type + '_east.png') ).convert_alpha()
        #tracks dist moved in actual pixels
        self.pixel_moved = 0.0
        self.alive = True
        #tracks current hp
        self.level = level
        self.world = world_level

        #enemy defined by level 
        #TODO - move enemy stat definition into level resource
        if self.world == 1:
            self.hp = (level+1) * 5.0
                  
        elif self.world == 2:
            if self.level < 10:
                self.hp = (level+1) * 5.0
            else:
                self.hp = 50 + ((self.level-9) * 8.0)
                self.speed = 60
                      
        elif self.world == 3:
            if self.level < 10:
                self.hp = (self.level+1)*8.0
                self.speed = 60
            else:
                self.hp = 80 + ((self.level-9) * 10.0)
                
        elif self.world == 4:
            if self.level < 5:
                self.hp = (self.level+1)*8.0
                self.speed = 60
            elif self.level < 10:
                self.hp = 80 + ((self.level-4) * 10.0)
                self.speed = 60
            elif self.level < 15:
                self.hp = 120 + ((self.level-9) * 15.0)
            elif self.level == 15:
                self.hp = 1000
                self.speed = 40
            
        
        elif self.world == 5:
            if self.level < 10:
                self.hp = (self.level+1)*8.0
                self.speed = 60
            else:
                self.hp = 80 + ((self.level-9) * 10.0)
                
                
        elif self.world == 6:
            if self.level < 5:
                self.hp = (self.level+1)*8.0
                self.speed = 60
            elif self.level < 10:
                self.hp = 40 + ((self.level-4) * 15.0)
            else:
                self.hp = 90 + ((self.level-9) * 18.0)
                
        elif self.world == 7:
            self.hp = 1000
            
                
        elif self.world == 8:
            if self.level < 5:
                self.hp = (self.level+1)*8.0
                self.speed = 50
            elif self.level < 10:
                self.hp = 40 + ((self.level-4) * 8.0)
                self.speed = 60
            elif self.level < 15:
                self.hp = 80 + ((self.level-9) * 10.0)
                self.speed = 60
            elif self.level < 20:
                self.hp = 130+((self.level-14) * 12.0)
                self.speed = 50
            elif self.level < 25:
                self.hp = 190+((self.level-14) * 10.0)
                self.speed = 50
            else:
                self.hp = 1000
                self.speed = 40
                    
        
        if level == 9 or level == 18 or level == 27:
            self.speed = 120
            self.hp = int(self.hp/3)
        #stores reward for killing
        self.reward = self.hp/3
        
        
    
    #moves enemy by pixels based on time passed
    def move(self, time):
        if self.alive:
            if self.next_tile.kind != 'dam':        
                self.pixel_moved+= self.speed * time
            
            
            if self.pixel_moved >= 30:
                self.path_num+= 1
                self.tile = self.path[self.path_num]
                if len(self.path) > self.path_num+1:
                    self.next_tile = self.path[self.path_num+1]
                self.pixel_moved = 0.0
            
            #only scarabs have north and south images    
            if self.tile.dir == 'north':
                self.loc = ((self.tile.loc[1]+1)*30, self.tile.loc[0]*30+15-self.pixel_moved)
                if self.type == 'scarab':
                    self.pic = pygame.image.load('IMG/scarab_north.png').convert_alpha()
                    
        
            elif self.tile.dir == 'south':
                self.loc = ((self.tile.loc[1]+1)*30, self.tile.loc[0]*30+15+self.pixel_moved)
                if self.type == 'scarab':
                    self.pic = pygame.image.load('IMG/scarab_south.png').convert_alpha()
                
        
            elif self.tile.dir == 'east':
                self.loc = ((self.tile.loc[1]+1)*30+self.pixel_moved, self.tile.loc[0]*30+15)
                self.pic = pygame.image.load('IMG/'+self.type+'_east.png').convert_alpha()
            
            elif self.tile.dir == 'west':
                self.loc = ((self.tile.loc[1]+1)*30-self.pixel_moved, self.tile.loc[0]*30+15)
                self.pic = pygame.image.load('IMG/'+self.type+'_west.png').convert_alpha()
        
    
    #returns coordinates for drawing to screen based on center
    def draw_coords(self):
        out = (self.loc[0]-15, self.loc[1]-15)
        return out
        
        
