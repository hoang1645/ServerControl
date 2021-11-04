from tkinter import *
from tkinter import ttk
import threading
import socket
from time import sleep
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
from tkinter import messagebox
import re
class Kill(Frame):
    def __init__(self,master,IP,port_no,function='KILL'):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.resizable(FALSE, FALSE)

        self.pid = StringVar()
        self.IP=IP
        self.port_no=port_no

        self.entryInput = ttk.Entry(self.master,width=40,textvariable=self.pid)
        if function=='START':
            self.entryInput.insert(0,'ProcessName')
        elif function=='KILL':
            self.entryInput.insert(0,'PID')
        self.entryInput.grid(row=0,column=0,columnspan=2,sticky='w',padx=10,pady=10)

        clickButton = ttk.Button(self.master, text=function,command=self.sendProcess)
        clickButton.grid(row=0,column=3,padx=10,pady=10,sticky='e')

    def load(self,name='Kill'):
        self.master.wm_title(name)
        self.master.mainloop()

    def sendProcess(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.IP, self.port_no))
            self.conn.send(("KILL " + self.pid.get()).encode())
            data = self.conn.recv(8)
            if data.decode() == 'TRUE':
                global PID_Deleted
                PID_Deleted=self.pid.get()
            else:
                messagebox.showerror("Error","Failed to kill a process!")
        except:
            messagebox.showerror("Error","Not Found!")

class Start(Kill):
    def __init__(self, master,IP,port_no,function):
        super().__init__(master,IP,port_no, function=function)
    def sendProcess(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.IP, self.port_no))
            self.conn.send(("START " + self.pid.get()).encode())
            data = self.conn.recv(8)
            if data.decode() != 'TRUE':
                messagebox.showerror("Error","Failed to start a process!")
        except:
            messagebox.showerror("Error","Not Found!")
        

class Process(Frame):
    def __init__(self,master, IP, port_no):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.resizable(0,0)
        
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)

        self.IP=IP
        self.port_no = port_no

        labelProcess = ttk.Label(self.master,text='Chương trình diệt process')
        labelProcess.grid(row=0,column=0,columnspan=4,padx=10,pady=10,sticky='we')
    

        killButton = ttk.Button(self.master, text='Kill',command=self.eventKillProcess)
        killButton.grid(row=1,column=0,padx=10,pady=5,sticky='news')

        watchButton = ttk.Button(self.master, text='Watch',command=self.eventWatchProcess,style="Accent.TButton")
        watchButton.grid(row=1,column=1,padx=10,pady=5,sticky='news')

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDeleteProcess)
        deleteButton.grid(row=1,column=2,padx=10,pady=5,sticky='news')

        startButton = ttk.Button(self.master, text='Start',command=self.eventStartProcess)
        startButton.grid(row=1,column=3,padx=10,pady=5,sticky='news')
        #file status
        
        self.treeViewProcess=ttk.Treeview(self.master)
        s = ttk.Style()
        s.configure('Treeview', rowheight=30)
        
        self.treeViewProcess["columns"]=("one","two")
        self.treeViewProcess.column("#0",width=160,anchor=CENTER)
        self.treeViewProcess.column("one",width=160,anchor=CENTER)
        self.treeViewProcess.column("two",width=160,anchor=CENTER)
        self.treeViewProcess.heading("#0",text='Name Process')
        self.treeViewProcess.heading("one",text='ID Process')
        self.treeViewProcess.heading("two",text='Count Threads')

        #Mau
        #for i in range(0,10,1):
            #self.treeViewProcess.insert("",'end',text='notepad.exe',values=("1234",str(i)))

        self.treeViewProcess.grid(row=2,column=0,columnspan=4,padx=10,pady=5,sticky='we')
    #Start Process GUI
    def loadProcess(self):
        try:
            self.master.wm_title("Process")
            self.master.mainloop()
        except:
            pass

    #Start kill window
    def eventKillProcess(self):
        ins=Kill(self.master,self.IP,self.port_no)
        ins.load()
        try:
            self.deleteInTreeView(str(PID_Deleted))
        except:
            pass
    #Delete in treeview
    def deleteInTreeView(self,PID):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            if str(self.treeViewProcess.item(child)['values'][0]) == PID:
                self.treeViewProcess.delete(child)
    #Start delete all process
    def eventDeleteProcess(self):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            self.treeViewProcess.delete(child)
    #Start watch process
    def eventWatchProcess(self):
        self.eventDeleteProcess()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send("SHWPRC".encode())
        answer = ""
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            if data.decode().find('STOPRIGHTNOW')!=-1:
                break
            answer += data.decode()
        ls = answer.split('\n')
        for line in ls:
            try:
                part = line.split(',')
                if len(part) != 3:
                    continue
                self.treeViewProcess.insert("",'end',text=part[0],values=(str(part[1]),str(part[2])))
            except:
                print('Catch error')
            
                
    def eventStartProcess(self):
        ins=Start(self.master,self.IP,self.port_no,'START')
        ins.load('Start')