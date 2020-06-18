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

        # Gets the detector and predictor methods from dlib import
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("landmarks.dat")

        # Creates the frame variable
        self.frame = ''

        # Creates a set a default coordinates which are being compared to 
        # When deciding whether or not the player has turned or not
        self.defaultTranslation = [0, 0, 0]
        self.setDefault = 0

        # Offset player needs to move in order to make a move
        self.xOffset = 100
        self.yOffset = 75


    """ Creates a game where a player can play snake. """
    def runGame(self):
        # Start the snake game and start capturing from webcam
        self.game.startGame(speed = 750)
        self.running = True
        self.video = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.video.isOpened():
            raise IOError("Cannot open webcam")
        
        # Draws the calibrate button
        self.drawCalibrate()

        while self.running:
            # Updates Display
            pygame.display.update()
            events = pygame.event.get()
            self.videoCapture()
            
            # Handles events
            for i in events:
                # Event which occurs every second
                if i.type == pygame.USEREVENT + 1:
                    self.game.updateSnake()
                
                # Checks to see iaf the "Calibrate" button has been clicked
                elif i.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()
                    if (click[0] > 520 and click[1] > 45 and click[0] < 680 and click[1] < 80):
                        self.calibrate()
                        intro = False

                # Quitting out of the game and the webcam
                elif i.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    self.video.release()
                    cv2.destroyAllWindows() 

    """ Changes the CV button into a Calibrate button so that player 
    may define where they will control the snake in the frame. """
    def drawCalibrate(self):
        computer_text = self.game.font.render("Calibrate", True, self.game.black, self.game.red)
        computer_text_rect = computer_text.get_rect()
        computer_text_rect.center = (600, 60)
        self.game.screen.blit(computer_text, computer_text_rect)
        pygame.display.update()
        

    """ Sets game to calibrate on next frame. """
    def calibrate(self):
        self.setDefault = 9
        
    """ Captures video from webcam and adds it to the pygame frame. """
    def videoCapture(self):
        check, self.frame = self.video.read()

        # Detect the face in current webcam frame
        rotation = self.detectFace()

        # Set default rotation values if they have not been set yet
        if (self.setDefault < 10):
            self.defaultTranslation = rotation
            self.setDefault += 1
            
        # Detect if the player has rotated or not
        self.detectDirection(rotation)

        # Convert and resize the frame so that it is usable in pygame
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = np.rot90(self.frame)
        self.frame = cv2.resize(self.frame, (450, 800))

        # Add the frame to the pygame 
        self.frame = pygame.surfarray.make_surface(self.frame)
        self.game.addVideoFeed(self.frame)

    """ Gets the direction from the rotation matrix and figures out which direction the snake needs to move in. """
    def detectDirection(self, translation):
        x_off = translation[0] - self.defaultTranslation[0]
        y_off = translation[1] - self.defaultTranslation[1]
        if (abs(x_off) > self.xOffset and abs(x_off) > abs(y_off) * 1.5):
            if (x_off < 0):
                self.game.setDir(1)
            else:
                self.game.setDir(2)
        elif (abs(y_off) > self.yOffset):
            if (y_off < 0):
                self.game.setDir(3)
            else:
                self.game.setDir(4)


    """ Detects the face and calculates which direction the face is turned in for snake movements. """
    def detectFace(self):
        # 2D image points are extracted from the frame using get2DRef(),
        # which converts frame to grayscale and extracts relevant
        # landmark points from reference file
        two_dim_ref = self.get2DRef()
        
        # 3D model generic reference points which are used to calculate the rotation and translation vectors
        three_dim_ref = np.array([
                                    (0.0, 0.0, 0.0),                # Nose Tip
                                    (0.0, -330.0, -65.0),           # Chin
                                    (-225.0, 170.0, -135.0),        # Left Eye Left Corner
                                    (225.0, 170.0, -135.0),         # Right Eye Right Corner
                                    (-150.0, -150.0, -125.0),       # Left Mouth Corner
                                    (150.0, -150.0, -125.0),        # Right Mouth Corner
                                ])
        dim = self.frame.shape

        # Putting camera features into a matrix
        focal_length_approx = dim[1] # approximating f_x and f_y with image width
        center_x = dim[1]/2
        center_y = dim[0]/2
        camera_matrix = np.array(
                            [[focal_length_approx, 0, center_x],
                            [0, focal_length_approx, center_y],
                            [0, 0, 1]], dtype="double")
        
        # Run estimation using cv2.solvePnP - gives us rotation and 
        # translation vectors. Uses Direct Linear Transform and Levenberg-Marquardt Optimization
        # See this link https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/#code for more info
        try:
            success, rotation, translation = cv2.solvePnP(three_dim_ref, two_dim_ref, camera_matrix, np.zeros((4, 1)))
            return translation
        
        # Catches an error where the face isn't properly detected 
        # and continues running the game with the previous face location
        except cv2.error as e:
            return self.defaultTranslation
        


    """ Isolating the face in the webcam. Returns an array which has stored positions of 
    a few select landmarks on the face. """
    def get2DRef(self):
        # Convert the frame to a gray frame to make it easier to find features
        grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) 

        # Detect the face from the passed in frame
        faces = self.detector(grayFrame)

        # Get the face and find the landmarks from that face
        for face in faces:
            # Coordinates for drawing a box around the detected face
            if (self.setDefault < 10):
                self.left = face.left()
                self.top = face.top()
                self.right = face.right()
                self.bottom = face.bottom()
            
            # Add a rectangle around the location of the calibrated face
            cv2.rectangle(self.frame, (self.left, self.top), (self.right, self.bottom), (255, 0, 0), 3)

            # Add a rectangle around the boundaries the player needs to move to make a move
            cv2.rectangle(self.frame, (self.left - self.xOffset, self.top - self.yOffset), 
                            (self.right + self.xOffset, self.bottom + self.yOffset), (0, 255, 0), 3)

            # Get the positions on the face which correspond to the dots in landmarks.dat
            landmarks = self.predictor(grayFrame, face)

            # Return an array which represents the 2 dimensional picture coordinates which 
            # can be converted to a 3 dimensional reference
            return np.array([
                (landmarks.part(33).x, landmarks.part(33).y),       # Nose Tip
                (landmarks.part(8).x, landmarks.part(8).y),         # Chin
                (landmarks.part(36).x, landmarks.part(36).y),       # Left Eye Left Corner
                (landmarks.part(45).x, landmarks.part(45).y),       # Right Eye Right Corner
                (landmarks.part(48).x, landmarks.part(48).y),       # Left Mouth Corner
                (landmarks.part(54).x, landmarks.part(54).y)        # Right Mouth Corner
            ], dtype="double") 
