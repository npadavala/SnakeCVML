""" File which runs the computer vision version of snake.
This takes the users movements and translates them to directions in which the
snake will move in. """

# Necessary imports
import pygame
import cv2
import time
import pandas
import numpy as np

class Player():

    """ Class which runs the computer vision code. The player will need
    to move in the physical direction that they want the snake to move in. """

    def __init__(self, game):
        self.game = game

    """ Creates a game where a player can play snake. """
    def runGame(self):
        # Start the snake game and start capturing from webcam
        self.game.startGame(speed = 500)
        self.running = True
        self.video = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.video.isOpened():
            raise IOError("Cannot open webcam")
        
        while self.running:
            # Updates Display
            pygame.display.update()
            self.videoCapture()

            # Handles events
            for i in pygame.event.get():
                # Event which occurs every second
                if i.type == pygame.USEREVENT + 1:
                    self.game.updateSnake()

                # Quitting out of the game and the webcam
                elif i.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    self.video.release()
                    cv2.destroyAllWindows() 

    """ Allows the direction to be set to a different value """
    def setDirectionChange(self, dir):
        self.game.setDir(dir)

    """ Captures video from webcam and adds it to the pygame frame. """
    def videoCapture(self):
        check, frame = self.video.read()

        # Convert and resize the frame so that it is usable in pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = cv2.resize(frame, (450, 800))
        frame = pygame.surfarray.make_surface(frame)
        
        # frame = self.detectFace(frame)
        # Add the frame to the pygame 
        self.game.addVideoFeed(frame)

    def detectFace(self, frame):
        reference_points = np.array([ 
                                        (359, 391),      # Nose Tip
                                        (399, 561),      # Chin
                                        (337, 297),      # Left Eye Left Corner
                                        (513, 301),      # Right Eye Right Corner
                                        (345, 465),      # Left Mouth Corner
                                        (453, 469)       # Right Mouth Corner
                                    ], dtype="double")
        

    """ Isolating the face in the webcam. (Not needed)
    def faceIsolation(self)
        static_back = None
        motion_list  = [None, None]
        time=[]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) """
        
        
        
        