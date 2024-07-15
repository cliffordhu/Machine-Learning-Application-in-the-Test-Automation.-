# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:12:04 2024

@author: kuifenhu
"""
import cv2
from FrameObj import FrameObject
fm=FrameObject()
fm.model_path="C:/Users/kuifenhu/yolo/yolov8s_playing_cards.pt"
#fm.model_path="C:/Users/kuifenhu/yolo/cardbest.pt"

#fm.find_channel(3)
fm.channel=1
fm.ini()

while True:
    fm.refresh()
    #fm.yolo()
    fm.show()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break    



fm.end
