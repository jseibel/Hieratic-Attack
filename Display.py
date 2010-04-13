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

    #redraw the screen
    def update_view(self,resources):
        if resources.game_state == 'main':
            #clear background and add panel
            self.background.fill((255,255,255))
            self.background.blit(self.panel,(615,0))
            #update towers on cooldownrapid
            resources.the_map.update_towers(resources.time)
            #get the newest map
            map_surface = resources.the_map.get_map().convert()
            self.background.blit(map_surface, (15,0))
            meter_surface = resources.meter.getMeter(resources.time,resources.enemy_level)
            self.background.blit(meter_surface,(0,0))
            curr_tile = resources.grid[resources.curr_y][resources.curr_x]
            #draws a rectangle around current tile
            pygame.draw.rect(self.background, (255,255,255), ((resources.curr_x*30+15,resources.curr_y*30),(29,29)), 2)

            #displays firing radius around tower as well as all info on the sidebar
            if curr_tile.kind == 'tower':
                pygame.draw.circle(self.background, (255,255,0), curr_tile.center, curr_tile.range, 1)
                info = curr_tile.get_info()
                info_y = 200
                for text in info:
                    self.background.blit(self.font.render(text,True,(255,255,255)), (616,info_y))
                    info_y+= self.font_height


            self.background.blit(resources.current_level, (700,0))
            self.background.blit(resources.res_img, (616,75))
            #print messages on sidebar
            text_y = 75
            #display current resource count
            text = " x " + str(int(resources.res))
            self.background.blit(self.font.render(text,True,(255,255,255)), (680,100))
            text = 'Wave: ' + str(resources.enemy_level) + "/" + str(resources.wave_max)
            self.background.blit(self.font.render(text,True,(255,255,255)), (616,35))

            text = 'Press (H) for instructions'
            self.print_sidebar(text, 600-self.font_height)


            #draw in all living enemies
            for i in resources.enemies:
                if resources.enemies[i].alive:
                    self.background.blit(resources.enemies[i].pic, resources.enemies[i].draw_coords())
            #draw the typing window (if necessary)
            if resources.typer.active:
                type_sur = resources.typer.get_display(resources.typing_timer)
                self.background.blit(type_sur, (resources.typer.x*30+15,resources.typer.y*30))
            else:
                pygame.mouse.set_visible(True)
                
        elif resources.game_state == 'start_menu':
            if (resources.frame / 20) % 2 == 0:
                self.background.blit(resources.title1,(0,0))
            else:
                self.background.blit(resources.title2,(0,0))

        elif resources.game_state == 'loading':
            self.background.blit(resources.loading,(0,0))

        elif resources.game_state == 'help':
            self.background.blit(resources.help_screen,(0,0))

        elif resources.game_state == 'end_level':
            self.background.blit(resources.level_finish, (0,0))

        elif resources.game_state == 'end':
            self.background.blit(resources.the_end, (0,0))

        self.screen.blit(self.background,(0,0))
        
