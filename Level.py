#Level class stores level-specific information, loaded from LEVEL file

import pygame
from pygame.locals import *

class Level(object):

    def __init__(self):
        self.music_name = ''
        self.map_name = ''
        self.level_image = ''
        self.wave_max = 0
        self.first_wave_time = 0
        self.wave_time = 0
        self.start_res = 0
        self.tower_d = 3
        self.sm_upgrade_d = 3
        self.lg_upgrade_d = 3
        
    def load(self,number):
        source = file('LEVEL/' + str(number) + '.level')
        self.music_name = str('MUSIC/' + source.readline().rstrip())
        self.map_name = 'MAP/' + str(number) + '.map'
        self.level_image = 'IMG/level_' + str(number) + '_100.png'
        self.wave_max = int(source.readline())
        self.first_wave_time = int(source.readline())
        self.wave_time = int(source.readline())
        self.start_res = int(source.readline())
        self.tower_d = int(source.readline())
        self.sm_upgrade_d = int(source.readline())
        self.lg_upgrade_d = int(source.readline())
