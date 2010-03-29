#class for creating the field of play, reads a file of .map extension

from Road import *
from Grass import Grass
from HomeBase import HomeBase
from EnemyBase import *
from Tower import Tower
from Dam import Dam
import pygame
from pygame.locals import *
from sys import exit

class Field(object):
    
    def __init__(self,file_name):
        
        #tracks start and end tiles
        self.finish = None
        self.start = None
        self.source = file(file_name)
        
        #maps to 600x600 surface
        self.surface = pygame.Surface((600,600)).convert()
        #tracks all tiles by [row][column]
        self.grid = dict()
        #ordered path enemies follow
        self.path = list()
        #list of all towers on map
        self.towers = dict()
        #number of all towers for indexing
        self.tower_num = 0
        self.dams = list()
        
        #reads input line by line and fills in the grid
        for i in xrange(20):
            columns = dict()
            line = self.source.readline()
            line = line.split()
            
            for j in xrange(20):
                if(line[j] == 'G'):
                    columns[j] = Grass()
                    current_tile = columns[j]
                elif(line[j] == 'N'):
                    columns[j] = RoadToNorth(i,j)
                    current_tile = columns[j]
                elif(line[j] == 'S'):
                    columns[j] = RoadToSouth(i,j)
                    current_tile = columns[j]
                elif(line[j] == 'E'):
                    columns[j] = RoadToEast(i,j)
                    current_tile = columns[j]
                elif(line[j] == 'W'):
                    columns[j] = RoadToWest(i,j)
                    current_tile = columns[j]
                elif(line[j] == 'T'):
                    columns[j] = Tower(i,j)
                    current_tile = columns[j]
                    self.towers[self.tower_num] = columns[j]
                    self.tower_num+= 1
                elif(line[j] == 'A'):
                    columns[j] = EnemyToNorth(i,j)
                    current_tile = columns[j]
                    self.start = (i,j)
                elif(line[j] == 'B'):
                    columns[j] = EnemyToSouth(i,j)
                    current_tile = columns[j]
                    self.start = (i,j)
                elif(line[j] == 'C'):
                    columns[j] = EnemyToEast(i,j)
                    current_tile = columns[j]
                    self.start = (i,j)
                elif(line[j] == 'D'):
                    columns[j] = EnemyToWest(i,j)
                    current_tile = columns[j]
                    self.start = (i,j)
                elif(line[j] == 'H'):
                    columns[j] = HomeBase(i,j)
                    current_tile = columns[j]
                    self.finish = (i,j)
                
                self.surface.blit(current_tile.pic, (30*j,30*i))
                
            self.grid[i] = columns
                
        self.source.close()
        self.set_path()
        
        
    #returns the visual map
    def get_map(self):
        return self.surface
    
    #returns the physical tileset
    def get_grid(self):
        return self.grid
        

    #ticks the cooldown of all necessary towers and changes color accordingly
    def update_towers(self, time):
        for i in self.towers:
            if self.towers[i].cool > 0:
                self.towers[i].tick(time)
            self.surface.blit(self.towers[i].pic,(self.towers[i].loc[0],self.towers[i].loc[1]))
    
    
    def update_dams(self,time):
        for x in xrange(len(self.dams)):
            self.dams[x].update(time)
            if self.dams[x].valid == False:
                i = self.dams[x].loc[0]
                j = self.dams[x].loc[1]
                self.grid[i][j].kind = 'road'
                self.surface.blit(self.grid[i][j].pic,(30*j,30*i))
                
    
    
    #starts at enemy base and creates the path following roads to the home base
    def set_path(self):
        current_tile = self.grid[self.start[0]][self.start[1]]
        while current_tile.next != None:
            #print current_tile.dir
            self.path.append(current_tile)
            prev_dir = current_tile.dir
            current_tile = self.grid[current_tile.next[0]][current_tile.next[1]]
            if current_tile.next != None:
                current_tile.upd_pic(prev_dir)
                self.surface.blit(current_tile.pic, (30*current_tile.loc[1],30*current_tile.loc[0]))
        self.path.append(current_tile)
        
        
    #adds a tower to the map
    def add_tower(self,i,j):
        self.grid[i][j] = Tower(i,j)
        self.surface.blit(self.grid[i][j].pic, (30*j,30*i))
        self.towers[self.tower_num] = self.grid[i][j]
        self.tower_num+= 1
        
    def add_dam(self,i,j):
        self.grid[i][j].kind = 'dam'
        new_dam = Dam(i,j)
        self.dams.append(new_dam)
        self.surface.blit(new_dam.pic,(30*j,30*i))
