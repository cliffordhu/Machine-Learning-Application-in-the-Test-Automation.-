# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:36:16 2024

@author: kuifenhu
"""

import cv2

def mouse_click_event(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
    print("Mouse clicked at coordinates: (" + str(x) + ", " + str(y) + ")")

# Open the video capture object (replace 0 with video source index if needed)
cap = cv2.VideoCapture(1)

# Create a named window
cv2.namedWindow('ESDCamera')

# Set the mouse callback function
cv2.setMouseCallback('ESDCamera', mouse_click_event)

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  if ret:
    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # Exit if 'q' key is pressed
    if key == ord('q'):
      break

  else:
    break

# Release capture object and destroy windows
cap.release()
cv2.destroyAllWindows()