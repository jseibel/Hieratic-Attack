#event handler
#resolves user input based on state of game

import pygame
from pygame.locals import *
from sys import exit
from Typer import Typer

class Controller(object):

    def __init__(self):
        self.curr_x = 0
        self.curr_y = 0
    
    
    def handle(self,event,game_data):
        if event.type == QUIT:
            exit()

        if game_data.game_state == 'main':
            #update current tile based on mouse or keyboard
            if event.type == MOUSEMOTION:
                new_loc = pygame.mouse.get_pos()
                #convert current mouse coordinates to game map coordinates
                if (15 <= new_loc[0] < 615) and (0 <= new_loc[1] < 600):
                    self.curr_x = (new_loc[0]-15)/30
                    self.curr_y = (new_loc[1])/30
                    
            #relay keyboard input to typer if active
            if game_data.typer.active:
                if event.type == KEYDOWN:
                    key = pygame.key.name(event.key)
                    if event.key == K_SPACE:
                        key = ' '
                    if game_data.typer.put(key):
                        game_data.typer.type_complete(game_data)
                    if event.key == K_ESCAPE:
                        game_data.typer.kill()
            elif event.type == KEYDOWN:
                #move selected square with WASD or arrow keys
                if (event.key == K_DOWN or event.key == K_s) and self.curr_y < 19:
                    self.curr_y+= 1
                if (event.key == K_UP or event.key == K_w) and self.curr_y > 0:
                    self.curr_y-= 1
                if (event.key == K_RIGHT or event.key == K_d) and self.curr_x < 19:
                    self.curr_x+= 1
                if (event.key == K_LEFT or event.key == K_a) and self.curr_x > 0:
                    self.curr_x-= 1
                
                #upgrade a tower at current location
                if event.key == K_u:
                    game_data.ActivateTyper(self.curr_x,self.curr_y,'upgrade')
                    
                #builds a tower at current location
                if event.key == K_r:
                    game_data.ActivateTyper(self.curr_x,self.curr_y,'tower')
                    
                #upgrade tower to rapid-fire 
                if event.key == K_t:
                    game_data.ActivateTyper(self.curr_x,self.curr_y,'rapid')
                    
                #upgrade tower to sniper
                if event.key == K_y:
                    game_data.ActivateTyper(self.curr_x,self.curr_y,'snipe')
                    
                #build a dam
                if event.key == K_e:
                    game_data.ActivateTyper(self.curr_x,self.curr_y,'dam')
                    
                #show help menu    
                if event.key == K_h:
                    game_data.game_state = 'help_menu'

        
        if game_data.game_state == 'start_menu':
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game_data.game_state = 'loading'
            if event.type == MOUSEBUTTONDOWN:
                game_data.game_state = 'loading'


        elif game_data.game_state == 'help_menu':
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game_data.game_state == 'main'
            if event.type == MOUSEBUTTONDOWN:
                game_data.game_state == 'main'

        elif game_data.game_state == 'end_level':
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game_data.game_state = 'loading'
            if event.type == MOUSEBUTTONDOWN:
                game_data.game_state = 'loading'

        elif game_data.game_state == 'end':
            if event.type == KEYDOWN:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                exit()













        
