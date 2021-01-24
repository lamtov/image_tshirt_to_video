import cv2
import os
from tkinter import *
from tkinter import filedialog as fd
import tkinter as tk
from os import listdir
from os.path import isfile, join
import os
import cv2
import numpy as np
from PIL import ImageTk, ImageFont, ImageDraw, Image
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import logging
cur_dir= os.getcwd()
folder_frame = cur_dir+ '/dataset/frame_set/'


list_frame = [f for f in listdir(folder_frame) if
                        isfile(join(folder_frame, f)) and ('png' in f or 'jpg' in f)]
list_png_path = [folder_frame + '/' + f for f in list_frame]
f =open(folder_frame+'README.txt','a')

for index,png in enumerate(list_png_path):
    f.write(list_frame[index] +'\n')

    os.rename(png, folder_frame + '/frame_'+list_frame[index].split('_')[1]+'.png')
f.close()


# file_mp4 = cur_dir + "/dataset/origin_video2.mp4"
# mp4_origin = cv2.VideoCapture(file_mp4)
#
# width_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_WIDTH))
# height_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = mp4_origin.get(cv2.CAP_PROP_FPS)
# mp4_out = cv2.VideoWriter(cur_dir + "/dataset/" + 'origin_video_default' + '.mp4',
#                                       cv2.VideoWriter_fourcc(*'MP4V'), fps, (width_origin, height_origin))
# count=1
#
# background =Image.open(cur_dir + "/dataset/background_default.png").convert('RGBA')
start_open=1
end_open=25
start_model=26
end_model=214
start_close=215
end_close=240
start_text=241
end_text=473
# while True:
#
#     ret, frame = mp4_origin.read()
#     if ret:
#         if count>=start_open and count<=end_close:
#
#             time_stamp = mp4_origin.get(cv2.CAP_PROP_POS_MSEC)
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#             pilim = Image.fromarray(frame)
#             pilim.paste(background, box=(0,0))
#             frame = np.array(pilim)
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#
#         mp4_out.write(frame)
#         cv2.waitKey(1)
#             #cv2.imwrite(cur_dir + "/dataset/frame2/"+"frame_"+str(i)+"__"+str(time_stamp)+""+".png" ,frame)
#
#         count+=1
#     else:
#         break

