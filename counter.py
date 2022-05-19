import cv2
import mediapipe as mp
import numpy as np
import andrew_posemodule as pm #up to user's pose module file name

import tkinter as tk
from tkinter import ttk

# choose workout
def click(x):
    global side
    win.destroy()
    side = x


win = tk.Tk()
win.title("Squat Counter")
Lbl = ttk.Label(win, text="Choose your side")
Lbl.pack()
side = ""

left = ttk.Button(win, text="Left", command=lambda: click("Left"))
right = ttk.Button(win, text="Right", command=lambda: click("Right"))
left.pack()
right.pack()

win.mainloop()

cap = cv2.VideoCapture('video path')
detector = pm.poseDetector()
count = 0
direction = 0
form = 0

while cap.isOpened():
    ret, img = cap.read() #640 x 480
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        
        if side == 'Left':
            left_knee = detector.findAngle(img, 23, 25, 27)
            left_hip = detector.findAngle(img, 11, 23,25)

        if side == 'Right':
            right_knee = detector.findAngle(img, 24, 26, 28)
            right_hip = detector.findAngle(img, 12, 24,26)
        
        #Percentage of success of squat
        if side == 'Left':
            per = np.interp(left_hip, (45, 130), (100, 0))
            bar = np.interp(left_hip, (45, 130), (380, 50))
            # Bar to show squat progress


            #Check to ensure right form before starting the program
            if left_hip > 130 and left_knee > 160:
                form = 1
            
        
            #Check for full range of motion for the squat
            if form == 1:
                if per == 100:
                
                    if left_hip < 45 and left_knee < 70:
                        feedback = "Down"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                        
                if per == 0:
                    if left_hip > 120 and left_knee > 140:
                        feedback = "Up"
                        if direction == 1:
                            count += 0.5
                            direction = 0

            
            #Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)


            #Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            
            #Feedback 
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)


                
        if side == 'Right':
            per = np.interp(right_hip, (45, 130), (100, 0))
            bar = np.interp(right_hip, (45, 130), (380, 50))
            # Bar to show squat progress


            #Check to ensure right form before starting the program
            if right_hip > 130 and right_knee > 160:
                form = 1
            
        
            #Check for full range of motion for the squat
            if form == 1:
                if per == 100:
                    if right_hip < 45 and right_knee < 70:
                        feedback = "Down"
                        if direction == 0:
                            count += 0.5
                            direction = 1

                if per == 0:
                    if right_hip > 120 and right_knee > 140:
                        feedback = "Up"
                        if direction == 1:
                            count += 0.5
                            direction = 0 
    
        
        
            #Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)


            #Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            
            #Feedback 
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)

        
    cv2.imshow('Squat counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
