#   Main driver program for the game

import pygame
from pygame.locals import *
from Field import Field
from sys import exit
from Display import Display
from Enemy import Enemy
from Typer import Typer
from Game import Game
import math
from Controller import *


#initialize pygame and display
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Be More Games')

#initialize font and track height
#font = pygame.font.SysFont("arial",18)
#font_height = font.get_linesize()

#initialized to play sounds
pygame.mixer.init()
music = None

#allows for keys to be held down and repeating function
pygame.key.set_repeat(200,75)

#display object
game_display = Display(screen)
#resource object
m_game = Game()


#clock object for movement, (currently limited to 40 fps)
clock = pygame.time.Clock()
m_game.time = clock.tick(40)


#computes distance between two points
#   input pixel location tuple for two objects
def dist(a,b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    return math.sqrt( x**2 + y**2 )

#main game loop
while True:
    if m_game.game_state == 'loading':
        #game is over
        if m_game.level == 9:
            m_game.game_state = 'end'
        #load next level
        else:
            #load next level
            m_game.LoadNextLevel()
            
            #play music
            music = pygame.mixer.Sound(m_game.music_name)
            music.play(-1)
            
            #reset timer
            clock = pygame.time.Clock()
            m_game.time = clock.tick(40)
            
            
            #return to main game look
            m_game.game_state = 'main'


    for event in pygame.event.get():
        handle(event,m_game)

    if m_game.game_state == 'main':

        if m_game.typer.active:
            m_game.typing_timer+= m_game.time
        
        
        #adds a resource every second
        if (m_game.frame % 40) == 0:
            m_game.res+= 1
        
            
    #TODO - move all enemy creation garbage out of main
        
        
        #special speed waves
        if m_game.level == 7:
            if (m_game.frame % m_game.wave_time) == 0:
                m_game.enemy_max+=1
                m_game.enemy_level+=1
                m_game.frame = 0
        elif (m_game.enemy_level == 0):
            if m_game.frame % m_game.first_wave_time == 0:
                m_game.enemy_max+= 10
                m_game.enemy_level+= 1
                m_game.frame = 0
        elif m_game.level == 4 and m_game.enemy_level == 15:
            if (m_game.frame % m_game.wave_time) == 0:
                m_game.enemy_max+=1
                m_game.enemy_level+=1
                m_game.frame = 0
        elif m_game.level == 8 and m_game.enemy_level == 25:
            if (m_game.frame % m_game.wave_time) == 0:
                m_game.enemy_max+=1
                m_game.enemy_level+=1
                m_game.frame = 0
        elif (m_game.frame % m_game.wave_time) == 0 and m_game.enemy_level < m_game.wave_max:
            m_game.enemy_max+= 10
            m_game.enemy_level+= 1
            m_game.frame = 0
        
        #all towers within range of enemy fire at first available
        for i in m_game.towers:
            for j in m_game.enemies:
                if m_game.enemies[j].alive:
                    if dist(m_game.towers[i].center,m_game.enemies[j].loc) <= m_game.towers[i].range and m_game.towers[i].cool <= 0:
                        m_game.towers[i].fire(m_game.enemies[j],m_game.enemies,j)
                        if m_game.enemies[j].hp <= 0:
                            m_game.enemies[j].alive = False
                            m_game.res+= m_game.enemies[j].reward

        #update dams on the map
        m_game.the_map.update_dams(m_game.time)
        
        #kills all enemies that reach the end
        num_alive = 0
        for i in m_game.enemies:
            if m_game.enemies[i].tile.kind == 'home base':
                m_game.enemies[i].alive = False
                game = False
                end = True
                
            elif m_game.enemies[i].alive:
                m_game.enemies[i].move(m_game.time)
                num_alive+= 1

        #determine if level is complete and load next level
        if (num_alive == 0) and m_game.enemy_level == m_game.wave_max:
            m_game.game_state = 'end_level'
            m_game.level+=1
            pygame.mixer.stop()

    #find time passed since last frame (maxing at 40 fps)
    m_game.Update( (clock.tick(40)/1000.0) )
    
    #update screen
    game_display.update_view(m_game)
    #draw updated screen
    pygame.display.flip()





