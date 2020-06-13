""" File which runs the computer vision version of snake.
This takes the users movements and translates them to directions in which the
snake will move in. """

# Necessary imports
import pygame

class Player():
    """ Class which runs the computer vision code. The player will need
    to move in the physical direction that they want the snake to move in. """

    def __init__(self, game):
        self.game = game
        self.playerGame()

    """ Creates a game where a player can play snake. """
    def playerGame(self):
        self.game.startGame(speed = 500)
        running = True
        while running:
            # Updates Display
            pygame.display.update()

            # Handles events
            for i in pygame.event.get():
                self.directionChange()
                # Event which occurs every second
                if i.type == pygame.USEREVENT + 1:
                    self.game.updateSnake()

                # Quitting out of the game
                elif i.type == pygame.QUIT:
                    running = False
                    pygame.quit()

    """ Handles physical player movements. """
    def directionChange(self):
        # Stores whether or not that key has been pressed
        keys=pygame.key.get_pressed()

        # Handling of directions
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.game.setDir(1)
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.game.setDir(2)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.game.setDir(3)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.game.setDir(4)
