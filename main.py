import cv2
import numpy as np
from Queue import *

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
    height = frame.shape[0]
    width = frame.shape[1]
    tempx = width/2
    tempy = height/2
    tempw = int(width/20)
    temph = int(height/20)
    tempx = int(tempx*ds_factor) - tempw
    tempy = int(tempy*ds_factor) - temph
    
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)
    cv2.rectangle(frame, (tempx,tempy), (tempx+int(2.5*tempw*ds_factor),tempy+int(2*temph*ds_factor)), (0,0,255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Place your mouth in RED BOX',(10,50), font, 1,(0,0,255),1)
            
    for (x,y,w,h) in mouth_rects:
        if cntr < frameSeg:
            cntr += 1
            q.put([x,y])
            avgx = (avgx*cntr + x)/(cntr+1)
            avgy = (avgy*cntr + y)/(cntr+1)
                
            #print avgx, avgy, x, y, h, w
            y = int(y - 0.15*h)
            
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1)
            #cv2.rectangle(frame, (tempx,tempy), (tempx+123,tempy+74), (0,255,0), 1)
            #cv2.rectangle(frame, (tempx,tempy), (tempx+int(2.5*tempw*ds_factor),tempy+int(2*temph*ds_factor)), (0,0,255), 3)
            #frame = frame[y:y+74, x:x+123]
            break
        
        else:
            if (x > (avgx-frameSeg) or x < (avgx + frameSeg)) and (y > (avgy - frameSeg) or y < (avgy + frameSeg)):
                q.put([x,y])
                xy = q.get()
                avgx = (avgx*frameSeg + x - xy[0])/frameSeg
                avgy = (avgy*frameSeg + y - xy[1])/frameSeg
                   
                #print avgx, avgy, x, y
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1)
                #cv2.rectangle(frame, (tempx,tempy), (tempx+int(2.5*tempw*ds_factor),tempy+int(2*temph*ds_factor)), (0,0,255), 3)
                #frame = frame[y:y+w, x:x+h]
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
