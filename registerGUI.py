from tkinter import *
from tkinter import ttk
import threading
import socket
from tkinter.filedialog import askopenfilename
# pip install pillow
from PIL import Image, ImageTk

class RegistryWindow(Frame):
    def __init__(self,master,IP,port_no):
        Frame.__init__(self, master)
        self.master=master
        self.master.resizable(FALSE, FALSE)
        self.IP=IP
        self.port_no=port_no
        #duong dan
        self.browsePath = StringVar()
        self.browseEntry = ttk.Entry(self.master, width=60, textvariable=self.browsePath)
        self.browseEntry.configure(state='disabled')
        self.browseEntry.place(x=5,y=5)

        browseButton = ttk.Button(self.master, text='Browser',command=self.browseFunction)
        browseButton.place(x=self.browseEntry.winfo_reqwidth()+10,y=5)

        #file registry
        self.regFile = StringVar()
        self.regEntry = ttk.Entry(self.master,width=60,textvariable=self.regFile)
        self.regEntry.configure(state='disabled')
        self.regEntry.place(x=5,y=self.browseEntry.winfo_depth()+10,height=80)

        sendButton = ttk.Button(self.master, text='Gửi',command=self.sendRegFileFunction)
        sendButton.place(x=self.browseEntry.winfo_reqwidth()+10,y=self.browseEntry.winfo_depth()+10,height=81)

        ttk.Label(self.master, text='Edit value').place(x=5,y=125)

        #Chon chuc nang
        self.vlist = ["Get value", "Set value", "Delete value","Create key", "Delete key"]
        self.combo = ttk.Combobox(self.master, values = self.vlist)
        self.combo.configure(width=70)
        self.combo.bind("<<ComboboxSelected>>", self.manageRegistryGUIFunction)
        
        self.combo.set("Pick an Option")
        self.combo.place(x=5,y=160)

        #regpath
        self.regPathText = StringVar()
        self.regPathEntry = ttk.Entry(self.master,width=73,textvariable=self.regPathText)
        self.regPathEntry.place(x=5,y=200)

        #Rubbish variable (used to trespass error)
        self.keyEntry = ttk.Entry()
        self.keyEntry1 = ttk.Entry()
        self.valueEntry = ttk.Entry()
        self.comboData = ttk.Combobox()


        #file status
        self.statusText = StringVar()
        self.statusEntry = ttk.Entry(self.master,width=73,textvariable=self.statusText)
        self.statusEntry.configure(state='disabled')
        self.statusEntry.place(x=5,y=280,height=80)

        sendRegButton = ttk.Button(self.master, text='Gửi',command=self.sendRegCommand)
        sendRegButton.place(x=220,y=370)

        deleteButton = ttk.Button(self.master, text='Xóa',command=self.deleteNotification)
        deleteButton.place(x=380,y=370)
    #Row 7 lam viec :) 
    def manageRegistryGUIFunction(self,event):
        if str(self.combo.get())=='Get value':
            self.keyText = StringVar()
            self.keyEntry = ttk.Entry(self.master,textvariable=self.keyText,width=23)
            self.keyEntry.insert(0,'Key')
            self.keyEntry.place(x=5,y=240)
            if self.keyEntry1.winfo_ismapped():
                self.keyEntry1.place_forget()
                self.valueEntry.place_forget()
                self.comboData.place_forget()

        elif str(self.combo.get())=='Set value':
            self.keyText1 = StringVar()
            self.keyEntry1 = ttk.Entry(self.master,textvariable=self.keyText1,width=23)
            self.keyEntry1.place(x=5,y=240)
            self.keyEntry1.insert(0,'Key')

            self.valueText = StringVar()
            self.valueEntry = ttk.Entry(self.master,textvariable=self.valueText,width=22)
            self.valueEntry.place(x=250,y=240)
            self.valueEntry.insert(0,'Value')

            self.datatype = ["String", "Binary", "DWORD","QWORD", "Multi-String","Expandable String"]
            self.comboData = ttk.Combobox(self.master, values = self.datatype,width=22)
            self.comboData.set("Kiểu dữ liệu")
            self.comboData.place(x=490,y=240)
            if self.keyEntry.winfo_ismapped():
                self.keyEntry.place_forget()
        elif str(self.combo.get())=='Delete value':
            self.keyText = StringVar()
            self.keyEntry = ttk.Entry(self.master,textvariable=self.keyText,width=23)
            self.keyEntry.insert(0,'Key')
            self.keyEntry.place(x=5,y=240)
            if self.keyEntry1.winfo_ismapped():
                self.keyEntry1.place_forget()
                self.valueEntry.place_forget()
                self.comboData.place_forget()
        elif str(self.combo.get())=='Create key' or str(self.combo.get())=='Delete key':
            if self.keyEntry1.winfo_ismapped():
                self.keyEntry1.place_forget()
                self.valueEntry.place_forget()
                self.comboData.place_forget()
            if self.keyEntry.winfo_ismapped():
                self.keyEntry.place_forget()
    
    def sendRegFileFunction(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.IP, self.port_no))
        another_f = open (filename, "rb")
        l = another_f.read(1024)
        while (l):
            self.connection.send(l)
            l = another_f.read(1024)
        another_f.close()
    #Cac ham cai dat
    def browseFunction(self):
        try:
            global filename
            filename = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("registry file","*.reg"),("all files","*.*")))
            self.browseEntry.configure(state='normal')
            self.browsePath.set(filename)
            self.browseEntry.configure(state='disabled')

            f = open(filename,'r')
            global regText
            regText=f.read()
            self.regEntry.configure(state='normal')
            self.regFile.set(regText)
            self.regEntry.configure(state='disabled')
            f.close()
        except:
            print('None')
    def loadReg(self,res):
        self.master.wm_title("Registry editor")
        self.master.geometry(res)
        self.master.mainloop()
       
    def setNotification(self,Str):
        self.statusEntry.configure(state='normal')
        self.statusEntry.insert(0,Str)
        self.statusEntry.configure(state='disabled')
    def sendRegCommand(self):
        if str(self.combo.get())=='Get value':
            getRegStr = "GETVALUE " +self.regPathText.get()+ " "+self.keyText.get()
        elif str(self.combo.get())=='Delete value':
            getRegStr = "DELETEVALUE " +self.regPathText.get()+ " "+self.keyText.get()
        elif str(self.combo.get())=='Delete key':
            getRegStr = "DELETEKEY " +self.regPathText.get()
        elif str(self.combo.get())=='Create key':
            getRegStr = "CREATEKEY " +self.regPathText.get()
        elif str(self.combo.get())=='Set value':
            getRegStr = "SETVALUE%" +self.regPathText.get() +"%"+ self.keyText1.get() +"%"+ self.valueText.get() +"%"+ self.comboData.get()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.IP, self.port_no))
        self.connection.send(getRegStr.encode())
        self.setNotification(self.connection.recv(1024).decode())

    def deleteNotification(self):
        self.statusEntry.configure(state='normal')
        self.statusEntry.delete(0,END)
        self.statusEntry.configure(state='disabled')

