# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:58:49 2024

@author: kuifenhu
"""

from VoiceObj import VoiceObject 
vc=VoiceObject()
vc.model_path = "C:/Users/kuifenhu/yolo/vosk-model-en-us-0.42-gigaspeech"
vc.channel=1
vc.ini()
print('Start Listening....')
while True:
    command = vc.listen()       
    if len(command): 
        print(f"Received Command: {command}")
    if command == "finish" or command == "quit" or command == "done" :
        print(f"Finish listening....")
        break
        
