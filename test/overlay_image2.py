#!/usr/bin/env python3

import cv2
import random
import numpy as np
from PIL import Image

# Load a speedo image which has transparency
speedo = Image.open('dataset/insss.png').convert('RGBA')

capture = cv2.VideoCapture("dataset/input.mp4")
out = cv2.VideoWriter('dataset/test.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 25, (1920, 1080))
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

speedo=speedo.resize((300, 300))

def velocity():
    now = (random.randint(0,100))
    return now

while True:
    ret, frame = capture.read()
    if ret:
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Velocity:',(15,580),font,0.7,(255,255,255),1)
        cv2.putText(frame,'Distance:',(15,620),font,0.7,(255,255,255),1)
        cv2.putText(frame,'Inclination:',(15,660),font,0.7,(255,255,255),1)
        cv2.putText(frame,'Orientation:',(15,700),font,0.7,(255,255,255),1)
        cv2.putText(frame, str(velocity()), (130,580),font,0.7,(255,255,255),1)
        cv2.putText(frame,'KM/H',(165,580),font,0.7,(255,255,255),1)

        # Make PIL image from frame, paste in speedo, revert to OpenCV frame
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        pilim = Image.fromarray(frame)
        pilim.paste(speedo,box=(80,20),mask=speedo)
        frame = np.array(pilim)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        out.write(frame)
        cv2.imshow("Testing", frame)
        cv2.waitKey(1)

    else:
        break

capture.release()
out.release()
cv2.destroyAllWindows()

