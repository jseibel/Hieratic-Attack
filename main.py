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
font = pygame.font.SysFont("arial",18)
font_height = font.get_linesize()

#initialized to play sounds
pygame.mixer.init()
music = None

#allows for keys to be held down and repeating function
pygame.key.set_repeat(200,75)

#display object
game_display = Display(screen)
#resource object
resources = Resources()

#game is valid
game = True
end = False



#clock object for movement, (currently limited to 40 fps)
clock = pygame.time.Clock()
resources.time = clock.tick(40)

#tracks current text line
text_y = 0
#typer
#typebox_x = 100
#typebox_y = 100
time_type = 0


#computes distance between two points
#   input pixel location tuple for two objects
def dist(a,b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    return math.sqrt( x**2 + y**2 )

level = 1
unloaded = True
help = False


#start menu loop
while resources.game_state == 'start_menu':
    
    resources.time = clock.tick(40)/1000.0
    resources.frame+= 1

    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        else:
            handle(event,resources)

    game_display.update_view(resources)
    screen.blit(game_display.background,(0,0))
            
    pygame.display.flip()

#main game loop
while resources.game_state != 'end':
    if resources.game_state == 'loading':
        #game is over
        if level == 9:
            resources.game_state = 'end'
        #load next level
        else:
            #load resources to the level
            resources.load(level)
            
            #play music
            music = pygame.mixer.Sound(resources.music_name)
            music.play(-1)
            
            #reset timer
            clock = pygame.time.Clock()
            resources.time = clock.tick(40)
            
            
            #return to main game look
            resources.game_state = 'main'

    #display help menu
    while help:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    help = False
            if event.type == MOUSEBUTTONDOWN:
                help = False

        screen.blit(resources.help_screen,(0,0))
        pygame.display.flip()
        
    #get user input
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
        #update current tile based on mouse or keyboard
        if event.type == MOUSEMOTION:
            new_loc = pygame.mouse.get_pos()
            if (15 <= new_loc[0] < 615) and (0 <= new_loc[1] < 600):
                resources.curr_x = (new_loc[0]-15)/30
                resources.curr_y = (new_loc[1])/30
        #get keyboard input if typer is active
        if resources.typer.active:
            if event.type == KEYDOWN:
                key = pygame.key.name(event.key)
                if event.key == K_SPACE:
                    key = ' '
                if resources.typer.put(key):
                    resources.typer.type_complete(resources)
                if event.key == K_ESCAPE:
                    resources.typer.kill()
        elif event.type == KEYDOWN:
            #move selected square with WASD or arror keys
            if (event.key == K_DOWN or event.key == K_s) and resources.curr_y < 570: 
                resources.curr_y+= 1
            if (event.key == K_UP or event.key == K_w) and resources.curr_y > 0:
                resources.curr_y-= 1
            if (event.key == K_RIGHT or event.key == K_d) and resources.curr_x < 570:
                resources.curr_x+= 1
            if (event.key == K_LEFT or event.key == K_a) and resources.curr_x > 0:
                resources.curr_x-= 1
            
            #upgrade a tower at current location
            if event.key == K_u:
                if resources.res >= 80:
                    current_tile = resources.grid[resources.curr_y][resources.curr_x]
                    if (current_tile.kind == 'tower' and current_tile.upgrades < 10):
                        pygame.mouse.set_visible(False)
                        resources.typer = Typer('DICT/1','upgrade',1,resources.curr_y, resources.curr_x)
                        resources.typing_timer = -1
            
            #builds a tower at current location
            if event.key == K_r:
                if resources.res >= 150:
                    if (resources.grid[resources.curr_y][resources.curr_x].kind == 'grass'):
                        pygame.mouse.set_visible(False)
                        resources.typer = Typer('DICT/1','tower',2,resources.curr_y, resources.curr_x)
                        resources.typing_timer = -1
            
            #upgrade tower to rapid-fire 
            if event.key == K_t:
                if resources.res >= 300:
                    current_tile = resources.grid[resources.curr_y][resources.curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            resources.typer = Typer('DICT/1','rapid',3,resources.curr_y,resources.curr_x)
                            resources.typing_timer = -1
            
            #upgrade tower to sniper
            if event.key == K_y:
                if resources.res >= 500:
                    current_tile = resources.grid[resources.curr_y][resources.curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            resources.typer = Typer('DICT/1','snipe',3,resources.curr_y,resources.curr_x)
                            resources.typing_timer = -1
            
            #build a dam
            if event.key == K_e:
                if resources.res >= 50:
                    current_tile = resources.grid[resources.curr_y][resources.curr_x]
                    if (current_tile.kind == 'road'):
                        pygame.mouse.set_visible(False)
                        resources.typer = Typer('DICT/1','dam',1,resources.curr_y,resources.curr_x)     
                        resources.typing_timer = -1
            #show help menu    
            if event.key == K_h:
                help = True


    if resources.typer.active:
        resources.typing_timer+= resources.time
    
    #find time passed since last frame (maxing at 40 fps)
    resources.time = clock.tick(40)/1000.0
    resources.frame+= 1
    
    
    
    
    #adds a resource every second
    if (resources.frame % 40) == 0:
        resources.res+= 1
        
    
    #sends a new enemy (if not at max) every 0.5 second
    if (resources.frame%20) == 0 and resources.enemy < resources.enemy_max :
        resources.enemies[resources.enemy] = Enemy(resources.enemy_level, resources.the_map.path, level)
        resources.enemy+= 1
    
    #special speed waves
    if level == 7:
        if (resources.frame % resources.wave_time) == 0:
            resources.enemy_max+=1
            resources.enemy_level+=1
            resources.frame = 0
    elif (resources.enemy_level == 0):
        if resources.frame % resources.first_wave_time == 0:
            resources.enemy_max+= 10
            resources.enemy_level+= 1
            resources.frame = 0
    elif level == 4 and resources.enemy_level == 15:
        if (resources.frame % resources.wave_time) == 0:
            resources.enemy_max+=1
            resources.enemy_level+=1
            resources.frame = 0
    elif level == 8 and resources.enemy_level == 25:
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
    
    #update screen
    game_display.update_view(resources)
    screen.blit(game_display.background, (0,0))
    #show game over screen if enemy reaches end
    if end:
        screen.blit(resources.the_end, (0,0))
    #draw updated screen
    pygame.display.flip()        
    #determine if level is complete and load next level
    if (num_alive == 0) and resources.enemy_level == resources.wave_max:
        end_level = True
        level+=1
        pygame.mixer.stop()
        while end_level:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        end_level = False
                if event.type == MOUSEBUTTONDOWN:
                    end_level = False
            
            screen.blit(resources.level_finish, (0,0))
            pygame.display.flip()
        unloaded = True
        screen.blit(resources.loading,(0,0))
        pygame.display.flip()
    
        
    
#game over screen
while end:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                exit()
            if event.key == K_ESCAPE:
                exit()
