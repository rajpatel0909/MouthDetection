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
    mouth = frame[tempy:tempy+int(2*temph*ds_factor), tempx:tempx+int(2.5*tempw*ds_factor)]
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
     
     
    cv2.imshow('Camera', frame)       
    laplacian = cv2.Laplacian(mouth, cv2.CV_64F)
    canny = cv2.Canny(mouth, 70, 75)
    sobel_horizontal = cv2.Sobel(mouth, cv2.CV_64F, 1, 0, ksize=5)
    sobel_vertical = cv2.Sobel(mouth, cv2.CV_64F, 0, 1, ksize=5)
#     cannySobelV = cv2.Canny(, 10, 75)
#     cv2.imshow('cannySobelV', cannySobelV)
#     cv2.moveWindow('cannySobelV', 10, 200)
#     imgray = cv2.cvtColor(mouth, cv2.COLOR_BGR2GRAY)
#     ret, thresh = cv2.threshold(imgray, 127, 255, 0)
#     im2, contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     #cnt = contours[4]
#     try:
#         cv2.drawContours(mouth, contours, 0, (0,255,0), 3)
#     except cv2.error:
#         print("oops!")
    img_output = cv2.cvtColor(mouth, cv2.COLOR_YUV2BGR)
    img_output[:,:,0] = cv2.equalizeHist(img_output[:,:,0])
    
    cannyCont1 = cv2.Canny(img_output, 75, 100)
    cv2.imshow('cannyCont1', cannyCont1)
    cv2.moveWindow('cannyCont1', 10, 200)
    
    #cv2.imshow('contrast', histeq)
    
    
    img_yuv = cv2.cvtColor(mouth, cv2.COLOR_BGR2YUV)
    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    
    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    
    cannyCont = cv2.Canny(img_output, 75, 100)
    
    cv2.imshow('Histogram', img_output)
    cv2.moveWindow('Histogram', 1200, 50)
    cv2.imshow('cannyCont',cannyCont)
    cv2.moveWindow('cannyCont', 1000, 50)
    
    cv2.imshow('Mouth', mouth)
    cv2.moveWindow('Mouth', 10, 50)
    cv2.imshow('laplacian', laplacian)
    cv2.moveWindow('laplacian', 200, 50)
    cv2.imshow('sobel_horizontal', sobel_horizontal)
    cv2.moveWindow('sobel_horizontal', 400, 50)
    cv2.imshow('sobel_vertical', sobel_vertical)
    cv2.moveWindow('sobel_vertical', 600, 50)
    cv2.imshow('Canny', canny)
    cv2.moveWindow('Canny', 800, 50)
    

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
