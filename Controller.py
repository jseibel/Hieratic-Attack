#event handler
#resolves user input based on state of game

import pygame
from pygame.locals import *
from sys import exit
from Typer import Typer


def handle(event,resources):
    if event.type == QUIT:
        exit()

    if resources.game_state == 'main':
        #update current tile based on mouse or keyboard
        if event.type == MOUSEMOTION:
            new_loc = pygame.mouse.get_pos()
            #convert current mouse coordinates to game map coordinates
            if (15 <= new_loc[0] < 615) and (0 <= new_loc[1] < 600):
                resources.curr_x = (new_loc[0]-15)/30
                resources.curr_y = (new_loc[1])/30
                
        #relay keyboard input to typer if active
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
                resources.game_state = 'help_menu'

    
    if resources.game_state == 'start_menu':
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                resources.game_state = 'loading'
        if event.type == MOUSEBUTTONDOWN:
            resources.game_state = 'loading'


    elif resources.game_state == 'help_menu':
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                resources.game_state == 'main'
        if event.type == MOUSEBUTTONDOWN:
            resources.game_state == 'main'

    elif resources.game_state == 'end_level':
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                resources.game_state = 'loading'
        if event.type == MOUSEBUTTONDOWN:
            resources.game_state = 'loading'

    elif resources.game_state == 'end':
        if event.type == KEYDOWN:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            exit()













        
