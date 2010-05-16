#Display class, used for creating and updating the visual representation of the game

import pygame
from pygame.locals import *

class Display(object):

    #initialize display, pass it a pygame.display
    def __init__(self,screen):
        #initialize the background to screen size, convert, and fill with black
        self.screen = screen
        self.background = pygame.Surface(screen.get_size())
        self.background.convert()
        self.background.fill((255, 255, 255))
        #initialize the side info panel to size, convert, fill with gray
        self.panel = pygame.Surface((185,600))
        self.panel.convert()
        self.panel.fill((75,75,75))
        self.font = pygame.font.SysFont("arial",18)
        self.font_height = self.font.get_linesize()

    #print text to the sidebar
    def print_sidebar(self,text, y_height):
        self.background.blit(self.font.render(text,True,(255,255,255)), (616,y_height))

    def DrawRadial(self,x,y,choice_list):
        for selection in choice_list:
            self.
        

    #redraw the screen
    def update_view(self,game_data,controller):
        if game_data.game_state == 'main':
            #clear background and add panel
            self.background.fill((255,255,255))
            self.background.blit(self.panel,(615,0))
            #update towers on cooldownrapid
            game_data.the_map.update_towers(game_data.time)
            #get the newest map
            map_surface = game_data.the_map.get_map().convert()
            self.background.blit(map_surface, (15,0))
            meter_surface = game_data.meter.getMeter(game_data.time,game_data.enemy_level)
            self.background.blit(meter_surface,(0,0))
            curr_tile = game_data.grid[controller.curr_y][controller.curr_x]
            #draws a rectangle around current tile
            pygame.draw.rect(self.background, (255,255,255), ((controller.curr_x*30+15,controller.curr_y*30),(29,29)), 2)

            #displays firing radius around tower as well as all info on the sidebar
            if curr_tile.kind == 'tower':
                pygame.draw.circle(self.background, (255,255,0), curr_tile.center, curr_tile.range, 1)
                info = curr_tile.get_info()
                info_y = 200
                for text in info:
                    self.background.blit(self.font.render(text,True,(255,255,255)), (616,info_y))
                    info_y+= self.font_height


            self.background.blit(game_data.current_level, (700,0))
            self.background.blit(game_data.res_img, (616,75))
            
            #display current resource count
            text = " x " + str(int(game_data.res))
            self.background.blit(self.font.render(text,True,(255,255,255)), (680,100))
            text = 'Wave: ' + str(game_data.enemy_level) + "/" + str(game_data.wave_max)
            self.background.blit(self.font.render(text,True,(255,255,255)), (616,35))

            text = 'Press (H) for instructions'
            self.print_sidebar(text, 600-self.font_height)


            #draw in all living enemies
            for i in game_data.enemies:
                if game_data.enemies[i].alive:
                    self.background.blit(game_data.enemies[i].pic, game_data.enemies[i].draw_coords())
            #draw the typing window (if necessary)
            if game_data.typer.active:
                type_sur = game_data.typer.get_display(game_data.typing_timer)
                self.background.blit(type_sur, (game_data.typer.x*30+15,game_data.typer.y*30))
            else:
                pygame.mouse.set_visible(True)
                
        elif game_data.game_state == 'start_menu':
            if (game_data.frame / 20) % 2 == 0:
                self.background.blit(game_data.title1,(0,0))
            else:
                self.background.blit(game_data.title2,(0,0))

        elif game_data.game_state == 'loading':
            self.background.blit(game_data.loading,(0,0))

        elif game_data.game_state == 'help':
            self.background.blit(game_data.help_screen,(0,0))

        elif game_data.game_state == 'end_level':
            self.background.blit(game_data.level_finish, (0,0))

        elif game_data.game_state == 'end':
            self.background.blit(game_data.the_end, (0,0))

        self.screen.blit(self.background,(0,0))
        
