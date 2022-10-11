# So this is an upgrade project for my last HIMTI Expo Robot Project 
# The robot is going to move acording to hand movement
# hand goes right, robot turn right and viceversa
# hand goes up, robot open mouth and viceversa
# Here we use opencv ( Hand tracking ) from cv2 and firmata to move servo from the arduino
# Feel free to try the code :D

#import module that we need
import cv2
import mediapipe as mp
from pyfirmata import Arduino,util
import numpy as np

#So we need to make some of the variables & declaration that we need for handtracking
cap = cv2.VideoCapture(0)   #you can change base on your camera
mpHands = mp.solutions.hands
hands = mpHands.Hands()     #object hands
mpDraw = mp.solutions.drawing_utils
pTime = 0   #prev time
cTime = 0   #current time
handx = 0
handy = 0

#So we need to make some of the variables & declaration that we need for connecting to firmata
board = Arduino('COM4') #you can change base on your port
it = util.Iterator(board)
it.start()

#Declaration for servo
servo1= board.get_pin('d:9:s') # For the neck (horizontal move) we use pin number 9
servo2= board.get_pin('d:8:s') # For the mouth (vertical move) we use pin number 8
#First we set to 0 degree first
servo1.write(0) 
servo2.write(0)

# the void loop() part
while True:
    success, img = cap.read()
    imgRGB =cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    #turn to RGB
    results = hands.process(imgRGB)                 #turn frame from hand to RGB
    if results.multi_hand_landmarks:                #if there is hand detected then
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)                     #
                handx = cx                          # we use handx and handy to record the last hand position 
                handy = cy
                #list id point - point
                # base palm id = 0
                # thumb line id (1,2,3,4)
                # point line id (5,6,7,8)
                # middle line id (9,10,11,12)
                # ring line id (13,14,15,16)
                # little line id (17,18,19,20)

                #here we use the base palm, so we declare id == 0 
                if id == 0:                          
                    cv2.circle(img, (cx,cy),7,(255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)   #give line between point

    # we use numpy to convert hand detection range to servo degree range
    # so the hand detection is ranging from 10 to 600
    # and for the servo, for mouth servo we are only going to open it for maximum 90 degree
    # but for the neck servo it could move 180 degree 
    tempx = np.interp(handx, [10, 600], [180, 0])
    servo1.write(tempx)
    tempy = np.interp(handy, [10, 180], [90, 0])
    servo2.write(tempy)
    # we flip the camera horizontaly so we dont get mirror image
    flip = cv2.flip(img,1)  
    combined_window = np.hstack([flip])
    cv2.imshow("Image" , combined_window)
    cv2.waitKey(1)