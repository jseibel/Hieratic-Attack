#   Main driver program for the game

import pygame
from pygame.locals import *
from Field import Field
from sys import exit
from Enemy import Enemy
from Typer import Typer
from WaveMeter import WaveMeter
from Level import Level
import math


#initialize pygame and display
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Be More Games')

#title screen images
title1 = pygame.image.load('IMG/title1.png').convert()
title2 = pygame.image.load('IMG/title2.png').convert()
the_end = pygame.image.load('IMG/end.png').convert()

res_img = pygame.image.load('IMG/res_75.png').convert_alpha()
level_finish = pygame.image.load('IMG/level_finish.png').convert()
loading = pygame.image.load('IMG/loading.png').convert_alpha()
help_screen = pygame.image.load('IMG/help.png').convert()

#level resource object
level_resource = Level()

#initialized to play sounds
pygame.mixer.init()
music = None


#initialize font and track height
font = pygame.font.SysFont("arial",18)
font_height = font.get_linesize()

#allows for keys to be held down and repeating function
pygame.key.set_repeat(200,75)

#initialize the background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(((255, 255, 255)))

#game is valid
game = True
end = False

#initialize the side info panel
panel = pygame.Surface((185,600))
panel = panel.convert()
panel.fill((75,75,75))

#build the map object from input file
the_map = Field('MAP/3.map')
#blit the visual representation to the background
map_surface = the_map.get_map().convert()
background.blit(map_surface, (15,0))

#quick tracking of tiles (organized as tile = grid[row][column])
grid = the_map.get_grid()
#list of all the towers
towers = the_map.towers
#list of all enemies
enemies = dict()

#clock object for movement, (currently limited to 40 fps)
clock = pygame.time.Clock()
time = clock.tick(40)

#tracks current grid highlight
curr_x = 0
curr_y = 0

#tracks current text line
text_y = 0

#current level image object
current_level = pygame.image.load('IMG/level_1_100.png').convert_alpha()

#tracks current frame number
frame = 0
#tracks number of enemies sent and maximum number of enemies
enemy = 0
enemy_max = 0
enemy_level = 0
#tracks current resource total
res = 700

#typer
typebox_x = 100
typebox_y = 100
time_type = 0
typer = Typer('DICT/1',None,1,curr_x,curr_y)
typer.kill()

#wave meter
meter = None

#display start menu
start = True


#computes distance between two points
#   input pixel location tuple for two objects
def dist(a,b):
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])
    return math.sqrt( x**2 + y**2 )

#print the sidebar
def print_sidebar(text, y_height):
    background.blit(font.render(text,True,(255,255,255)), (616,y_height))

#execute on completion of a typing challenge
def type_complete(typ,res,time):
    if typ.type == 'tower':
        the_map.add_tower(typ.y,typ.x)
        tower = grid[typ.y][typ.x]
        tower.skill_modifier(typ.wrong,time)
        res-= 150
    elif typ.type == 'upgrade':
        current_tile = grid[typ.y][typ.x]
        current_tile.upgrade(typ.wrong,time)
        res-= 80
    elif typ.type == 'rapid':
        tower = grid[typ.y][typ.x]
        tower.rapid_upgrade(typ.wrong,time)
        res-= 300
    elif typ.type == 'snipe':
        tower = grid[typ.y][typ.x]
        tower.snipe_upgrade(typ.wrong,time)
        res-= 500
    elif typ.type == 'dam':
        the_map.add_dam(typ.y,typ.x)
        res-= 50
    return res


#redraw the screen
def update_view():
    
    #clear background and add panel
    background.fill((255,255,255))
    background.blit(panel,(615,0))
    #update towers on cooldownrapid
    the_map.update_towers(time)
    #get the newest map
    map_surface = the_map.get_map().convert()
    background.blit(map_surface, (15,0))
    meter_surface = meter.getMeter(time,enemy_level)
    background.blit(meter_surface,(0,0))
    curr_tile = grid[curr_y][curr_x]
    #draws a rectangle around current tile
    pygame.draw.rect(background, (255,255,255), ((curr_x*30+15,curr_y*30),(29,29)), 2)
    
    #displays firing radius around tower as well as all info on the sidebar
    if curr_tile.kind == 'tower':
        pygame.draw.circle(background, (255,255,0), curr_tile.center, curr_tile.range, 1)
        info = curr_tile.get_info()
        info_y = 200
        for text in info:
            background.blit(font.render(text,True,(255,255,255)), (616,info_y))
            info_y+= font_height
    
    
    background.blit(current_level, (700,0))
    background.blit(res_img, (616,75))
    #print messages on sidebar
    text_y = 75
    #display current resource count
    text = " x " + str(int(res))
    background.blit(font.render(text,True,(255,255,255)), (680,100))
    text = 'Wave: ' + str(enemy_level) + "/" + str(level_resource.wave_max)
    background.blit(font.render(text,True,(255,255,255)), (616,35))
    
    text = 'Press (H) for instructions'
    print_sidebar(text, 600-font_height)
    
    
    #draw in all living enemies
    for i in enemies:
        if enemies[i].alive:
            background.blit(enemies[i].pic, enemies[i].draw_coords())
    #draw the typing window (if necessary)
    if typer.active:
        type_sur = typer.get_display(time_type)
        background.blit(type_sur, (typer.x*30+15,typer.y*30))

level = 1
unloaded = True
help = False


#start menu loop
while start:
    
    time = clock.tick(40)/1000.0
    frame+= 1
    
    if (frame / 20) % 2 == 0:
        background.blit(title1,(0,0))
        screen.blit(background,(0,0))
    else:
        background.blit(title2,(0,0))
        screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        #advance to game on any key or mouse press
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                screen.blit(loading,(0,0))
                start = False
        if event.type == MOUSEBUTTONDOWN:
            screen.blit(loading,(0,0))
            start = False

    pygame.display.flip()

#main game loop
while game:
    if unloaded:
        #game is over
        if level == 9:
            game = False
            end = True
        #load next level
        else:
            #load resources to the level
            level_resource.load(level)
            
            #play music
            music = pygame.mixer.Sound(level_resource.music_name)
            music.play(-1)
            
            #initialize map from level resource
            the_map = Field(level_resource.map_name)
            map_surface = the_map.get_map().convert()           
            background.blit(map_surface, (15,0))
            grid = the_map.get_grid()
            towers = the_map.towers
            enemies = dict()
            
            #reset timer
            clock = pygame.time.Clock()
            time = clock.tick(40)
            
            #reset all main variables
            curr_x = 0
            curr_y = 0
            current_level = pygame.image.load(level_resource.level_image).convert_alpha() 
            frame = 0
            enemy = 0
            enemy_max = 0
            enemy_level = 0
            res = level_resource.start_res
            #reload WaveMeter 
            meter = WaveMeter(level_resource.wave_max,(level_resource.wave_time/40),(level_resource.first_wave_time/40),level)
            #return to main game look
            unloaded = False

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

        screen.blit(help_screen,(0,0))
        pygame.display.flip()
        
    #get user input
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
        #update current tile based on mouse or keyboard
        if event.type == MOUSEMOTION:
            new_loc = pygame.mouse.get_pos()
            if (15 <= new_loc[0] < 615) and (0 <= new_loc[1] < 600):
                curr_x = (new_loc[0]-15)/30
                curr_y = (new_loc[1])/30
        #get keyboard input if typer is active
        if typer.active:
            if event.type == KEYDOWN:
                key = pygame.key.name(event.key)
                if event.key == K_SPACE:
                    key = ' '
                if typer.put(key):
                    res = type_complete(typer,res,time_type)
                if event.key == K_ESCAPE:
                    typer.kill()
        elif event.type == KEYDOWN:
            #move selected square with WASD or arror keys
            if (event.key == K_DOWN or event.key == K_s) and curr_y < 570: 
                curr_y+= 1
            if (event.key == K_UP or event.key == K_w) and curr_y > 0:
                curr_y-= 1
            if (event.key == K_RIGHT or event.key == K_d) and curr_x < 570:
                curr_x+= 1
            if (event.key == K_LEFT or event.key == K_a) and curr_x > 0:
                curr_x-= 1
            
            #upgrade a tower at current location
            if event.key == K_u:
                if res >= 80:
                    current_tile = grid[curr_y][curr_x]
                    if (current_tile.kind == 'tower' and current_tile.upgrades < 10):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','upgrade',1,curr_y, curr_x)
                        time_type = -1
            
            #builds a tower at current location
            if event.key == K_r:
                if res >= 150:
                    if (grid[curr_y][curr_x].kind == 'grass'):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','tower',2,curr_y, curr_x)
                        time_type = -1
            
            #upgrade tower to rapid-fire 
            if event.key == K_t:
                if res >= 300:
                    current_tile = grid[curr_y][curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            typer = Typer('DICT/1','rapid',3,curr_y,curr_x)
                            time_type = -1
            
            #upgrade tower to sniper
            if event.key == K_y:
                if res >= 500:
                    current_tile = grid[curr_y][curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            typer = Typer('DICT/1','snipe',3,curr_y,curr_x)
                            time_type = -1
            
            #build a dam
            if event.key == K_e:
                if res >= 50:
                    current_tile = grid[curr_y][curr_x]
                    if (current_tile.kind == 'road'):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','dam',1,curr_y,curr_x)     
                        time_type = -1
            #show help menu    
            if event.key == K_h:
                help = True


    if typer.active:
        time_type+= time
    
    #find time passed since last frame (maxing at 40 fps)
    time = clock.tick(40)/1000.0
    frame+= 1
    
    
    
    
    #adds a resource every second
    if (frame % 40) == 0:
        res+= 1
        
    
    #sends a new enemy (if not at max) every 0.5 second
    if (frame%20) == 0 and enemy < enemy_max :
        enemies[enemy] = Enemy(enemy_level, the_map.path, level)
        enemy+= 1
    
    #special speed waves
    if level == 7:
        if (frame % level_resource.wave_time) == 0:
            enemy_max+=1
            enemy_level+=1
            frame = 0
    elif (enemy_level == 0):
        if frame % level_resource.first_wave_time == 0:
            enemy_max+= 10
            enemy_level+= 1
            frame = 0
    elif level == 4 and enemy_level == 15:
        if (frame % level_resource.wave_time) == 0:
            enemy_max+=1
            enemy_level+=1
            frame = 0
    elif level == 8 and enemy_level == 25:
        if (frame % level_resource.wave_time) == 0:
            enemy_max+=1
            enemy_level+=1
            frame = 0
    elif (frame % level_resource.wave_time) == 0 and enemy_level < level_resource.wave_max:
        enemy_max+= 10
        enemy_level+= 1
        frame = 0
    
    #all towers within range of enemy fire at first available
    for i in towers:
        for j in enemies:
            if enemies[j].alive:
                if dist(towers[i].center,enemies[j].loc) <= towers[i].range and towers[i].cool <= 0:
                    towers[i].fire(enemies[j],enemies,j)
                    if enemies[j].hp <= 0:
                        enemies[j].alive = False
                        res+= enemies[j].reward

    #update dams on the map
    the_map.update_dams(time)
    
    #kills all enemies that reach the end
    num_alive = 0
    for i in enemies:
        if enemies[i].tile.kind == 'home base':
            enemies[i].alive = False
            game = False
            end = True
            
        elif enemies[i].alive:
            enemies[i].move(time)
            num_alive+= 1
    
    #update screen
    update_view()
    screen.blit(background, (0,0))
    #show game over screen if enemy reaches end
    if end:
        screen.blit(the_end, (0,0))
    #draw updated screen
    pygame.display.flip()        
    #determine if level is complete and load next level
    if (num_alive == 0) and enemy_level == level_resource.wave_max:
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
            
            screen.blit(level_finish, (0,0))
            pygame.display.flip()
        unloaded = True
        screen.blit(loading,(0,0))
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
