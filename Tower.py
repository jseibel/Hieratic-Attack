import pygame
from pygame.locals import *
import random
from math import fabs



class Tower(object):

    def __init__(self,i,j):
        #kind of tile
        self.kind = 'tower'
        self.title = 'Basic Tower'
        #map tile location
        self.loc = (j*30,i*30)
        #center pixel on map for distance calculations
        self.center = ((j+1)*30,i*30+15)
        #damage done per shot
        self.damage = 5.0
        #damage done by tower overall
        self.totaldmg = 0
        #rate of fire
        self.rate = 1.0
        #tracks cooldown time on fire
        self.cool = 0
        #range of attack
        self.range = 90
        #number of upgrades
        self.upgrades = 0
        #splash radius
        self.splash = 0
        
        self.basic_100 = pygame.image.load('IMG/tower1_100.png').convert_alpha()
        self.basic_80 = pygame.image.load('IMG/tower1_80.png').convert_alpha()
        self.basic_60 = pygame.image.load('IMG/tower1_60.png').convert_alpha()
        self.basic_40 = pygame.image.load('IMG/tower1_40.png').convert_alpha()
        
        self.rapid_100 = pygame.image.load('IMG/tower2_100.png').convert_alpha()
        self.rapid_80 = pygame.image.load('IMG/tower2_80.png').convert_alpha()
        self.rapid_60 = pygame.image.load('IMG/tower2_60.png').convert_alpha()
        self.rapid_40 = pygame.image.load('IMG/tower2_40.png').convert_alpha()
        
        self.snipe_100 = pygame.image.load('IMG/tower3_100.png').convert_alpha()
        self.snipe_80 = pygame.image.load('IMG/tower3_80.png').convert_alpha()
        self.snipe_60 = pygame.image.load('IMG/tower3_60.png').convert_alpha()
        self.snipe_40 = pygame.image.load('IMG/tower3_40.png').convert_alpha()
        
        self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
        self.pic.blit(self.basic_100,(0,0))
    
    def skill_modifier(self,wrong,time):
        self.rate = (time/2)-.75
        self.damage = 10-wrong
        self.range = int(self.range/self.rate)
        if self.rate < .75:
            self.rate = .75
        if self.rate > 1.5:
            self.rate = 1.5
        if self.range > 120:
            self.range = 120
        if self.range < 60:
            self.range = 60
        if self.damage < 5:
            self.damage = 5
        
    
    #basic firing at enemy, takes the enemy as argument, no armor calculation yet
    def fire(self,enemy,enemy_list,index):
    
        #enemy loses HP equal to weapon damage
        enemy.hp-= self.damage
        self.totaldmg+= self.damage
        
        #if 
        
        #makes enemy red over time
        #enemy.pic.fill((255,255*(enemy.hp/enemy.totalhp),255*(enemy.hp/enemy.totalhp)))
        #sets cooldown counter
        self.cool = self.rate
        #turns tower tile black to show on cooldown
        self.pic.fill((0,0,0))
        
    #lowers cooldown counter, slowly fades tower back into color
    def tick(self, time):
        
        self.cool-= time
        if self.cool < 0.0:
            self.cool = 0.0
            self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
            self.pic.blit(self.basic_40,(0,0))
        percent = (fabs(self.rate-self.cool)/self.rate)
        if self.title == 'Basic Tower':
            if percent < .30:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.basic_40,(0,0))
            elif percent < .60:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.basic_60,(0,0))
            elif percent < .95:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.basic_80,(0,0))
            else:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.basic_100,(0,0))
        elif self.title == 'Rapid Tower':
            if percent < .30:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.rapid_40,(0,0))
            elif percent < .60:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.rapid_60,(0,0))
            elif percent < .95:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.rapid_80,(0,0))
            else:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.rapid_100,(0,0))
        elif self.title == 'Sniper Tower':
            if percent < .30:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.snipe_40,(0,0))
            elif percent < .60:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.snipe_60,(0,0))
            elif percent < .95:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.snipe_80,(0,0))
            else:
                self.pic = self.pic = pygame.image.load('IMG/sand.png').convert()
                self.pic.blit(self.snipe_100,(0,0))
        
        #self.pic.fill((125*(fabs(self.rate-self.cool)/self.rate), 75*(fabs(self.rate-self.cool)/self.rate), 0))
        
    
    #returns a list of information about tower for display in game
    def get_info(self):
        
        out = list()
        out.append(self.title + " level " + str(self.upgrades))
        out.append('Damage: ' + str(self.damage))
        out.append('Rate: ' + '%.3f' % self.rate + ' sec.')
        out.append('Cooldown: ' + '%.1f' % self.cool)
        out.append('Range: ' + str(self.range))
        out.append('Damage done: ' + str(self.totaldmg))
        
        return out
        '''
    #upgrade the tower, random
    def upgrade(self):
        roll = random.randint(1,10)
        if roll <= 3:
            self.range += 5
        elif roll <= 6:
            self.rate *= .85
        elif roll <= 9: 
            self.damage+= 3
        elif roll == 10:
            self.damage += 5
            self.rate   *= .9
            self.range  += 3
        self.upgrades+= 1
        #self.title = 'Tower level : ' + str(self.upgrades)
        '''
    def upgrade(self,wrong,time):
        if wrong < 3:
            self.range += 10-(wrong*5)
        if time < .75:
            self.rate *= .9
        if wrong == 0 and time < 1.5:
            self.damage+= 3
        
        
        self.upgrades+= 1
        
    def rapid_upgrade(self,wrong,time):
        self.title = 'Rapid Tower'
        self.damage-= int(time/4.0) + int(wrong/2)
        #self.pic = 
        if (self.damage < 4):
            self.damage = 4
        self.range = self.range * .85
        if self.range < 50:
            self.range = 50
        self.rate = ((time-2.0)/10.0)
        if self.rate < .4:
            self.rate = .4
        if self.rate > 1.0:
            self.rate = 1.0
            
    def snipe_upgrade(self,wrong,time):
        self.title = 'Sniper Tower'
        self.damage = 100-(5*wrong)
        
        if (self.damage < 70):
            self.damage = 4
        
        self.range = 150-(5*wrong)
        self.rate = 5.0 + ((time-2)/8.0)
        
        if self.rate > 7.5:
            self.rate = 7.5
        
        
        
        
        
        
        
        
