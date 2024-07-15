# Automated ESD Test Data Logging Using Computer Vision and Voice Control

## Abstract

This paper proposes a novel approach to Electrostatic Discharge (ESD) test data logging utilizing two open-source machine learning models for computer vision and voice control. Traditional ESD testing manually recode data like test level, tip type, and discharge location, leading to inefficiencies and potential errors. This work presents an automated system leveraging YOLO object detection for real-time tip location tracking and voice recognition with VOSK for operator commands.

The YOLO model is trained to recognize the ESD tip shape. The camera is therefore capable to track the location of the tip on DUT lively. Upon receiving a voice command to mark, the system automatically logs:

- Test level (by voice command)
- Tip type (identified by YOLO)
- Discharge location (extracted from the video frame bounding box)

Both vision and voice models runs on local machine with multiprocessing algorithm to reduce the latency. It could use API to cloud power to improve the performance. This program enables single-operator testing, eliminates manual data entry, and improves data accuracy through real-time tracking.

Training steps for the YOLO models will be elaborated upon in the full paper. The paper demonstrates the application of computer vision and voice control model in the test automation. It can be extended to other fields such as EM scanning etc.