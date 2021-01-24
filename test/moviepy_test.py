# Import everything needed to edit video clips
from moviepy.editor import *
from os import listdir
from os.path import isfile, join
import os

import cv2
import random
import numpy as np
from PIL import Image

# psApp = ct.CreateObject('Photoshop.Application', dynamic=True)
cur_dir=os.getcwd()

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip(cur_dir + "/dataset/origin_video.mp4").subclip(11,19)

# Reduce the audio volume (volume x 0.8)
# clip = clip.volumex(0.8)
print("OK")
# Generate a text clip. You can customize the font, color, etc.
txt_clip = ( TextClip("My Holidays 2013",fontsize=70,color='white')
             .set_position('center')
             .set_duration(10) )

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_position('center').set_duration(10)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile(cur_dir + "/dataset/myHolidays_edited.webm")