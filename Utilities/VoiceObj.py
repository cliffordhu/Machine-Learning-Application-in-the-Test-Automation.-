# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:59:40 2024

@author: kuifenhu
"""
from vosk import Model, KaldiRecognizer
#from vosk import Model
import pyaudio
import keyboard
import time

class VoiceObject:
    def __init__(self):
        self.model_path= "C:/Users/kuifenhu/vosk-model-en-us-0.42-gigaspeech"
        self.channel= 1
        
    def ini(self):
        # Replace with path to your downloaded model
        #model_path = "./vosk-model-cn-0.22"
        #self.model_path = "./vosk-model-en-us-0.42-gigaspeech"
        
        # Load the model
        model = Model(self.model_path)
    
        # Create recognizer with specified sample rate
        self.recognizer = KaldiRecognizer(model, 16000)
    
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
    
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))
            
        # Open audio stream from microphone
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channel,
            rate=16000,
            input=True,
            frames_per_buffer=4096,
            input_device_index=1)
        # Start the stream
        self.stream.start_stream()



    def listen(self):
        # Read audio data from the stream
        try:
            data = self.stream.read(8192)
            # Feed the data to the recognizer
            if self.recognizer.AcceptWaveform(data):
                # Get the recognized text
                text = self.recognizer.Result()
                command=text[14:-3]
                return(command)
            else: 
                return("") 
            
        except IOError as e:
            if e.errno == pyaudio.paInputOverflowed:
                print("Input overflowed, ignoring")
                # Handle the overflow (e.g., by clearing the stream)
                stream.read(stream.get_read_available())
            else:
                raise    
    


    def end(self):
                              
        # Stop the stream and close PyAudio
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("Finished")# -*- coding: utf-8 -*-
        """
        Created on Fri Jul 12 16:36:53 2024
        
        @author: kuifenhu
        """

