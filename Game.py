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
        #starting player self
        self.start_res = 0
        #letter length for words in typer
        self.basic_tower_d = 3
        self.adv_tower_d = 3
        self.upgrade_d = 3
        self.enemy_wave_description = list()

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
        self.typer = Typer(3,None,1,0,0)
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
            self.upgrade_d = int(source.readline())
            self.basic_tower_d = int(source.readline())
            self.adv_tower_d = int(source.readline())
            i = 0
            line = source.readline()
            line = line.split()
            num_waves = int(line[0])
            wave_type = line[1]
            while (i < self.wave_max):
                if i == num_waves:
                    line = source.readline()
                    line = line.split()
                    num_waves = int(line[0])
                    wave_type = line[1]
                self.enemy_wave_description.append(wave_type)
                i += 1
                    

            #initialize map from newly loaded self
            self.the_map = Field('MAP/' + str(self.level) + '.map')
            self.map_surface = self.the_map.get_map().convert()
            self.grid = self.the_map.get_grid()
            self.towers = self.the_map.towers
            self.enemies = dict()
            self.meter = WaveMeter(self.wave_max,(self.wave_time/40),(self.first_wave_time/40),self.enemy_wave_description)

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
                self.enemies[self.enemy_sent] = Enemy(self.enemy_wave_description[self.enemy_level],self.enemy_level, self.the_map.path, self.level)
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
        
        
    def ActivateTyper(self,x,y,typer_type):
        if typer_type == 'upgrade' and self.res >= 80:
            current_tile = self.grid[y][x]
            if (current_tile.kind == 'tower' and current_tile.upgrades < 10):
                pygame.mouse.set_visible(False)
                self.typer = Typer(self.upgrade_d,'upgrade',1,y,x)
                self.typing_timer = -1
        elif typer_type == 'tower' and self.res >= 150:
            current_tile = self.grid[y][x]
            if (current_tile.kind == 'grass'):
                pygame.mouse.set_visible(False)
                self.typer = Typer(self.basic_tower_d,'tower',2,y,x)
                self.typing_timer = -1
        elif typer_type == 'rapid' and self.res >= 300:
            current_tile = self.grid[y][x]
            if (current_tile.kind == 'tower' and current_tile.title == 'Basic Tower'):
                pygame.mouse.set_visible(False)
                self.typer = Typer(self.adv_tower_d,'rapid',3,y,x)
                self.typing_timer = -1
        elif typer_type == 'snipe' and self.res >= 500:
            current_tile = self.grid[y][x]
            if (current_tile.kind == 'tower' and current_tile.title == 'Basic Tower'):
                pygame.mouse.set_visible(False)
                self.typer = Typer(self.adv_tower_d,'snipe',3,y,x)
                self.typing_timer = -1
        elif typer_type == 'dam' and self.res >= 50:
            current_tile = self.grid[y][x]
            if (current_tile.kind == 'road'):
                pygame.mouse.set_visible(False)
                self.typer = Typer(self.upgrade_d,'dam',1,y,x)
                self.typing_timer = -1
        
        


    #execute on completion of a typing challenge
    def TypeComplete(self):
        if self.typer.type == 'tower':
            self.the_map.add_tower(self.typer.y,self.typer.x)
            tower = self.grid[self.typer.y][self.typer.x]
            tower.skill_modifier(self.typer.wrong,self.typing_timer)
            self.res-= 150
        elif self.typer.type == 'upgrade':
            current_tile = self.grid[self.typer.y][self.typer.x]
            current_tile.upgrade(self.typer.wrong,self.typing_timer)
            self.res-= 80
        elif self.typer.type == 'rapid':
            tower = self.grid[self.typer.y][self.typer.x]
            tower.rapid_upgrade(self.typer.wrong,self.typing_timer)
            self.res-= 300
        elif self.typer.type == 'snipe':
            tower = self.grid[self.typer.y][self.typer.x]
            tower.snipe_upgrade(self.typer.wrong,self.typing_timer)
            self.res-= 500
        elif self.typer.type == 'dam':
            self.the_map.add_dam(self.typer.y,self.typer.x)
            self.res-= 50


    def KillTyper(self):
        self.typer.kill()





        
