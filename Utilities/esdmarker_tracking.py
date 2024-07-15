☺# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 08:35:28 2024

@author: kuifenhu

# need to 
1. create conda new enviroment with python 3.10
2. https://visualstudio.microsoft.com/visual-cpp-build-tools/ to get VC 14++ compiler and cmake,
3. pip install opencv-python, torch,  super_gradients, 

"""


import cv2
import torch
#from super_gradients.training import models
import numpy as np
import math
from ultralytics import YOLO
import pdb
import pandas as pd

def mouse_click_event(event, x, y, flags, param):
  #pdb.set_trace()
  if event == cv2.EVENT_LBUTTONDOWN:
    #print("Mouse clicked at coordinates: (" + str(x) + ", " + str(y) + ")")
    x1, y1 =int(x)-10,int(y)-5
    x2, y2 = x1 + 20, y1 + 10  # Ensure 10x10 size
    cv2.rectangle(frame, (x1, y1), (x2, y2),green, -1)  # Filled square
    squaresC.append((x1, y1, x2, y2))
  if event == cv2.EVENT_RBUTTONDOWN:
    #print("Mouse clicked at coordinates: (" + str(x) + ", " + str(y) + ")")
    x1, y1 =int(x)-10,int(y)-5
    x2, y2 = x1 + 20, y1 + 10  # Ensure 10x10 size
    cv2.rectangle(frame, (x1, y1), (x2, y2),red, -1)  # Filled square
    squaresA.append((x1, y1, x2, y2))
  if event == cv2.EVENT_MBUTTONDOWN:
    squaresA.append((x1, y1, x2, y2))
    
device=torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
model=YOLO('./bestESD2.pt')
    
            
# Initialize webcam capture
x1, y1 =0, 0
x2, y2 = x1 + 1, y1 + 1  # Ensure 10x10 size
count=0
cv2.namedWindow('ESD Capture Window')
# Set the mouse callback function
cv2.setMouseCallback('ESD Capture Window', mouse_click_event)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
# Create a named window
    
global squaresC 
squaresC= [(x1,y1,x2,y2)]  # Track currently displayed squares
global squaresA 
squaresA = [(x1,y1,x2,y2)] # Track currently displayed squares
global squaresTotal 
# squaresTotal=pd.DataFrame({'XY':squaresC})
# squaresTotal.append({'XY':squaresA})


green = (0,255,0)
yellow = (0,255,255)
red = (0,0,255)
purple=(255,204,204)

while True:
    ret, frame = cap.read()
    results=model.predict(frame, conf=0.1)
    result=results[0]
    boxes=result.boxes
    if boxes.xyxy.nelement():
        xyxy=boxes.xyxy.tolist()[0]
        frame=result.plot()
    # Draw existing squaresqq
    countc=0
    counta=0
    for (x1, y1, x2, y2) in squaresC:
      if countc>=1:
        cv2.rectangle(frame, (x1, y1), (x2, y2), green, 2)  # Green outline
        cv2.putText(frame, f"{countc}", (x1 + 2, y1 + 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, purple, 1)  # Optional: Display coordinates
      countc=countc+1  
    for (x1, y1, x2, y2) in squaresA:
      if counta>=1:
        cv2.rectangle(frame, (x1, y1), (x2, y2), red, 2)  # Green outline
        cv2.putText(frame, f"{counta}", (x1 + 2, y1 + 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, yellow, 1)  # Optional: Display coordinates
      counta=counta+1
# Add new squares if 'contact discharge c' is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
      if len(xyxy):  
        x1, y1 =int((xyxy[0]+xyxy[2])/2-5),int((xyxy[1]+xyxy[3])/2-5)
        x2, y2 = x1 + 20, y1 + 10  # Ensure 10x10 size
        cv2.rectangle(frame, (x1, y1), (x2, y2),green, -1)  # Filled square
        squaresC.append((x1, y1, x2, y2))
        
# Add new squares if 'air discharge a' is pressed

    if cv2.waitKey(1) & 0xFF == ord('a'):
      if len(xyxy):     
        x1, y1 =int((xyxy[0]+xyxy[2])/2-5),int((xyxy[1]+xyxy[3])/2-5)
        x2, y2 = x1 + 20, y1 + 10  # Ensure 10x10 size
        cv2.rectangle(frame, (x1, y1), (x2, y2),green, 1)  # Filled square
        squaresA.append((x1, y1, x2, y2))
     
    # Display the frame
    cv2.imshow('ESD Capture Window', frame)

    # Exit on 'q' or 'Esc' key
    if cv2.waitKey(10) & 0xFF in (ord('q'), ord('Q'), 27):
        cv2.imwrite('finalresult.jpg',frame)
        break

# Release resources

cap.release()
cv2.destroyAllWindows()                                                                                                                             