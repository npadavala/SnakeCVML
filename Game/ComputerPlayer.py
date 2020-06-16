""" File which runs the computer vision version of snake.
This takes the users movements and translates them to directions in which the
snake will move in. """

# Necessary imports
import pygame
import cv2
import numpy as np
import dlib


class Player():
    """ Class which runs the computer vision code. The player will need
    to move in the physical direction that they want the snake to move in. """

    def __init__(self, game):
        self.game = game
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("landmarks.dat")

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
        two_dim_ref = self.get2DRef(frame)
        
        three_dim_ref = np.array([
                                        (0.0, 0.0, 0.0),                # Nose Tip
                                        (0.0, -330.0, -65.0),           # Chin
                                        (-225.0, 170.0, -135.0),        # Left Eye Left Corner
                                        (225.0, 170.0, -135.0),         # Right Eye Right Corner
                                        (-150.0, -150.0, -125.0),       # Left Mouth Corner
                                        (150.0, -150.0, -125.0),        # Right Mouth Corner
                                ])
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


    """ Isolating the face in the webcam. """
    def get2DRef(self, frame):
        # Convert the frame to a gray frame to make it easier to find features
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        # Detect the face from the passed in frame
        faces = self.detector(grayFrame)
        for face in faces:
            # Coordinates for drawing a box around the detected face
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            # Get the positions on the face which correspond to the dots in landmarks.dat
            landmarks = self.predictor(grayFrame, face)
            
            # Return an array which represents the 2 dimensional picture coordinates which 
            # can be converted to a 3 dimensional reference
            #cv2.rectangle(frame, (x1, y1), (x2, y2), 3, (255, 0, 0), -1)
            return np.array([
                (landmarks.part(33).x, landmarks.part(33).y),
                (landmarks.part(8).x, landmarks.part(8).y),
                (landmarks.part(36).x, landmarks.part(36).y),
                (landmarks.part(45).x, landmarks.part(45).y),
                (landmarks.part(48).x, landmarks.part(48).y),
                (landmarks.part(54).x, landmarks.part(54).y)
            ], dtype="double")
            
            
        
        
        
        