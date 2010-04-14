#   Main driver program for the game

import pygame
from pygame.locals import *
from Display import Display
from Game import Game
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


#main game loop
while True:
    if m_game.game_state == 'loading':
        pygame.mixer.stop()
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
        

    m_game.Update( (clock.tick(40)/1000.0) )
    
    #update screen
    game_display.update_view(m_game)
    #draw updated screen
    pygame.display.flip()





