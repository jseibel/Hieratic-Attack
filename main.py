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

#initialize font and track height
font = pygame.font.SysFont("arial",18)
font_height = font.get_linesize()

#initialized to play sounds
pygame.mixer.init()
music = None

#allows for keys to be held down and repeating function
pygame.key.set_repeat(200,75)

#initialize the background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(((255, 255, 255)))

#level resource object
level_resource = Level()

#game is valid
game = True
end = False

#initialize the side info panel
panel = pygame.Surface((185,600))
panel = panel.convert()
panel.fill((75,75,75))


background.blit(level_resource.map_surface, (15,0))



#clock object for movement, (currently limited to 40 fps)
clock = pygame.time.Clock()
time = clock.tick(40)

#tracks current text line
text_y = 0
#typer
typebox_x = 100
typebox_y = 100
time_type = 0
typer = Typer('DICT/1',None,1,level_resource.curr_x,level_resource.curr_y)
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
        level_resource.the_map.add_tower(typ.y,typ.x)
        tower = level_resource.grid[typ.y][typ.x]
        tower.skill_modifier(typ.wrong,time)
        res-= 150
    elif typ.type == 'upgrade':
        current_tile = level_resource.grid[typ.y][typ.x]
        current_tile.upgrade(typ.wrong,time)
        res-= 80
    elif typ.type == 'rapid':
        tower = level_resource.grid[typ.y][typ.x]
        tower.rapid_upgrade(typ.wrong,time)
        res-= 300
    elif typ.type == 'snipe':
        tower = level_resource.grid[typ.y][typ.x]
        tower.snipe_upgrade(typ.wrong,time)
        res-= 500
    elif typ.type == 'dam':
        level_resource.the_map.add_dam(typ.y,typ.x)
        res-= 50
    pygame.mouse.set_visible(True)
    return res


#redraw the screen
def update_view():
    
    #clear background and add panel
    background.fill((255,255,255))
    background.blit(panel,(615,0))
    #update towers on cooldownrapid
    level_resource.the_map.update_towers(time)
    #get the newest map
    map_surface = level_resource.the_map.get_map().convert()
    background.blit(map_surface, (15,0))
    meter_surface = meter.getMeter(time,level_resource.enemy_level)
    background.blit(meter_surface,(0,0))
    curr_tile = level_resource.grid[level_resource.curr_y][level_resource.curr_x]
    #draws a rectangle around current tile
    pygame.draw.rect(background, (255,255,255), ((level_resource.curr_x*30+15,level_resource.curr_y*30),(29,29)), 2)
    
    #displays firing radius around tower as well as all info on the sidebar
    if curr_tile.kind == 'tower':
        pygame.draw.circle(background, (255,255,0), curr_tile.center, curr_tile.range, 1)
        info = curr_tile.get_info()
        info_y = 200
        for text in info:
            background.blit(font.render(text,True,(255,255,255)), (616,info_y))
            info_y+= font_height
    
    
    background.blit(level_resource.current_level, (700,0))
    background.blit(level_resource.res_img, (616,75))
    #print messages on sidebar
    text_y = 75
    #display current resource count
    text = " x " + str(int(level_resource.res))
    background.blit(font.render(text,True,(255,255,255)), (680,100))
    text = 'Wave: ' + str(level_resource.enemy_level) + "/" + str(level_resource.wave_max)
    background.blit(font.render(text,True,(255,255,255)), (616,35))
    
    text = 'Press (H) for instructions'
    print_sidebar(text, 600-font_height)
    
    
    #draw in all living enemies
    for i in level_resource.enemies:
        if level_resource.enemies[i].alive:
            background.blit(level_resource.enemies[i].pic, level_resource.enemies[i].draw_coords())
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
    level_resource.frame+= 1
    
    if (level_resource.frame / 20) % 2 == 0:
        background.blit(level_resource.title1,(0,0))
        screen.blit(background,(0,0))
    else:
        background.blit(level_resource.title2,(0,0))
        screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        #advance to game on any key or mouse press
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                screen.blit(level_resource.loading,(0,0))
                start = False
        if event.type == MOUSEBUTTONDOWN:
            screen.blit(level_resource.loading,(0,0))
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
            '''
            #initialize map from level resource
            the_map = Field(level_resource.map_name)
            map_surface = the_map.get_map().convert()           
            background.blit(map_surface, (15,0))
            grid = the_map.get_grid()
            towers = the_map.towers
            enemies = dict()
            '''
            #reset timer
            clock = pygame.time.Clock()
            time = clock.tick(40)
            '''
            #reset all main variables
            level_resource.curr_x = 0
            level_resource.curr_y = 0
            current_level = pygame.image.load(level_resource.level_image).convert_alpha() 
            level_resource.frame = 0
            enemy = 0
            enemy_max = 0
            enemy_level = 0
            res = level_resource.start_res
            '''
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

        screen.blit(level_resource.help_screen,(0,0))
        pygame.display.flip()
        
    #get user input
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
        #update current tile based on mouse or keyboard
        if event.type == MOUSEMOTION:
            new_loc = pygame.mouse.get_pos()
            if (15 <= new_loc[0] < 615) and (0 <= new_loc[1] < 600):
                level_resource.curr_x = (new_loc[0]-15)/30
                level_resource.curr_y = (new_loc[1])/30
        #get keyboard input if typer is active
        if typer.active:
            if event.type == KEYDOWN:
                key = pygame.key.name(event.key)
                if event.key == K_SPACE:
                    key = ' '
                if typer.put(key):
                    level_resource.res = type_complete(typer,level_resource.res,time_type)
                if event.key == K_ESCAPE:
                    typer.kill()
        elif event.type == KEYDOWN:
            #move selected square with WASD or arror keys
            if (event.key == K_DOWN or event.key == K_s) and level_resource.curr_y < 570: 
                level_resource.curr_y+= 1
            if (event.key == K_UP or event.key == K_w) and level_resource.curr_y > 0:
                level_resource.curr_y-= 1
            if (event.key == K_RIGHT or event.key == K_d) and level_resource.curr_x < 570:
                level_resource.curr_x+= 1
            if (event.key == K_LEFT or event.key == K_a) and level_resource.curr_x > 0:
                level_resource.curr_x-= 1
            
            #upgrade a tower at current location
            if event.key == K_u:
                if level_resource.res >= 80:
                    current_tile = level_resource.grid[level_resource.curr_y][level_resource.curr_x]
                    if (current_tile.kind == 'tower' and current_tile.upgrades < 10):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','upgrade',1,level_resource.curr_y, level_resource.curr_x)
                        time_type = -1
            
            #builds a tower at current location
            if event.key == K_r:
                if level_resource.res >= 150:
                    if (level_resource.grid[level_resource.curr_y][level_resource.curr_x].kind == 'grass'):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','tower',2,level_resource.curr_y, level_resource.curr_x)
                        time_type = -1
            
            #upgrade tower to rapid-fire 
            if event.key == K_t:
                if level_resource.res >= 300:
                    current_tile = level_resource.grid[level_resource.curr_y][level_resource.curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            typer = Typer('DICT/1','rapid',3,level_resource.curr_y,level_resource.curr_x)
                            time_type = -1
            
            #upgrade tower to sniper
            if event.key == K_y:
                if level_resource.res >= 500:
                    current_tile = level_resource.grid[level_resource.curr_y][level_resource.curr_x]
                    if (current_tile.kind == 'tower'):
                        if current_tile.title == 'Basic Tower':
                            pygame.mouse.set_visible(False)
                            typer = Typer('DICT/1','snipe',3,level_resource.curr_y,level_resource.curr_x)
                            time_type = -1
            
            #build a dam
            if event.key == K_e:
                if level_resource.res >= 50:
                    current_tile = level_resource.grid[level_resource.curr_y][level_resource.curr_x]
                    if (current_tile.kind == 'road'):
                        pygame.mouse.set_visible(False)
                        typer = Typer('DICT/1','dam',1,level_resource.curr_y,level_resource.curr_x)     
                        time_type = -1
            #show help menu    
            if event.key == K_h:
                help = True


    if typer.active:
        time_type+= time
    
    #find time passed since last frame (maxing at 40 fps)
    time = clock.tick(40)/1000.0
    level_resource.frame+= 1
    
    
    
    
    #adds a resource every second
    if (level_resource.frame % 40) == 0:
        level_resource.res+= 1
        
    
    #sends a new enemy (if not at max) every 0.5 second
    if (level_resource.frame%20) == 0 and level_resource.enemy < level_resource.enemy_max :
        level_resource.enemies[level_resource.enemy] = Enemy(level_resource.enemy_level, level_resource.the_map.path, level)
        level_resource.enemy+= 1
    
    #special speed waves
    if level == 7:
        if (level_resource.frame % level_resource.wave_time) == 0:
            level_resource.enemy_max+=1
            level_resource.enemy_level+=1
            level_resource.frame = 0
    elif (level_resource.enemy_level == 0):
        if level_resource.frame % level_resource.first_wave_time == 0:
            level_resource.enemy_max+= 10
            level_resource.enemy_level+= 1
            level_resource.frame = 0
    elif level == 4 and level_resource.enemy_level == 15:
        if (level_resource.frame % level_resource.wave_time) == 0:
            level_resource.enemy_max+=1
            level_resource.enemy_level+=1
            level_resource.frame = 0
    elif level == 8 and level_resource.enemy_level == 25:
        if (level_resource.frame % level_resource.wave_time) == 0:
            level_resource.enemy_max+=1
            level_resource.enemy_level+=1
            level_resource.frame = 0
    elif (level_resource.frame % level_resource.wave_time) == 0 and level_resource.enemy_level < level_resource.wave_max:
        level_resource.enemy_max+= 10
        level_resource.enemy_level+= 1
        level_resource.frame = 0
    
    #all towers within range of enemy fire at first available
    for i in level_resource.towers:
        for j in level_resource.enemies:
            if level_resource.enemies[j].alive:
                if dist(level_resource.towers[i].center,level_resource.enemies[j].loc) <= level_resource.towers[i].range and level_resource.towers[i].cool <= 0:
                    level_resource.towers[i].fire(level_resource.enemies[j],level_resource.enemies,j)
                    if level_resource.enemies[j].hp <= 0:
                        level_resource.enemies[j].alive = False
                        level_resource.res+= level_resource.enemies[j].reward

    #update dams on the map
    level_resource.the_map.update_dams(time)
    
    #kills all enemies that reach the end
    num_alive = 0
    for i in level_resource.enemies:
        if level_resource.enemies[i].tile.kind == 'home base':
            level_resource.enemies[i].alive = False
            game = False
            end = True
            
        elif level_resource.enemies[i].alive:
            level_resource.enemies[i].move(time)
            num_alive+= 1
    
    #update screen
    update_view()
    screen.blit(background, (0,0))
    #show game over screen if enemy reaches end
    if end:
        screen.blit(level_resource.the_end, (0,0))
    #draw updated screen
    pygame.display.flip()        
    #determine if level is complete and load next level
    if (num_alive == 0) and level_resource.enemy_level == level_resource.wave_max:
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
            
            screen.blit(level_resource.level_finish, (0,0))
            pygame.display.flip()
        unloaded = True
        screen.blit(level_resource.loading,(0,0))
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
