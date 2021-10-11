from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import time
import cv2
# pip install pillow
from PIL import Image, ImageTk,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class WindowScreenShot(Frame):
    def __init__(self,filepath, master=None):
        Frame.__init__(self, master)
        self.filepath=filepath
        self.master = master
        global img
        img = Image.open(filepath)
        img = img.resize((800, 500), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(img)
        panel = Label(self.master, image=imgTk)
        panel.image = imgTk
        panel.place(x=5,y=50)
        btn = Button(self.master, text='Save image', command=self.saveImg,width=20)
        btn.place(x=5,y=5)

    def loadImg(self):
        self.master.wm_title("Tkinter window")
        self.master.geometry("900x600")
        self.master.mainloop()
    def saveImg(self):
        files = [('All Files', '*.*'), 
             ('PNG Files', '*.png'),
             ('JPEG Files', '*.jpeg')]
        filename = filedialog.asksaveasfilename(filetypes=files, defaultextension=files,title='Save')
        img.save(filename)
        messagebox.showinfo(title='Success',message='You save image successfully')
