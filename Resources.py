#Level class stores level-specific game information

import pygame
from pygame.locals import *
from Field import Field
from Typer import Typer
from WaveMeter import WaveMeter

class Resources(object):

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

        self.level = 1

        self.game_state = 'start_menu'
        #reset all main variables

        #current user cursor (x,y)
        self.curr_x = 0
        self.curr_y = 0
        #display frame counter
        self.frame = 0
        #total number of enemies sent
        self.enemy = 0
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
    def load(self,number):
        source = file('LEVEL/' + str(number) + '.level')
        self.music_name = str('MUSIC/' + source.readline().rstrip())
        self.wave_max = int(source.readline())
        self.first_wave_time = int(source.readline())
        self.wave_time = int(source.readline())
        self.res = int(source.readline())
        self.tower_d = int(source.readline())
        self.sm_upgrade_d = int(source.readline())
        self.lg_upgrade_d = int(source.readline())

        #initialize map from newly loaded resources
        self.the_map = Field('MAP/' + str(number) + '.map')
        self.map_surface = self.the_map.get_map().convert()
        self.grid = self.the_map.get_grid()
        self.towers = self.the_map.towers
        self.enemies = dict()
        self.meter = WaveMeter(self.wave_max,(self.wave_time/40),(self.first_wave_time/40),number)

        #reset all main variables
        self.curr_x = 0
        self.curr_y = 0
        self.current_level = pygame.image.load('IMG/level_' + str(number) + '_100.png').convert_alpha() 
        self.frame = 0
        self.enemy = 0
        self.enemy_max = 0
        self.enemy_level = 0
            


















        
