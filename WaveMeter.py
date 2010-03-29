#WaveMeter is a visual cue for timing and contents of the next wave of enemies

from Enemy import Enemy
import pygame
from pygame.locals import *
from sys import exit

class WaveMeter(object):
    
    def __init__(self,waves,between,first_wave_time,level):
        #visual surface of meter
        self.meter = pygame.Surface((15,600))
        self.background = pygame.Surface((15,600))
        self.background.fill((69,59,255))
        #total number of waves for the meter
        self.waves = waves+1      
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
        self.total_time = 0.0
        self.first = first_wave_time
        self.current_enemy = Enemy
        self.level = level
    
    #returns visual of the wave meter for display
    def getMeter(self,time_change,current_wave):
    
        if (self.current_wave == current_wave):
            self.total_time += time_change
        else:
            self.current_wave = current_wave
            self.total_time = time_change
            
        self.meter.blit(self.background,(0,0))
        
        #TODO - move hard coded monster waves to level resource
        if self.level == 1:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = (((wave-current_wave)*10.0 - self.total_time))*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        
                            
        if self.level == 2:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = (((wave-current_wave)*10.0 - self.total_time))*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
        
        if self.level == 3:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = (((wave-current_wave)*10.0 - self.total_time))*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
        
        
        if self.level == 4:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        elif wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 15:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.lion,(-3,y))
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        elif wave < 10:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 15:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.lion,(-3,y))
        
        
        if self.level == 5:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 10:
                            y = (((wave-current_wave)*10.0 - self.total_time))*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
        
        
        
        if self.level == 6:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.mummy ,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 10:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.mummy ,(-3,y))
        
        
        
        if self.level == 7:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                        self.meter.blit(self.lion,(-3,y))
                        
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                        self.meter.blit(self.lion,(-3,y))
        
        
        if self.level == 8:
            if current_wave == 0:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        elif wave < 10:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        elif wave < 15:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 20:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        elif wave < 25:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.mummy,(-3,y))
                        else:
                            y = ((wave-1)*10.0 + self.first - self.total_time)*10.0
                            self.meter.blit(self.anubis,(-3,y))
            else:
                for wave in xrange(self.waves):
                    if wave > current_wave:
                        if wave < 5:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.scarab,(-3,y))
                        elif wave < 10:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.wasp,(-3,y))
                        elif wave < 15:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.falcon,(-3,y))
                        elif wave < 20:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.eagle,(-3,y))
                        elif wave < 25:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.mummy,(-3,y))
                        else:
                            y = ((wave-current_wave)*10.0   - self.total_time)*10.0
                            self.meter.blit(self.anubis,(-3,y))
        
        return self.meter
