#typing class

import pygame
from pygame.locals import *
from sys import exit
from math import *
import random
import os


class Typer(object):

    def __init__(self,filename,use,num,y,x):
        #define font
        self.font = pygame.font.SysFont('arial',16)
        self.font_height = self.font.get_linesize()
        self.word = ''
        # x,y for drawing the box
        self.x = x
        self.y = y
        # what is being upgraded
        self.type = use
        #number of words to grab
        self.num = num
        self.text_color = (0,0,0)
        self.back_color = (255,180,75)
        i = 0
        #grab number of words from file
        while i < self.num:
            temp = ''
            while( len(temp) <= 1 ):
                temp = self.get_word(filename)
            temp = temp.strip()
            if i > 0:
                self.word = temp + ' ' + self.word
            else:
                self.word = temp
            i+= 1
            

        self.word = self.word.strip()
        self.active = True
        #create visual surface
        self.surface = pygame.Surface(((self.num+1)*(50),(self.font_height*2+2))).convert()
        self.surface.fill(self.back_color)
        self.surface.blit(self.font.render(self.word,True,self.text_color),(0,0))

        #tracks user correct, incorrect, and current typed string
        self.correct = 0
        self.out = ''
        self.next = self.word[self.correct]
        self.wrong = 0
        
    #get a random word from file
    def get_word(self,filename):
    
        offset = random.randint(0,os.stat(filename)[6])
        fd = file(filename,'rb')
        fd.seek(offset)
        fd.readline()
        return fd.readline()

    #check if character is correct
    def put(self, char):
        if (char == self.word[self.correct]):
            self.correct+=1
            self.out+= char
            #self.next = self.word[self.correct]
            self.complete()
        else:
            self.wrong+= 1
        return self.complete()
    
    #check if all words have been typed
    def complete(self):
        if self.correct == len(self.word):
            self.active = False
            return True
        else:
            return False
    
    #returns visual of the typing box for display
    def get_display(self,time):
        top = self.word + '  ' + '%.1f' % time
        self.surface.fill(self.back_color)
        self.surface.blit(self.font.render(top,True,self.text_color),(1,1))
        self.surface.blit(self.font.render(self.out,True,self.text_color),(1,self.font_height+1))
        
        return self.surface
        
    def kill(self):
        self.active = False
        
        
    
