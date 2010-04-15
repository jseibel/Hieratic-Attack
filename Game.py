#Game class serves as the data model got the game back-end

import pygame
from pygame.locals import *
from Field import Field
from Typer import Typer
from Enemy import Enemy
from WaveMeter import WaveMeter
import math

#computes distance between two points
#   input pixel location tuple for two objects
def dist(a,b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    return math.sqrt( x**2 + y**2 )

class Game(object):

    def __init__(self):
        #filename variables
        self.music_name = ''
        self.map_name = ''
        self.level_image = ''
        #total enemy waves
        self.wave_max = 0
        #time before first wave
        self.first_wave_time = 0
        #time between waves after first
        self.wave_time = 0
        #starting player resources
        self.start_res = 0
        #letter length for words in typer
        self.tower_d = 3
        self.sm_upgrade_d = 3
        self.lg_upgrade_d = 3

        self.level = 0

        self.game_state = 'start_menu'
        
        #display frame counter
        self.frame = 0
        #total number of enemies sent
        self.enemy_sent = 0
        #total number of enemies that needs to be sent
        self.enemy_max = 0
        #enemy level
        self.enemy_level = 0
        #user resource total
        self.res = 700

        #map for current level
        self.the_map = Field('MAP/1.map')
        self.map_surface = self.the_map.get_map().convert()
        self.grid = self.the_map.get_grid()
        self.towers = self.the_map.towers
        self.enemies = dict()

        #initialize typer
        self.typer = Typer('DICT/1',None,1,0,0)
        self.typer.kill()


        self.time = 0
        self.typing_timer = 0

        self.wave_meter = None
        
        #title screen images
        self.title1 = pygame.image.load('IMG/title1.png').convert()
        self.title2 = pygame.image.load('IMG/title2.png').convert()
        #game over image
        self.the_end = pygame.image.load('IMG/end.png').convert()

        self.res_img = pygame.image.load('IMG/res_75.png').convert_alpha()
        self.level_finish = pygame.image.load('IMG/level_finish.png').convert()
        self.loading = pygame.image.load('IMG/loading.png').convert_alpha()
        self.help_screen = pygame.image.load('IMG/help.png').convert()

    #load a new level
    def LoadNextLevel(self):
        self.level += 1
        if self.level < 9:
            source = file('LEVEL/' + str(self.level) + '.level')
            self.music_name = str('MUSIC/' + source.readline().rstrip())
            self.wave_max = int(source.readline())
            self.first_wave_time = int(source.readline())
            self.wave_time = int(source.readline())
            self.res = int(source.readline())
            self.tower_d = int(source.readline())
            self.sm_upgrade_d = int(source.readline())
            self.lg_upgrade_d = int(source.readline())

            #initialize map from newly loaded resources
            self.the_map = Field('MAP/' + str(self.level) + '.map')
            self.map_surface = self.the_map.get_map().convert()
            self.grid = self.the_map.get_grid()
            self.towers = self.the_map.towers
            self.enemies = dict()
            self.meter = WaveMeter(self.wave_max,(self.wave_time/40),(self.first_wave_time/40),self.level)

            #reset all main variables
            self.current_level = pygame.image.load('IMG/level_' + str(self.level) + '_100.png').convert_alpha() 
            self.frame = 0
            self.enemy_sent = 0
            self.enemy_max = 0
            self.enemy_level = 0
            
        else:
            self.game_state = 'end'


    def Update(self,time):
        self.time = time
        self.frame+= 1
        
        if self.game_state == 'main':
        
            #update typing time if active
            if self.typer.active:
                self.typing_timer+= self.time
                
            #adds a resource every second
            if (self.frame % 40) == 0:
                self.res+= 1
            
            #sends a new enemy (if not at max) every 0.5 second
            if (self.frame%20) == 0 and self.enemy_sent < self.enemy_max :
                self.enemies[self.enemy_sent] = Enemy(self.enemy_level, self.the_map.path, self.level)
                self.enemy_sent+= 1
            
            #adds another wave of enemies to be sent if time == wave_time
            if (self.frame % self.wave_time) == 0 and self.enemy_level < self.wave_max:
                self.enemy_max+= 10
                self.enemy_level+= 1
                self.frame = 0
            
            #all towers within range of enemy fire at first available
            all_dead = True
            for j in self.enemies:
                if self.enemies[j].alive:
                    all_dead = False
                    self.enemies[j].move(self.time)
                    for i in self.towers:
                        if dist(self.towers[i].center,self.enemies[j].loc) <= self.towers[i].range and self.towers[i].cool <= 0:
                            self.towers[i].fire(self.enemies[j],self.enemies,j)
                            if self.enemies[j].hp <= 0:
                                self.enemies[j].alive = False
                                self.res+= self.enemies[j].reward
                
                #if enemy has reached home base, end game
                if self.enemies[j].tile.kind == 'home base':
                    self.game_state = 'end'

            #update dams on the map
            self.the_map.update_dams(self.time)
            
            #if everything is dead and all waves sent, end level
            if all_dead and self.enemy_level == self.wave_max:
                self.game_state = 'end_level'
        
        if self.game_state == 'loading':
            #stop music
            pygame.mixer.stop()
            #load next level
            self.LoadNextLevel()
            #if game is not over play new music
            if self.game_state != 'end':
                music = pygame.mixer.Sound(self.music_name)
                music.play(-1)
                self.game_state = 'main'
        
        
    #def ActivateTyper(self,x,y,typer_type):
        











        
