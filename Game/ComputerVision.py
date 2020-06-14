""" File which reads video input and uses it to determine which actions are being taken.
These actions are used to run a snake game.  """

# Necessary imports
import pygame
import cv2
import ComputerPlayer as cp
import threading

player = ""

""" Creates the computer player object and has it running in 
its own thread. Reason for multi-threading is so that game
can update simultaneously while we are reading inputs from the
webcam. """
def startGame(game):
    # Creating the player game object
    player = cp.Player(game)

    # Creating 2 separate threads to update GUI and get inputs from the 
    # webcam simultaneously
    guiThread = threading.Thread(target=cp.Player.runGame, args=(player,), daemon=True)
    videoThread = threading.Thread(target=videoCapture, args=(), daemon=True)
    guiThread.start()
    videoThread.start()


""" Logic for reading from the webcam """
def videoCapture():
    video = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not video.isOpened():
        raise IOError("Cannot open webcam")
        
    while True:
        check, frame = video.read()
        cv2.imshow("Capturing", frame)

        c = cv2.waitKey(1)
        if c == 27:
            break    

    video.release()
    cv2.destroyAllWindows()
