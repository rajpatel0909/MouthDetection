import cv2
import numpy as np
import os.path 

words = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THUR", "TEEN", "TWEN", "TEE", "FIF", "HUNDRED", "THOUSAND", "MILLION"]

#name = raw_input("Please enter Your Name: ")
name = "test"

LipPath = "C:/Users/rajpu/workspace/LipData/"
FacePath = "C:/Users/rajpu/workspace/FaceData/"

if not os.path.exists(FacePath   + name):
    os.makedirs(FacePath + name)
else:
    print "Already exists"
    raw_input("Press Enter to continue...")
    exit()

if not os.path.exists(LipPath + name):
    os.makedirs(LipPath + name)
else:
    print "Already exists"
    raw_input("Press Enter to continue...")
    exit()
    

# if os.path.isfile("C:/Users/rajpu/workspace/FaceData/ZERO/" + name + ".avi"):
#     print "This file already exists"

cap = cv2.VideoCapture(0)

x = int(275)
y = int(275)
w = int(100)
h = int(75)

while(cap.isOpened):
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if ret == True:
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,('Please your mouth in RED BOX'),(10,25), font, 0.5,(0,0,255),1)
        cv2.putText(frame,('Press space to continue'),(10,50), font, 0.5,(0,0,255),1)
        
        cv2.imshow('frame',frame)
        
        k = cv2.waitKey(33)
        if k == 32:
            break
        
    
cap.release()
cv2.destroyAllWindows()
i = 0

while i < len(words):
    
    word = words[i]
    
    cap = cv2.VideoCapture(0)
    #ds_factor = 2
    
    width=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
    height=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    
    if not os.path.exists(FacePath + name + "/" + word):
        os.makedirs(FacePath + name + "/" + word)
    

    if not os.path.exists(LipPath + name + "/" + word):
        os.makedirs(LipPath + name + "/" + word)
    
    facefp = FacePath + name + "/" + word + "/" + word + ".avi"
    lipfp = LipPath + name + "/" + word + "/" + word + ".avi"
    
    faceout = cv2.VideoWriter(facefp,fourcc, 20.0, (width,height))
    lipout = cv2.VideoWriter(lipfp,fourcc, 20.0, (w,h))
    
    start = False
    
    while(cap.isOpened):
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        if ret == True:
            
            #frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            
            
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
            mouth = frame[y:y+h, x:x+w]
            if start:
                faceout.write(frame)
                lipout.write(mouth)
                print "start"
                
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,('Speak : ' + word),(10,25), font, 0.5,(0,0,255),1)
            if not start:
                cv2.putText(frame,('Press Space to start and Esc to redo '),(10,50), font, 0.5,(0,0,255),1)
            else:
                cv2.putText(frame,('Press Space to end and continue and Esc to redo '),(10,50), font, 0.5,(0,0,255),1)
            
            cv2.imshow('mouth', mouth)
            cv2.imshow('frame',frame)
            print "Camera On"
            k = cv2.waitKey(33)
            if k == 32:
                if not start:
                    print "start"
                    start = True
                    continue
                    k = 0
                else:
                    print "end"
                    i += 1
                    break
            elif k == 27:
                break
            
           
    cap.release()
    cv2.destroyAllWindows()