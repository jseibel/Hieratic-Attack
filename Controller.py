#event handler
import pygame
from pygame.locals import *


def handle(event,resources):
    if resources.game_state == 'start_menu':
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                resources.game_state = 'loading'
        if event.type == MOUSEBUTTONDOWN:
            resources.game_state = 'loading'


    #elif resource.game_state == 'help_menu':
