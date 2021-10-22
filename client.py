from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import socket
import commander
import threading
import dirtree
import keylogGUI
import processGUI
import appGUI
import loadimage
from time import sleep

from timerGUI import TimerWindow
class Client(object):
    def __init__(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Client")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="10 10 25 25")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        

        #IP addr. input space
        self.ip_addr = StringVar()
        ip_addr_entry = ttk.Entry(self.mainframe, width=40, textvariable=self.ip_addr)
        ttk.Label(self.mainframe, text='IP Addr.').grid(column=1, row=1, sticky=(W,E))
        ip_addr_entry.grid(column=1,row=2,sticky=(W,E))

        #Port input space
        self.port = StringVar()
        port_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.port)
        ttk.Label(self.mainframe, text='Port').grid(column=2, row=1, sticky=(W,E))
        port_entry.grid(column=2, row=2, sticky=(W,E))
        
        #Connect button
        connectButton = ttk.Button(self.mainframe, text='Connect', command=self.Connect)
        connectButton.grid(column=3, row=2, sticky=(E))

        #Functions
        ttk.Label(self.mainframe, text='Command').grid(column=1,row=3,sticky=(W,E))
        self.func = StringVar()
        funcEntry = ttk.Combobox(self.mainframe, textvariable=self.func, width=40)
        funcEntry['values'] = ("Show running processes", "Show running apps", "Shutdown and Logout", "Screen capture"
                                , "Keylog and lock keyboard", "Show and copy/delete files")
        funcEntry.state(["readonly"])
        funcEntry.grid(column=1, row=4, sticky=(W,E))

        #Confirmation button
        self.confButton = ttk.Button(self.mainframe, text='Go', command=self.act, state=DISABLED)
        self.confButton.grid(column=3, row=4, sticky=(E,S))

        subframe = ttk.Frame(self.root, padding='3 3 12 12')
        subframe.grid(row=1, column=0)

        self.State = ttk.Label(subframe, text='Not connected')
        self.State.grid(column=1, row=1)


        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
        
        for i in range(5):
            self.mainframe.rowconfigure(i, weight=1)
    #Connect to the server
    def Connect(self):
        try:
            self.IP = str(self.ip_addr.get())
            self.port_no = int(self.port.get())
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.IP, self.port_no))
            self.connection.send('Hello'.encode())


            self.State['text'] = "Connected to server: " + self.IP + ":" + str(self.port_no) + "."
            self.confButton['state'] = NORMAL
        except:
            messagebox.showerror(title='Connect error', message='An error occurred while trying to connect to the address ' + 
                            self.IP + ":" + str(self.port_no) + ".")
            self.confButton['state'] = DISABLED
            
        
    def act(self):
        func = self.func.get()
        if func == "Show running processes":
            self.command_ShowProcess()
        elif func == "Show running apps":
            self.command_ShowApps()
        elif func == "Shutdown and Logout":
            self.command_Shutdown()
        elif func == "Screen capture":
            self.command_CaptureScreen()
        elif func == "Keylog and lock keyboard":
            self.command_Keylog()
        elif func == "Show and copy/delete files":
            self.command_DirTree()

    
    def command_Shutdown(self):
        cmd = commander.ShutdownCMD(self.root)
        cmd.NewInstance()
        if cmd.isExcuted==commander.StateOut.Nope.value:
            cmd.command = 'Nope'
        elif cmd.isExcuted == commander.StateOut.LogOut.value:
            cmd.command = 'LOGOUT'
        elif cmd.isExcuted == commander.StateOut.ShutDown.value:
            cmd.command = 'SHUTDOWN'
            cmd.delay_time.set('0')
        else:
            cmd.command = 'SHUTDOWN'
        command = cmd.command + " " + cmd.delay_time.get()
        self.sendToServer(command)
        if cmd.isExcuted == commander.StateOut.ShutDownWithTime:
            timerWindow = TimerWindow(int(cmd.delay_time.get()),self.root)
            timerWindow.submit()
        pass

    def command_CaptureScreen(self):
        cmd = 'CAPSCR'
        print(cmd)
        self.sendToServer(cmd)
        scrshot = open("capture.png", 'wb')
        while True:
            data = self.connection.recv(1024)
            if len(data) < 1024:
                scrshot.write(data)
                break
            scrshot.write(data)
        ins = loadimage.WindowScreenShot('capture.png',Toplevel(self.root))
        scrThread =threading.Thread(target=ins.loadImg())
        scrThread.start()
        scrshot.close()
    def command_ShowProcess(self):
        ins = processGUI.Process(self.root,self.IP,self.port_no)
        processThread=threading.Thread(target=ins.loadProcess())
        processThread.start()
    def command_ShowApps(self):
        ins = appGUI.App(self.root,self.IP,self.port_no)
        processThread=threading.Thread(target=ins.loadApp())
        processThread.start()
    def command_DirTree(self):
        ft = dirtree.FileTree(self.root, self.IP, self.port_no)
        instanceThread = threading.Thread(target=ft.startInstance())
        instanceThread.start()
    
    def command_Keylog(self):
        keyloggerGUI = keylogGUI.KeyloggerWindow(self.root,self.IP,self.port_no)
        keylogThread = threading.Thread(target=keyloggerGUI.loadKeyLog())
        keylogThread.start()
       

    #Ham gui toi server
    def sendToServer(self,Str):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.IP, self.port_no))
        self.connection.send(Str.encode())
    
    def NewInstance(self):
        self.root.mainloop()
    def CloseConnection(self):
        if type(self.connection) == socket.socket:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.IP, self.port_no))
            self.connection.send(b"")
            self.connection.close()
            
ins = Client()
ins.NewInstance()
