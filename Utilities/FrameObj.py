import cv2
import torch
#from super_gradients.training import models
import numpy as np
import math
from ultralytics import YOLO
import pdb
import pandas as pd


green = (0,255,0)
yellow = (0,255,255)
red = (0,0,255)
purple=(255,204,204)


class FrameObject:
    def __init__(self):
        self.model_path='./bestESD2.pt'
        self.channel=1
        self.boxes=[]
        self.cv=[]
        self.frame=[]
        self.overlay=[]
        self.boxesc=[]
        self.boxesa=[]
        self.countc=0
        self.counta=0
        self.location=[(0,0,0,0)]
    
    def ini(self):
        device=torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model=YOLO(self.model_path)
        
        x1, y1 =0, 0
        x2, y2 = x1 + 1, y1 + 1  # Ensure 10x10 size
        self.squaresC= [(x1,y1,x2,y2)]  # Track currently displayed squares
        self.squaresA = [(x1,y1,x2,y2)] # Track currently displayed squares
        self.squaresTotal =0
        self.count=0
        # cv2.namedWindow('ESD Capture Window')
        # # Set the mouse callback function
        # cv2.setMouseCallback('ESD Capture Window', mouse_click_event)
        
        # #self.mainW=cv2.namedWindow('ESD Capture Window')
        # self.cap = cv2.VideoCapture(self.channel)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        # ret, self.frame=self.cap.read()
        #height, width,tmp=self.frame.shape
        height=480
        width=640
        self.overlay = np.zeros((height, width, 4), dtype=np.uint8)
        
        
    def refresh(self):
        height=480
        width=640
        self.overlay = np.zeros((height, width, 4), dtype=np.uint8)
        self.countc=0  
    def new(self):
        height=480
        width=640
        self.overlay = np.zeros((height, width, 4), dtype=np.uint8)

    def deleteboxc(self): 
        if len.self.boxesc >=1 :
            self.boxesc.pop()
    def deleteboxa(self): 
        if len.self.boxesa >=1 :
            self.boxesa.pop()
            
    def show(self):
        self.combine_overlay()
        cv2.imshow('ESD Capture Window', self.frame)

    def save(self,fname):
        self.combine_overlay()
        cv2.imwrite(fname,self.frame)
        
    def yolo(self):
        results=self.model.predict(self.frame, conf=0.1, verbose=False)
        result=results[0]
        boxes=result.boxes
        if result.boxes is not None: 
            if boxes.xyxy.nelement():
                xyxy=boxes.xyxy.tolist()[0]
                xyxy = [int(x) for x in xyxy]
                self.location=[(xyxy[0]-10,xyxy[1]-5,xyxy[0]+10,xyxy[1]+5 )]
                self.frame=result.plot()
                #return(xyxy)

    def add_pointer(self, tip_location, color):
        R,G,B=color
        for (x1, y1, x2, y2) in tip_location:
          cv2.rectangle(self.overlay, (x1, y1), (x2, y2),(R, G, B, 128),-1)  # Green outline
          cv2.putText(self.overlay, f"{self.countc}", (x1 + 2, y1 + 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, purple, 1)  # Optional: Display coordinates
          self.countc=self.countc+1  
           
    def combine_overlay(self):
        overlay_rgb = self.overlay[:, :, :3]
        alpha = self.overlay[:, :, 3] / 255.0

        # Perform alpha blending
        result = self.frame.copy()
        for c in range(3):
            result[:, :, c] = (1 - alpha) * self.frame[:, :, c] + alpha * overlay_rgb[:, :, c]
        self.frame=result
       
    # def get_pointer(self, name):
    #     return self._pointers.get(name)

    # def remove_pointer(self, name):
    #     self._pointers.pop(name, None)# -*- coding: utf-8 -*-
    def end(self):
        self.cap.release()
        cv2.destroyAllWindows()
    # def find_channel(self,n):
    #     available_cameras = []
    #     for i in range(n):  # Check first 10 indexes
    #         cap = cv2.VideoCapture(i)
    #         if cap.isOpened():
    #             ret, frame = cap.read()
    #             if ret:
    #                 available_cameras.append(i)
    #                 print(f"Camera index {i} is available")
    #                 # You can uncomment the following lines to display the camera feed
    #                 # cv2.imshow(f"Camera {i}", frame)
    #                 # cv2.waitKey(1000)
    #                 # cv2.destroyAllWindows()
    #             cap.release()
    #         else:
    #             print(f"Camera index {i} is not available")
        
    #     return available_cameras
        
"""
Created on Thu Jun 27 11:10:30 2024

@author: kuifenhu
"""

