from tkinter import *
from tkinter import ttk
import threading
import socket
from time import sleep
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
import re
class Kill(Frame):
    def __init__(self,master,IP,port_no,function='KILL'):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.pid = StringVar()
        self.master.resizable(FALSE, FALSE)
        self.IP=IP
        self.port_no=port_no
        self.entryInput = ttk.Entry(self.master,width=30,textvariable=self.pid)
        if function=='START':
            self.entryInput.insert(0,'ProcessName')
        elif function=='KILL':
            self.entryInput.insert(0,'PID')
        self.entryInput.place(x=5,y=5)

        clickButton = ttk.Button(self.master, text=function,command=self.sendProcess)
        clickButton.place(x=320,y=5,height=35)
    def load(self,name='Kill'):
        self.master.wm_title(name)
        self.master.geometry('500x50')
        self.master.mainloop()
        self.master.destroy()
    def sendProcess(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send(("KILL " + self.pid.get()).encode())
        data = self.conn.recv(8)
        if data.decode() == 'TRUE':
            global PID_Deleted
            PID_Deleted=self.pid.get()
            self.master.quit()
        else:
            print("Failed to kill process.")
class Start(Kill):
    def __init__(self, master,IP,port_no,function):
        super().__init__(master,IP,port_no, function=function)
    def sendProcess(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send(("START " + self.pid.get()).encode())
        data = self.conn.recv(8)
        if data.decode() == 'TRUE':
            self.master.quit()
        else:
            print("Failed to start process.")
        pass
class Process(Frame):
    def __init__(self,master, IP, port_no):
        Frame.__init__(self, master)
        self.master = master #Toplevel(master)
        self.master.resizable(0,0)
        
        self.IP=IP
        labelProcess = ttk.Label(self.master,text='Chương trình diệt process')
        labelProcess.grid(row=0,column=0,columnspan=4,padx=10,pady=10,sticky='we')
    

        killButton = ttk.Button(self.master, text='Kill',command=self.eventKillProcess)
        killButton.grid(row=1,column=0,padx=10,sticky='w')

        watchButton = ttk.Button(self.master, text='Watch',command=self.eventWatchProcess)
        watchButton.grid(row=1,column=1,sticky='w')

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDeleteProcess)
        deleteButton.grid(row=1,column=2,sticky='e')

        startButton = ttk.Button(self.master, text='Start',command=self.eventStartProcess)
        startButton.grid(row=1,column=3,padx=10,pady=5,sticky='e')
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

    def loadProcess(self):
        self.master.wm_title("Process")
        self.master.geometry('500x450')
        self.master.mainloop()
    def eventKillProcess(self):
        ins=Kill(self.master,self.IP,self.port_no)
        ins.load()
        self.deleteInTreeView(str(PID_Deleted))
    def eventDeleteProcess(self):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            self.treeViewProcess.delete(child)
    def eventWatchProcess(self):
        self.eventDeleteProcess()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send("SHWPRC".encode())
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            if data.decode().find('STOPRIGHTNOW')!=-1:
                break
            if len(str(data.decode()))!=1 and str(data.decode()).find('ThreadCount')==-1:
                arr=re.sub(' +', ' ',data.replace(b'\x00', b'').decode('utf-8')).split(' ')
                print(arr)
                chain=''
                for i in range(0,len(arr)-3,1):
                    chain+=arr[i]
                if arr[1]!='ProcessId' and arr[2]!='ThreadCount':
                    self.treeViewProcess.insert("",'end',text=chain,values=(str(arr[len(arr)-3]),str(arr[len(arr)-2])))
                chain=''
            #print(data.decode())
    def eventStartProcess(self):
        ins=Start(self.master,self.IP,self.port_no,'START')
        ins.load('Start')
    def deleteInTreeView(self,PID):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            if str(self.treeViewProcess.item(child)['values'][0]) == PID:
                self.treeViewProcess.delete(child)
hello = Process(Tk(),'192.168.1.7',1024)
hello.loadProcess()