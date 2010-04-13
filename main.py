#   Main driver program for the game

import pygame
from pygame.locals import *
from Field import Field
from sys import exit
from Display import Display
from Enemy import Enemy
from Typer import Typer
from Resources import Resources
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
resources = Resources()


#clock object for movement, (currently limited to 40 fps)
clock = pygame.time.Clock()
resources.time = clock.tick(40)


#computes distance between two points
#   input pixel location tuple for two objects
def dist(a,b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    return math.sqrt( x**2 + y**2 )

#main game loop
while True:
    if resources.game_state == 'loading':
        #game is over
        if resources.level == 9:
            resources.game_state = 'end'
        #load next level
        else:
            #load resources for the current resources.level
            resources.load()
            
            #play music
            music = pygame.mixer.Sound(resources.music_name)
            music.play(-1)
            
            #reset timer
            clock = pygame.time.Clock()
            resources.time = clock.tick(40)
            
            
            #return to main game look
            resources.game_state = 'main'


    for event in pygame.event.get():
        handle(event,resources)

    if resources.game_state == 'main':

        if resources.typer.active:
            resources.typing_timer+= resources.time
        
        
        #adds a resource every second
        if (resources.frame % 40) == 0:
            resources.res+= 1
        
            
    #TODO - move all enemy creation garbage out of main
        #sends a new enemy (if not at max) every 0.5 second
        if (resources.frame%20) == 0 and resources.enemy < resources.enemy_max :
            resources.enemies[resources.enemy] = Enemy(resources.enemy_level, resources.the_map.path, resources.level)
            resources.enemy+= 1
        
        #special speed waves
        if resources.level == 7:
            if (resources.frame % resources.wave_time) == 0:
                resources.enemy_max+=1
                resources.enemy_level+=1
                resources.frame = 0
        elif (resources.enemy_level == 0):
            if resources.frame % resources.first_wave_time == 0:
                resources.enemy_max+= 10
                resources.enemy_level+= 1
                resources.frame = 0
        elif resources.level == 4 and resources.enemy_level == 15:
            if (resources.frame % resources.wave_time) == 0:
                resources.enemy_max+=1
                resources.enemy_level+=1
                resources.frame = 0
        elif resources.level == 8 and resources.enemy_level == 25:
            if (resources.frame % resources.wave_time) == 0:
                resources.enemy_max+=1
                resources.enemy_level+=1
                resources.frame = 0
        elif (resources.frame % resources.wave_time) == 0 and resources.enemy_level < resources.wave_max:
            resources.enemy_max+= 10
            resources.enemy_level+= 1
            resources.frame = 0
        
        #all towers within range of enemy fire at first available
        for i in resources.towers:
            for j in resources.enemies:
                if resources.enemies[j].alive:
                    if dist(resources.towers[i].center,resources.enemies[j].loc) <= resources.towers[i].range and resources.towers[i].cool <= 0:
                        resources.towers[i].fire(resources.enemies[j],resources.enemies,j)
                        if resources.enemies[j].hp <= 0:
                            resources.enemies[j].alive = False
                            resources.res+= resources.enemies[j].reward

        #update dams on the map
        resources.the_map.update_dams(resources.time)
        
        #kills all enemies that reach the end
        num_alive = 0
        for i in resources.enemies:
            if resources.enemies[i].tile.kind == 'home base':
                resources.enemies[i].alive = False
                game = False
                end = True
                
            elif resources.enemies[i].alive:
                resources.enemies[i].move(resources.time)
                num_alive+= 1

        #determine if level is complete and load next level
        if (num_alive == 0) and resources.enemy_level == resources.wave_max:
            resources.game_state = 'end_level'
            resources.level+=1
            pygame.mixer.stop()

    #find time passed since last frame (maxing at 40 fps)
    resources.time = clock.tick(40)/1000.0
    resources.frame+= 1
    
    #update screen
    game_display.update_view(resources)
    #draw updated screen
    pygame.display.flip()





