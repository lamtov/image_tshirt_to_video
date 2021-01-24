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

logging.basicConfig(filename='./log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running  ")


class List_Image():
    def __init__(self, list_png, list_png_path):
        self.lock_1 = Lock()
        self.list_png = list_png
        self.list_png_path = list_png_path
        self.count = -1
        self.isDone = False

    def get_next_image(self):
        self.lock_1.acquire()
        try:
            self.count = self.count + 1
            if self.count == len(self.list_png) - 1:
                self.isDone = True
            if self.count < len(self.list_png):
                return (self.list_png[self.count], self.list_png_path[self.count])
            else:
                self.isDone = True
                return (-1, -1)
        except Exception as e:
            logging.debug(str(e))
            self.isDone = True
            self.lock_1.release()
        finally:
            self.lock_1.release()


cur_dir = os.getcwd()


class MyWindow:
    def __init__(self, win):

        self.start_open=1
        self.end_open=25
        self.start_model=26
        self.end_model=214
        self.start_close=215
        self.end_close=240
        self.start_text=241
        self.end_text=473

        self.folder_png = cur_dir + "/dataset/folder_png"

        self.list_png = []
        self.background_default = cur_dir + "/dataset/background_default.png"

        self.frame_set=cur_dir+'/dataset/frame_set'
        self.file_mp4 = cur_dir + "/dataset/origin_video.mp4"
        self.folder_output = cur_dir + "/dataset/folder_output"
        self.lbl0 = Label(win, text='NOTE: DOI KET QUA O OUTPUT FOLDER!', bg="white", fg="red", font=("Arial", 11))
        self.lbl1 = Label(win, text='LIST DESIGN PNG (default: ' + self.folder_png + ')', bg="black", fg="white",
                          font=("Arial", 10))
        self.lbl11 = Label(win, text='PNG: (default: ' + self.folder_png + ')', font=("Arial", 10))
        self.lbl3 = Label(win, text='FILE VIDEO MP4 (default: ' + self.file_mp4 + ')', bg="black", fg="white",
                          font=("Arial", 10))
        self.lbl33 = Label(win, text='MP4: (default: ' + self.file_mp4 + ')', font=("Arial", 10))
        self.lbl4 = Label(win, text='OUTPUT FOLDER (default: ' + self.folder_output + ')', bg="black", fg="white",
                          font=("Arial", 10))
        self.lbl44 = Label(win, text='OUTPUT: (default: ' + self.folder_output + ')', font=("Arial", 10))
        self.t1 = Button(text='Chon thu muc chua list design png', bg="gray", fg="blue",
                         command=self.callback_folder_png)
        self.t3 = Button(text='Chon  file video MP4', bg="gray", fg="blue", command=self.callback_file_mp4)
        self.t4 = Button(text='Chon thu muc output', bg="gray", fg="blue", command=self.callback_folder_output)

        self.lbt1 = Label(win, text='start time image (milisecond): ')
        self.et1 = Entry(win, bd=5, foreground="green")
        self.lbt2 = Label(win, text='end time image: (milisecond) ')
        self.et2 = Entry(win, bd=5, foreground="green")
        self.lbt3 = Label(win, text='start time link: (milisecond)')
        self.et3 = Entry(win, bd=5, foreground="green")
        self.lbt4 = Label(win, text='end time link: (milisecond)')
        self.et4 = Entry(win, bd=5, foreground="green")

        self.et1.insert(END, str(self.start_model))
        self.et2.insert(END, str(self.end_model))
        self.et3.insert(END, str(self.start_text))
        self.et4.insert(END, str(self.end_text))

        self.b1 = Button(win, text='RUN', bg="green", fg="white", command=self.start_run)
        self.b2 = Button(win, text='STOP', bg="red", fg="white", command=self.stop_run)
        self.t5 = Label(win, text='KET QUA:')
        self.lbt55 = Label(win, text='number thread')
        self.et55 = Entry(win, bd=2, foreground="green")
        self.et55.insert(END, '1')
        self.is_new_background=tk.IntVar(value=1)
        self.c1 = tk.Checkbutton(window, text='is_new_background', variable=self.is_new_background, onvalue=1, offvalue=0)
        self.lbt1.place(x=130, y=190)
        self.et1.place(x=305, y=190)
        self.lbt2.place(x=480, y=190)
        self.et2.place(x=655, y=190)
        self.lbt3.place(x=130, y=230)
        self.et3.place(x=305, y=230)
        self.lbt4.place(x=480, y=230)
        self.et4.place(x=655, y=230)
        self.lbl0.place(x=0, y=10)
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=1000, y=50)
        self.lbl11.place(x=130, y=80)
        self.lbl3.place(x=100, y=120)
        self.t3.place(x=1000, y=120)
        self.lbl33.place(x=130, y=150)
        self.lbl4.place(x=100, y=270)
        self.t4.place(x=1000, y=270)
        self.lbl44.place(x=130, y=300)
        self.b1.place(x=570, y=330)
        self.b2.place(x=640, y=330)
        self.t5.place(x=200, y=370)
        self.c1.place(x= 380, y=330)
        self.lbt55.place(x=130, y=330)
        self.et55.place(x=230, y=330)





    def callback_folder_png(self):
        try:
            self.folder_png = fd.askdirectory()
            self.lbl11.configure(text=str('PNG: ' + self.folder_png))
        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR callback_folder_png")

    def callback_file_mp4(self):
        try:
            self.file_mp4 = fd.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
            self.lbl33.configure(text=str('MP4: ' + self.file_mp4))
        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR callback_file_mp4")

    def callback_folder_output(self):
        try:
            self.folder_output = fd.askdirectory()
            self.lbl44.configure(text=str('OUTPUT: ' + self.folder_output))
        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR callback_file_mp4")

    def convert_video_to_int_size(self):
        try:
            mp4_origin = cv2.VideoCapture(self.file_mp4)
            width_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = mp4_origin.get(cv2.CAP_PROP_FPS)
            mp4_fix_size = cv2.VideoWriter(cur_dir + "/dataset/folder_output" + '/video_fix_size.mp4',
                                           cv2.VideoWriter_fourcc(*'MP4V'), fps, (width_origin, height_origin))
            while True:
                ret, frame = mp4_origin.read()
                if ret:
                    frame = cv2.resize(frame, (width_origin, height_origin))
                    mp4_fix_size.write(frame)
                    cv2.waitKey(1)
                else:
                    break
            self.file_mp4 = cur_dir + "/dataset/folder_output" + '/video_fix_size.mp4'
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG")

    def fix_file_mp4(self):
        try:
            self.t5.configure(text=str("RUNNING " + str('FIX FILE SIZE')), bg="gray", fg="blue")
            file_mp4_origin = cv2.VideoCapture(self.file_mp4)
            width_origin = file_mp4_origin.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
            height_origin = file_mp4_origin.get(cv2.CAP_PROP_FRAME_HEIGHT)
            if width_origin.is_integer() and height_origin.is_integer():
                width_origin = int(width_origin)
                height_origin = int(height_origin)
                logging.debug("OK")
            else:
                self.convert_video_to_int_size()
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG fix_file_mp4")

    def write_original_video_with_background_default(self):
        try:
            self.t5.configure(text=str("RUNNING " + str('write_original_video_with_background_default')), bg="gray", fg="blue")
            mp4_origin = cv2.VideoCapture(self.file_mp4)
            width_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = mp4_origin.get(cv2.CAP_PROP_FPS)
            original_new_background = cv2.VideoWriter(cur_dir + "/dataset/origin_video_add_background.mp4",
                                           cv2.VideoWriter_fourcc(*'MP4V'), fps, (width_origin, height_origin))
            count=1
            back_ground_image= Image.open(self.background_default).convert('RGBA')
            back_ground_image.resize((width_origin, height_origin))
            while True:
                ret, frame = mp4_origin.read()
                if ret:
                    if count>=self.start_open and count<=self.end_close:
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        pilim = Image.fromarray(frame)
                        pilim.paste(back_ground_image, box=(0,0))


                        if count>=self.start_model and count<=self.end_model:
                            frame_gif=Image.open(self.frame_set+'/'+'frame_'+str(count)+'.png').convert('RGBA')
                            pilim.paste(frame_gif, box=(0, 0),mask=frame_gif)
                        frame = np.array(pilim)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    original_new_background.write(frame)
                    cv2.waitKey(1)
                    count=count+1
                else:
                    break

            self.file_mp4 = cur_dir + "/dataset/origin_video_add_background.mp4"
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG write_original_video_with_background_default")
    def merge_video_and_file(self, link_sp, path_image):
        try:
            mp4_origin = cv2.VideoCapture(self.file_mp4)
            width_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
            height_origin = int(mp4_origin.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = mp4_origin.get(cv2.CAP_PROP_FPS)
            mp4_out = cv2.VideoWriter(cur_dir + "/dataset/folder_output" + '/' + link_sp + '.mp4',
                                      cv2.VideoWriter_fourcc(*'MP4V'), fps, (width_origin, height_origin))

            image = Image.open(path_image).convert('RGBA')
            w, h = image.size
            box = None
            if (w * height_origin < width_origin * h):
                image = image.resize((int(w * (height_origin / h)), height_origin))
                box = (int((width_origin - w * height_origin / h) / 2), 0)
            else:
                image = image.resize((width_origin, int(h * width_origin / w)))
                box = (0, int((height_origin - h * width_origin / w) / 2))

            # font1 = ImageFont.truetype(cur_dir + "/dataset/font/" + "font_get_it_here.ttf", 100)
            font2 = ImageFont.truetype(cur_dir + "/dataset/font/" + "font_link.ttf", 70)
            # text1 = "GET IT HERE"
            text2 = link_sp.replace('_', '/')
            # textsize1 = font1.getsize(text1)
            textsize2 = font2.getsize(text2)
            # textX1 = (width_origin - textsize1[0]) / 2
            # textY1 = (height_origin) / 2 - textsize1[1]
            textX2 = (width_origin - textsize2[0]) / 2
            textY2 = (height_origin) / 2 + 40
            time_range = (self.end_frame_text - self.start_frame_text) / 10
            count=1
            while True:
                ret, frame = mp4_origin.read()
                if ret:
                    # time_stamp = mp4_origin.get(cv2.CAP_PROP_POS_MSEC)
                    if count >= self.start_open and count <= self.end_close:
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        pilim = Image.fromarray(frame)
                        pilim.paste(image, box=box, mask=image)

                        #
                        #
                        if count>=self.start_open and count<=self.end_open:
                            frame_gif=Image.open(self.frame_set+'/'+'frame_'+str(count)+'.png').convert('RGBA')
                            pilim.paste(frame_gif, box=(0, 0),mask=frame_gif)
                        if count>=self.start_close and count<=self.end_close:
                            frame_gif=Image.open(self.frame_set+'/'+'frame_'+str(count)+'.png').convert('RGBA')
                            pilim.paste(frame_gif, box=(0, 0),mask=frame_gif)
                        frame = np.array(pilim)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        mp4_out.write(frame)
                        cv2.waitKey(1)
                    elif count >= self.start_frame_text and count <= self.end_frame_text:
                        try:
                            cur_time = (count - self.start_frame_text)
                            if cur_time < time_range:
                                cur_time = time_range - cur_time
                                opacity = int(cur_time / time_range * 80)
                            elif cur_time >= 9 * time_range:
                                opacity = int(abs(time_range * 9 - cur_time) / time_range * 80)
                            else:
                                opacity = 0

                            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                            pilim = Image.fromarray(frame)
                            draw = ImageDraw.Draw(pilim)
                            # draw.text((int(textX1), int(textY1 + opacity)), text1, font=font1)
                            draw.text((int(textX2), int(textY2 + opacity)), text2, font=font2)
                            frame = np.array(pilim)
                            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                            mp4_out.write(frame)
                            cv2.waitKey(1)
                        except Exception as e:
                            print(e)
                            logging.debug(str(e))
                    else:
                        mp4_out.write(frame)
                        cv2.waitKey(1)
                    count=count+1
                else:
                    break

            mp4_origin.release()
            mp4_out.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)
            logging.debug(str(e))
            print("SOME THING WRONG + merge_video_and_file")
            logging.debug("SOME THING WRONG + merge_video_and_file")

    def thread_merge_video(self):
        try:
            while self.List_Image.isDone == False:

                link_sp, path_image = self.List_Image.get_next_image()
                link_sp = link_sp[:-4]
                self.t5.configure(text=str("RUNNING" + str(link_sp)), bg="gray", fg="blue")
                logging.debug("RUNNING" + str(link_sp))
                self.merge_video_and_file(link_sp, path_image)
                self.t5.configure(text=str("DONE" + str(link_sp)), bg="gray", fg="red")
                logging.debug("DONE" + str(link_sp))
                if self.List_Image.isDone:
                    self.t5.configure(text=str("DONE ALL"), bg="gray", fg="white")
                    logging.debug("DONE ALL")
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG + thread_merge_video")

    def start_run(self):
        try:
            self.start_frame_image = int(self.et1.get())
            self.end_frame_image = int(self.et2.get())
            self.start_frame_text = int(self.et3.get())
            self.end_frame_text = int(self.et4.get())
            self.number_thread = int(self.et55.get())

            # print(self.is_new_background.get())


        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG")
        try:
            self.fix_file_mp4()
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG")
        if self.is_new_background.get():
            try:
                self.write_original_video_with_background_default()
            except Exception as e:
                logging.debug(str(e))
                logging.debug("SOME THING WRONG")
        try:
            list_png = [f for f in listdir(self.folder_png) if
                        isfile(join(self.folder_png, f)) and ('png' in f or 'jpg' in f)]
            list_png_path = [self.folder_png + '/' + f for f in list_png]

            self.List_Image = List_Image(list_png, list_png_path)
            logging.debug(list_png)

            for i in range(0, self.number_thread):
                executor = ThreadPoolExecutor(1)
                executor.submit(self.thread_merge_video)
        except Exception as e:
            logging.debug(str(e))
            logging.debug("SOME THING WRONG")

        # print(list_png)
        # print(list_png_path)
        # print(self.folder_png)
        # print(self.file_psd)
        # print(self.file_mp4)
        # print(self.folder_output)
        # for index, path in enumerate(list_png_path):
        #     link_sp = list_png[index][:-4]
        #     path_image = list_png_path[index]
        #     self.merge_video_and_file(path_image, link_sp)

        logging.debug("STOP")

    def stop_run(self):
        try:
            self.List_Image.isDone = True
            self.t5.configure(text=str("DONE ALL"), bg="gray", fg="white")
            logging.debug('DONE ALL')
        except Exception as e:
            logging.debug(str(e))
            logging.debug("STOP")


window = Tk()
try:
    imagebg = Image.open(cur_dir + '/dataset/back_ground.jpg')
    imagebg.resize((1300, 450))
    photo_image = ImageTk.PhotoImage(imagebg)
    label = tk.Label(window, image=photo_image)
    label.pack()
except Exception as e:
    logging.debug(str(e))
mywin = MyWindow(window)

window.title('CONVERT IMAGE TO VIDEO')
window.geometry("1300x450+10+10")
window.mainloop()
