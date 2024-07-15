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
# Replace with path to your downloaded model
#model_path = "./vosk-model-cn-0.22"
model_path = "./vosk-model-en-us-0.42-gigaspeech"
# Load the model
model = Model(model_path)

# Create recognizer with specified sample rate
recognizer = KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        
# Open audio stream from microphone
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8192,
    input_device_index=1
    
)

# Start the stream
stream.start_stream()

print("Speak now...")

while True:
    # Read audio data from the stream
    data = stream.read(4096)

    # Feed the data to the recognizer
    if recognizer.AcceptWaveform(data):
        # Get the recognized text
        text = recognizer.Result()

        # Print the recognized text
        print(f"Recognized: {text[14:-3]}")

        if text[14:-3]=='finish' or text[14:-3]== 'done' or text[14:-3]== 'quite' :
            keyboard.press('q')
            time.sleep(0.05)
            keyboard.release('q')
   
            break
        elif text[14:-3]=='mark':
            keyboard.press('a')
            time.sleep(0.05)
            keyboard.release('a')
        elif text[14:-3]=='KV':
            keyboard.press('K')
            time.sleep(0.05)
            keyboard.release('K')
            keyboard.press('V')
            time.sleep(0.05)
            keyboard.release('V')
            
        elif text[14:-3]=='four' or text[14:-3]=='for' :
            keyboard.press('4')
            time.sleep(0.05)
            keyboard.release('4')
            
        elif text[14:-3]=='eight':
                keyboard.press('8')
                time.sleep(0.05)
                keyboard.release('8')
                
        elif text[14:-3]=='mark' or text[14:-3]=='non-contact':
            keyboard.press('a')
            time.sleep(0.05)
            keyboard.release('a')
            
        elif text[14:-3]=='contact' or text[14:-3]=='contract' or text[14:-3]=='concept' or text[14:-3]=='contextac':
                keyboard.press('c')
                time.sleep(0.05)
                keyboard.release('c')
        elif text[14:-3]=='air' or text[14:-3]=='hair':
                       keyboard.press('a')
                       time.sleep(0.05)
                       keyboard.release('a')
                       
# Stop the stream and close PyAudio
stream.stop_stream()
stream.close()
p.terminate()

print("Finished")