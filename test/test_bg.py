import tkinter as tk
import  os
cur_dir=os.getcwd()
from PIL import Image, ImageTk
window = tk.Tk()
image = Image.open(cur_dir + '/dataset/447857-PF1FKN-86-02.png')
photo_image = ImageTk.PhotoImage(image)
label = tk.Label(window, image = photo_image)
label.pack()

window.mainloop()