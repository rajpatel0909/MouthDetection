import cv2
#import io
import numpy as np
from queue import *

# from selective_search import *

mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

if mouth_cascade.empty():
  raise IOError('Unable to load the mouth cascade classifier xml file')

cap = cv2.VideoCapture(0)
ds_factor = 2

cntr = 0
frameSeg = 100
q = Queue()
avgx = 0
avgy = 0

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)
    
    for (x,y,w,h) in mouth_rects:
        if cntr < frameSeg:
            cntr += 1
            q.put([x,y])
            avgx = (avgx*cntr + x)/(cntr+1)
            avgy = (avgy*cntr + y)/(cntr+1)
                
            print avgx, avgy, x, y
            y = int(y - 0.15*h)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1)
            frame = frame[y:y+h, x:x+w]
            break
        
        else:
            if (x > (avgx-frameSeg) or x < (avgx + frameSeg)) and (y > (avgy - frameSeg) or y < (avgy + frameSeg)):
                q.put([x,y])
                xy = q.get()
                avgx = (avgx*frameSeg + x - xy[0])/frameSeg
                avgy = (avgy*frameSeg + y - xy[1])/frameSeg
                   
                print avgx, avgy, x, y
                y = int(y - 0.15*h)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1)
                frame = frame[y:y+h, x:x+w]
                break
        break
    #         print cv2.calcHist([frame],[0],None, [256], [0,256])
    #         exit()
    #         regions = selective_search(frame)
    #         for v, (i0, j0, i1, j1) in regions:
    #             print v
            
    
    cv2.imshow('Mouth Detector', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
