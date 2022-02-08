# This is a sample Python script.

# Press The Button Game in python using OpenCV!!!

import math
import random
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone

# web-cam for the detection purpose

cam_cap = cv2.VideoCapture(0)
cam_cap.set(3, 1280)        # id 3 is for width
cam_cap.set(4, 720)         # id 4 is for height
cam_cap.set(10, 200)         # id 10 is for brightness


# Hand-detector
detector = HandDetector(detectionCon= 0.8, maxHands=1)

# find function
# x is the raw distance and y is the value in cm.

x= [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y= [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coefficients = np.polyfit(x, y, 2)     # y = A*(x**2) + Bx + C

# game variable
cx, cy = 200, 200
color = (255, 0, 255)
counter = 0
Score = 0
timebegins = time.time()
totalTime = 30

#loop to detect vid
while True:
    success, img = cam_cap.read()
    img = cv2.flip(img, 1)

    if time.time()-timebegins < totalTime:
        hands = detector.findHands(img, draw=False)

        # hands are detected in 21 points;
        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            # print(lmList)
            x1, y1 = lmList[5]
            x2, y2 = lmList[17]

            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coefficients
            distanceCM = A * distance ** 2 + B * distance + C

            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

            # used to display the purple box
            cv2.rectangle(img, (x, y), (x + w, y + h), (250, 0, 250), 2)

            # print(distanceCM, distance)
            if distanceCM < 30:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1

        # Buzzer Display - Target
        cv2.circle(img, (cx, cy), 13, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 3, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 15, (50, 50, 50), 1)

        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (255, 0, 255)
                Score += 1
                counter = 0

        # game head up display
        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time() - timebegins))} ', (1075, 75), scale=2, offset=30)
        cvzone.putTextRect(img, f'Score: {str(Score).zfill(2)}', (60, 75), scale=2, offset=30)
    else:
        cvzone.putTextRect(img, 'Game Over', (460, 340), scale=4, offset=30, thickness=5)
        cvzone.putTextRect(img, f'Your Score: {Score}', (520, 443), scale=2, offset=30)
        cvzone.putTextRect(img, f'press R to restart', (495, 525), scale=2, offset=20)

    cv2.imshow("Game.Press_The_Buzzer", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timebegins = time.time()
        Score = 0