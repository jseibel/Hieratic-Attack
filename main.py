#   Main driver program for the game

import pygame
from pygame.locals import *
from Display import Display
from Game import Game
from Controller import Controller

#initialize pygame and display
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Hieratic Attack')

#initialized to play sounds
pygame.mixer.init()

#allows for keys to be held down and repeating function
pygame.key.set_repeat(200,75)

#display object
m_display = Display(screen)

#game object
m_game = Game()

#controller object
m_controller = Controller()

#clock object for time-based
clock = pygame.time.Clock()

#main game loop
while True:
    
    #send all events to controller
    for event in pygame.event.get():
        m_controller.handle(event,m_game)
        
    #update game logic but limit to 40 FPS
    m_game.Update( (clock.tick(40)/1000.0) )
    
    #update screen
    m_display.update_view(m_game,m_controller)
    
    #display new screen to user
    pygame.display.flip()


