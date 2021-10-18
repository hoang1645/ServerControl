from tkinter import *
from tkinter import ttk
import socket
# pip install pillow
from pyautogui import scroll
from tkinter import messagebox
mpApplication={}
#os.system('taskkill /f /im brave.exe')
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
        self.master.geometry('500x50')
        self.master.mainloop()

    def sendProcess(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.IP, self.port_no))
            self.conn.send(("KILLAPP " + self.pid.get()).encode())
            data = self.conn.recv(8)
            if data.decode() == 'TRUE':
                global PID_Deleted
                PID_Deleted=self.pid.get()
                self.master.quit()
            else:
                messagebox.showerror("Error","Failed to kill an app!")
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
            if data.decode() == 'TRUE':
                self.master.quit()
            else:
                messagebox.showerror("Error","Failed to start an app!")
        except:
            messagebox.showerror("Error","Not Found!")
class App(Frame):
    def __init__(self,master, IP, port_no):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.resizable(FALSE, FALSE)
        self.IP=IP
        self.port_no=port_no

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
    
        killButton = ttk.Button(self.master, text='Kill',command=self.eventKillApp)
        killButton.grid(row=1,column=0,padx=10,sticky='w')

        watchButton = ttk.Button(self.master, text='Watch',command=self.eventWatchApp)
        watchButton.grid(row=1,column=1,sticky='w')

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDeleteAppProcess)
        deleteButton.grid(row=1,column=2,sticky='e')

        startButton = ttk.Button(self.master, text='Start',command=self.eventStartApp)
        startButton.grid(row=1,column=3,padx=10,pady=5,sticky='e')
        #file status
        
        self.treeViewProcess=ttk.Treeview(self.master)
        s = ttk.Style()
        s.configure('Treeview', rowheight=30)
        
        self.treeViewProcess["columns"]=("one","two")
        self.treeViewProcess.column("#0",width=165,anchor=CENTER)
        self.treeViewProcess.column("one",width=165,anchor=CENTER)
        self.treeViewProcess.column("two",width=165,anchor=CENTER)
        self.treeViewProcess.heading("#0",text='Application Name')
        self.treeViewProcess.heading("one",text='Application ID')
        self.treeViewProcess.heading("two",text='Count Threads')
        #Mau
        #for i in range(0,10,1):
            #self.treeViewProcess.insert("",'end',text='notepad.exe',values=("1234",str(i)))
        self.treeViewProcess.grid(row=2,column=0,columnspan=4,padx=10,pady=5,sticky='we')

    def loadApp(self):
        self.master.wm_title("App Manager")
        self.master.geometry('510x400')
        self.master.mainloop()
    def eventKillApp(self):
        ins=Kill(self.master,self.IP,self.port_no)
        ins.load()
        self.deleteInTreeView(str(PID_Deleted))
    def eventDeleteAppProcess(self):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            self.treeViewProcess.delete(child)
    #Chinh sua xong
    def eventWatchApp(self):
        self.eventDeleteAppProcess()
        strRev=''
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send("SHWPRCAPP".encode())
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            if data.decode().find('STOPRIGHTNOW')!=-1:
                break
            strRev+=data.decode('utf8')
        finalAppRunning = strRev.split()
        for i in range(0,len(finalAppRunning)//3,1):
            self.treeViewProcess.insert("",'end',text=finalAppRunning[3*i],values=(finalAppRunning[3*i+1],finalAppRunning[3*i+2]))
    #Giu nguyen
    
    def eventStartApp(self):
        ins=Start(self.master,self.IP,self.port_no,'START')
        ins.load('Start')
    def deleteInTreeView(self,PID):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            if str(self.treeViewProcess.item(child)['values'][0]) == PID:
                self.treeViewProcess.delete(child)