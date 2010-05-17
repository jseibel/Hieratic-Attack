#WaveMeter is a visual cue for timing and contents of the next wave of enemies

from Enemy import Enemy
import pygame
from pygame.locals import *
from sys import exit

class WaveMeter(object):
    
    def __init__(self,waves,between,first_wave_time,wave_descriptions):
        #visual surface of meter
        self.background = pygame.Surface((15,600))
        self.background.fill((69,59,255))
        #total number of waves for the meter
        self.waves = waves
        #time between waves
        self.between = between
        #load all possible monster images
        self.scarab = pygame.image.load('IMG/scarab_meter.png').convert_alpha()
        self.falcon = pygame.image.load('IMG/falcon_meter.png').convert_alpha()
        self.wasp = pygame.image.load('IMG/wasp_meter.png').convert_alpha()
        self.eagle = pygame.image.load('IMG/eagle_meter.png').convert_alpha()
        self.mummy = pygame.image.load('IMG/mummy_meter.png').convert_alpha()
        self.anubis = pygame.image.load('IMG/anubis_meter.png').convert_alpha()
        self.lion = pygame.image.load('IMG/lion_meter.png').convert_alpha()

        self.current_wave = 0
        self.elapsed_time = 0.0
        self.first = first_wave_time
        self.current_enemy = Enemy
        self.wave_descriptions = wave_descriptions
    
    #returns visual of the wave meter for display
    def getMeter(self,time_change):
        self.elapsed_time += time_change
        meter = pygame.Surface((15,600)) 
        meter.blit(self.background,(0,0))
        
        i = 0
        while (i < self.waves):
            #wave_time = self.first + (self.between * i)
            wave_time = (self.between * i)
            if (wave_time > self.elapsed_time) and (wave_time < self.elapsed_time + 60.0):
                y_loc = (600*(wave_time - self.elapsed_time) / 60.0)
                img = pygame.image.load('IMG/'+self.wave_descriptions[i]+'_meter.png').convert_alpha()
                meter.blit(img,(-3,y_loc))
            i += 1
                
        return meter
