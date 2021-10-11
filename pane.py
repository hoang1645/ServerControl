from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll

class Kill(Frame):
    def __init__(self,master,ip,port_no,function='KILL'):
        Frame.__init__(self, master)
        self.master=master
        self.pid = StringVar()
        self.master.resizable(FALSE, FALSE)
        self.entryInput = ttk.Entry(self.master,width=30,textvariable=self.pid)
        self.entryInput.place(x=5,y=5)

        clickButton = ttk.Button(self.master, text=function,command=self.sendProcess)
        clickButton.place(x=320,y=5,height=35)
    def load(self,name='Kill'):
        self.master.wm_title(name)
        self.master.geometry('450x50')
        self.master.mainloop()
    def sendProcess(self):
        pass
class Start(Kill):
    def __init__(self, master, ip, port_no):
        super().__init__(master, ip, port_no, function='START')
        
ins=Start(Tk(),123,12)
ins.load('Start')