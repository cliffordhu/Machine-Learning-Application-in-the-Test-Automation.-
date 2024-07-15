# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:46:14 2024

@author: kuifenhu
use multip process to capture ESD discharge location:
1. Yolo_detection process always feed the location to the 1 varabile stack queue
2. vosk_recognization listen to the voice command. if "mark" is identified, put a label on the frame. 
3. 
"""

import multiprocessing as mp
import time
import random
from Utilities.FrameObj import FrameObject
import cv2
from Utilities.VoiceObj import VoiceObject 
from pynput import keyboard, mouse



# configuration 
Mic_Device_Channel=1
Vosk_Model_Weigths="./Models/vosk-model-en-us-0.42-gigaspeech"

Camera_Device_Channel=0
Yolo_Model_Weights="./Models/yolov8s_playing_cards.pt"

# definition of constant
green = (0,255,0)
yellow = (0,255,255)
red = (0,0,255)
purple=(255,204,204)

#initialization of variables.
n=0  # tracking the report page number

def yolo_detection(fm_queue):
    
    cap = cv2.VideoCapture(Camera_Device_Channel)
    while True:
        ret, frame = cap.read()
        if not ret:
             break
        if not fm_queue.full():
             fm_queue.put(frame)
        if cv2.waitKey(1) & 0xFF in (ord('q'), ord('Q'), 27):   
           cap.release()

        
def vosk_recognition(vc_queue):
    vc=VoiceObject()
    vc.model_path = Vosk_Model_Weigths
    vc.channel=Mic_Device_Channel
    vc.ini()

    print("VoiceObject is initialized successfully, Speak now...")
       
    while True:
        command = vc.listen()       
        if command =="break" or command=="finish":
            break
        else:
            if len(command):
                
                if vc_queue.full():
                    vc_queue.get()
                    vc_queue.put(command)
                else:
                    vc_queue.put(command)
                    
                
             
def monitor_keypad(key_queue):
    def on_press(key):
        try:
            if key_queue.full():
                key_queue.get()
                key_queue.put(key.char)
            else:
                key_queue.put(key.char)
        except AttributeError:
            pass  # Ignore special keys

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def monitor_mouse(ms_queue):
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            if not ms_queue.full():
                ms_queue.put([0,(x-10, y-5,x+10,y+5)])
        if button == mouse.Button.right and pressed:
            if not ms_queue.full():
                ms_queue.put([1,(x-10, y-5,x+10,y+5)])  
        if button == mouse.Button.middle and pressed:
            if not ms_queue.full():
                ms_queue.put([2,(x-10, y-5,x+10,y+5)])  
                

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
def offset(coords):
    x1, y1, x2, y2 = coords
    window_name='ESD Capture Window'
    rect = cv2.getWindowImageRect(window_name)
    x, y, w, h = rect
    return (x1 - x, y1 - y, x2 -x, y2 -y)

            
if __name__ == "__main__":
    fm_queue = mp.Queue(maxsize=1)
    vc_queue = mp.Queue(maxsize=1)
    key_queue = mp.Queue(maxsize=1)
    ms_queue = mp.Queue(maxsize=1)
    
    yolo_process = mp.Process(target=yolo_detection, args=(fm_queue,))
    vosk_process = mp.Process(target=vosk_recognition, args=(vc_queue,))
    key_process = mp.Process(target=monitor_keypad, args=(key_queue,))
    ms_process = mp.Process(target=monitor_mouse, args=(ms_queue,))
  
    
    yolo_process.start()
    vosk_process.start()
    key_process.start()
    ms_process.start()
    
    fm=FrameObject()
    #fm.model_path="C:/Users/kuifenhu/yolo/yolov8n-cls.pt"
    fm.model_path=Yolo_Model_Weights
    # # Set the mouse callback function
    fm.channel=0
    fm.ini()
    command=""
    print('FrameObject is initialized successfully!')
    while True:
        #perform yolo vision on ESD tip
        if not fm_queue.empty():
            fm.frame=fm_queue.get()
            fm.yolo()
            fm.show()
            # action when voice command is detected
            if not vc_queue.empty():
                command=vc_queue.get()
                print(f'Received command: {command}')
                if command =="mark":
                    if fm.location:
                        fm.add_pointer(fm.location,green)
                        fm.show()
                if command =="check":
                    #tip_location=fm.location
                    if fm.location:
                        fm.add_pointer(fm.location,red)
                        fm.show()
                if command =="save":
                    fname=f'./Results/finalresult{n}.jpg'
                    fm.save(fname)
                    n=n+1
                    print(f"Frame is saved to {fname}")
                    fm.new()
                if command =="new":
                    fm.new()
                    fm.show()
                if command =="refresh":
                    fm.refresh()
                    fm.show()
                    
                    
                    
                if command =="break" or command=="finish":
                    break
            #action when keyboard is clicked
            if not key_queue.empty():
                key = key_queue.get()
                if key == 'c': # contact discharge
                    print("contact discharge point marked!")
                    fm.add_pointer(fm.location,green)
                    fm.show() # air discharge
                if key == 'a':
                    print("Air discharge point marked!")
                    fm.add_pointer(fm.location,red)
                    fm.show()
                if key == 'r':
                    print("Ereas all points")
                    fm.refresh()
                    fm.show()
                if key == 'n':
                    print("New overlay is created")
                    fm.news()
                    fm.show()
                if key=='s':   #save    
                    print("Current frame is saved!")
                    fname=f'./Results/finalresult{n}.jpg'
                    fm.save(fname)
                    n=n+1
                    print(f"Frame is saved to {fname}")
                    fm.new()
                    
                if command =="q":
                    fm.save(f'./finalresult{n}.jpg')
                    n=n+1
                    break    # Add any specific action you want to perform when 'c'
            # action when mouse is clicked
            if not ms_queue.empty():
                 ms=ms_queue.get()
                 ms1 = offset(ms[1])
                 if ms[0]==0: # contact discharge
                     print(f"Contact discharge point is marked by mouse")
                     fm.add_pointer([ms1],green)
                     fm.show()   
                 if ms[0]==1:  # air discharge 
                     print(f" Air discharge point is marked by mouse")
                     fm.add_pointer([ms1],red)
                     fm.show()       
                 if ms[0]==2:  # air discharge 
                     print(f" Current frame is saved and new Overlay is created!")
                     fname=f'./Results/finalresult{n}.jpg'
                     fm.save(fname)
                     n=n+1
                     print(f"Frame is saved to {fname}")
                     fm.new()      
                     
        if cv2.waitKey(1) & 0xFF == ord('q') or command=="break" or command=="finish":
          break    
    
    #add label to the ESD tip
    #fm.add_pointer(tip_location)
    
    
    
    yolo_process.terminate()
    vosk_process.terminate()
    key_process.terminate()
    ms_process.terminate()
    
    
    yolo_process.join()
    vosk_process.join()
    key_process.join()
    ms_process.join()
    
    cv2.destroyAllWindows()
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

