""" File which runs the computer vision version of snake.
This takes the users movements and translates them to directions in which the
snake will move in. """

# Necessary imports
import pygame
import cv2
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

        # Detect the face in current webcam frame
        self.detectFace(frame)
        
        # Convert and resize the frame so that it is usable in pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = cv2.resize(frame, (450, 800))

        # Add the frame to the pygame 
        frame = pygame.surfarray.make_surface(frame)
        self.game.addVideoFeed(frame)

    def detectFace(self, frame):
        two_dim_ref = np.array([ 
                                        (359, 391),      # Nose Tip
                                        (399, 561),      # Chin
                                        (337, 297),      # Left Eye Left Corner
                                        (513, 301),      # Right Eye Right Corner
                                        (345, 465),      # Left Mouth Corner
                                        (453, 469)       # Right Mouth Corner
                                    ], dtype="double")
        three_dim_ref = np.array([
                                        (0.0, 0.0, 0.0),                # Nose Tip
                                        (0.0, -330.0, -65.0),           # Chin
                                        (-225.0, 170.0, -135.0),        # Left Eye Left Corner
                                        (225.0, 170.0, -135.0),         # Right Eye Right Corner
                                        (-150.0, -150.0, -125.0),       # Left Mouth Corner
                                        (150.0, -150.0, -125.0),        # Right Mouth Corner
                                ], dtype="double")
        dim = frame.shape

        # Getting camera matrix
        focal_length_approx = dim[1] # approximating f_x and f_y with image width
        center_x = dim[1]/2
        center_y = dim[0]/2
        camera_matrix = np.array(
                                    [[focal_length_approx, 0, center_x],
                                     [0, focal_length_approx, center_y],
                                     [0, 0, 1]], dtype="double"
                                )
        
        # run estimation using cv2.solvePnP - gives us rotation and translation vectors
        success, rotation, translation = cv2.solvePnP(three_dim_ref, two_dim_ref, camera_matrix, np.zeros((4, 1)))
        print(rotation)


    """ Isolating the face in the webcam. (Not needed)
    def faceIsolation(self)
        static_back = None
        motion_list  = [None, None]
        time=[]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) """
        
        
        
        