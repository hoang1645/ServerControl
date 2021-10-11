from tkinter import ttk
from tkinter import *
import threading
import socket
import os
import pyautogui
import registry
from winreg import *
from time import sleep
import subprocess
import keyboard #pip install keyboard

mp={
    'HKEY_CLASSES_ROOT':HKEY_CLASSES_ROOT,
    'HKEY_CURRENT_CONFIG':HKEY_CURRENT_CONFIG,
    'HKEY_CURRENT_USER':HKEY_CURRENT_USER,
    'HKEY_USERS':HKEY_USERS,
    'HKEY_LOCAL_MACHINE':HKEY_LOCAL_MACHINE
}
class Server(object):
    def main_form(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Server")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="25 25 50 50")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        #Open server button
        self.connectButton = ttk.Button(self.mainframe, text='Open', command=self.threadConnect)
        self.connectButton.grid(column=1, row=1)
        self.root.mainloop()
        pass
    def threadConnect(self):
        con=threading.Thread(target=self.Connect)
        con.start()
    def Connect(self):
        port = 1025
        #addr = '14.230.23.93'
        addr = socket.gethostbyname(socket.gethostname())
        Label(self.mainframe,text=addr+':'+str(port)).grid(column=1,row=2)
        print(addr, port)
        self.connectButton['text'] = 'Close'
        self.connectButton['command'] = self.Close
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((addr, port))
        s.listen()
        while True:
            self.conn, self.target_addr = s.accept()
            data=self.conn.recv(1024)
            print(data)
            if not data:
                break
            self.magicFunction(data)
    #Ham nay nhan lenh tu client
    def magicFunction(self,Str):
        if Str.decode()=='Hello':
            print('Hello')
        elif Str.decode().find('SHUTDOWN')!=-1:
            #Commands the server to shut down
            try:
                a = Str.decode().split()
                cmd = Str.decode()
                if len(a) == 2:
                    cmd='shutdown -s -t ' + a[1]
                else:
                    cmd='shutdown -s'
                os.system(cmd)
            except Exception as e:
                self.conn.send("Invalid command: " + str(e))
        elif Str.decode() == 'CAPSCR':
            pyautogui.screenshot().save('scr.png')
            send = open('scr.png','rb')
            while True:
                data=send.read(1024)
                if not data:
                    break
                self.conn.sendall(data)
        
        elif Str.decode() == 'SHWPRC':
            #Commands the server to send the file consisting of running processes
            os.system("wmic process get Name, ProcessId, ThreadCount >list.txt")
            send = open('list.txt', 'r')
            while True:
                data = send.readline()
                print(data)
                if not data:
                    self.conn.send('STOPRIGHTNOW'.encode())
                    break
                self.conn.sendall(data.strip().encode())
        elif Str.decode() == 'SHWPRCAPP':
            tmp = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}")
            arr = tmp.split()[6:]
            print(arr)
            for i in range(0,len(arr)//3,1):
                plusStr=str(arr[3*i].decode()+' '+arr[3*i+1].decode()+' '+arr[3*i+2].decode()+' ')
                self.conn.send(plusStr.encode())
            self.conn.send('STOPRIGHTNOW'.encode())
        elif Str.decode().find('GETVALUE')!=-1:
            arr = Str.decode().split(' ')
            brr = arr[1].split('\\',1)
            self.conn.send(str(registry.getValue(mp[brr[0]],brr[1],arr[2])).encode())
        elif Str.decode().find('DELETEVALUE')!=-1:
            arr = Str.decode().split(' ')
            brr = arr[1].split('\\',1)
            if registry.deleteValue(mp[brr[0]],brr[1],arr[2]):
                self.conn.send('Completed'.encode())
            else:
                self.conn.send('Failure'.encode())
        elif Str.decode().find('CREATEKEY')!=-1:
            arr = Str.decode().split(' ')
            if registry.createKey(arr[1])==True:
                self.conn.send('Completed'.encode())
            else:
                self.conn.send('Failure'.encode())
        elif Str.decode().find('DELETEKEY')!=-1:
            arr = Str.decode().split(' ')
            if registry.deleteKey(arr[1])==True:
                self.conn.send('Completed'.encode())
            else:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('SETVALUE')!=-1:
            arr = Str.decode().split('%')
            brr = arr[1].split('\\',1)
            try:
                if registry.setValue(mp[brr[0]],brr[1],arr[2],arr[3],arr[4]) == True:
                    self.conn.send('Completed'.encode())
                else:
                    self.conn.send('Failed'.encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('KILLAPP') != -1:
            name = str(Str.decode().split()[1])
            try:
                subprocess.check_output('powershell Stop-Process -ID '+ name +' -Force')            
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode().find('KILL') != -1:
            PID = int(Str.decode().split()[1])
            try:
                os.kill(PID, 9)
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode().find('START') != -1:
            try:
                os.system(Str.decode())
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode() == 'KEYLOG':
            bep = threading.Thread(target=self.startKeylogging)
            bep.start()
        elif Str.decode() == 'KEYSTOP':
            self.stopKeylogging()
        else:
            f_bin=open('testing.reg','wb+')
            f_bin.write(Str)
            f_bin.close()
            if len(Str)<1024:
                registry.importRegistry(filepath=r'E:\Python\Socket_Midterm\testing.reg')
                

    #ATTRIBUTES AND METHODS SPECIFICALLY FOR KEYLOGGING:
    __interval = 5
    __log = ''
    __noch = 0
    def __callback(self, event):
        name = event.name
        if len(name) > 1:
                if name == 'space':
                    name = ' '
                elif name == 'enter':
                    name = '[ENTER]\n'
                elif name == 'decimal':
                    name = '.'
                else:
                    name = name.replace(" ", "_")
                    name = f"[{name.upper()}]"
        self.__log += name
    def __report(self):
        if self.__log:
            self.conn.send(self.__log[self.__noch:].encode())
            self.__noch = len(self.__log)
        timer = threading.Timer(interval=self.__interval, function=self.__report)
        timer.daemon = True
        timer.start()
    def startKeylogging(self):
        keyboard.on_release(self.__callback)
        self.__report()
        keyboard.wait()
    #TODO: Unhook
    def stopKeylogging(self):
        keyboard.unhook(self.__callback)
    ##################################################################################
    def Close(self):
        s.close()
        close_it=threading.Thread(target=self.root.destroy,daemon=True)
        close_it.start()
ins=Server()
mainz=threading.Thread(target=ins.main_form)
try:
    mainz.start()
except:
    ins.Connect()
    pass
