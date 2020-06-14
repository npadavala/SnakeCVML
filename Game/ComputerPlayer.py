""" File which runs the computer vision version of snake.
This takes the users movements and translates them to directions in which the
snake will move in. """

# Necessary imports
import pygame
import cv2

class Player():

    """ Class which runs the computer vision code. The player will need
    to move in the physical direction that they want the snake to move in. """

    def __init__(self, game):
        self.game = game

    """ Creates a game where a player can play snake. """
    def runGame(self):
        self.game.startGame(speed = 500)
        running = True
        while running:
            # Updates Display
            pygame.display.update()

            # Handles events
            for i in pygame.event.get():
                # Event which occurs every second
                if i.type == pygame.USEREVENT + 1:
                    self.game.updateSnake()

                # Quitting out of the game and the webcam
                elif i.type == pygame.QUIT:
                    running = False
                    pygame.quit()

    """ Allows the direction to be set to a different value """
    def setDirectionChange(self, dir):
        self.game.setDir(dir)