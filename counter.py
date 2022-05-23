import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm


cap = cv2.VideoCapture('video5.mp4')
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"

side = input("Which side of my body is my video device? L/R: ")

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
        
        if side == 'L':
            left_knee = detector.findAngle(img, 23, 25, 27)
            left_hip = detector.findAngle(img, 11, 23,25)

        if side == 'R':
            right_knee = detector.findAngle(img, 24, 26, 28)
            right_hip = detector.findAngle(img, 12, 24,26)
        
        #Percentage of success of squat
        if side == 'L':
            per = np.interp(left_hip, (45, 130), (0, 100))
            bar = np.interp(left_hip, (45, 130), (380, 50))
            # Bar to show squat progress
            
            
            #Check to ensure right form before starting the program
            if left_hip > 130 and left_knee > 160:
                form = 1                  
        
            #Check for full range of motion for the squat
            if form == 1:
                if per == 0:
                
                    if left_hip < 45 and left_knee < 70:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1

                else:
                    feedback = "Go Lower"
                        
                if per == 100:
                    if left_hip > 120 and left_knee > 140:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0

                else:
                    feedback = "Go Lower"
                            # form = 0
            
            #Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)


            #Squat counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            
            #Feedback 
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
            
                
        if side == 'R':
            per = np.interp(right_hip, (45, 130), (0, 100))
            bar = np.interp(right_hip, (45, 130), (380, 50))
            # Bar to show squat progress
            

            #Check to ensure right form before starting the program
            if right_hip > 130 and right_knee > 160:
                form = 1
            
        
            #Check for full range of motion for the squat
            if form == 1:
                if per == 0:
                
                    if right_hip < 45 and right_knee < 70:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1

                else:
                    feedback = "Go Lower"
                        
                if per == 100:
                    if right_hip > 120 and right_knee > 140:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0

                else:
                    feedback = "Go Lower"
                            # form = 0            
                        
        
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
