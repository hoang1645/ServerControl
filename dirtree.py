import os
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import socket
import json
from time import sleep

class FileTree():
    def __init__(self, parent, ip='127.0.0.1', port=1025):
        self.parent = parent
        assert ip
        assert port
        self.ip = ip
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        if parent:
            self.ui = Toplevel(parent)
        else:
            self.ui = Tk()
        self.ui.title('Files')
        # self.ui.geometry("700x360")
        self.mainframe = ttk.Frame(self.ui, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.ui.columnconfigure(0, weight=1)
        self.ui.rowconfigure(0, weight=1)
        self.ui.rowconfigure(1, weight=1)

        self.fileTree = ttk.Treeview(self.mainframe, padding="3 3 12 12")
        self.fileTree.grid(column=1, row=1, sticky=(N, W, E, S))
        self.scroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, \
            command=self.fileTree.yview)

        self.mainframe.columnconfigure(1, weight=5)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.fileTree.bind("<Double-1>", self.onDBLClick)
        self.fileTree.bind("<1>", self.onSingle)

        self.buttonFrame = ttk.Frame(self.ui, padding='10 10 25 25')
        self.buttonFrame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.copyButton = ttk.Button(self.buttonFrame, text='Copy', command=self.Copy, state=DISABLED)
        self.copyButton.grid(column=1, row=1, sticky=(N, W, E, S))
        self.deleteButton = ttk.Button(self.buttonFrame, text='Delete', command=self.Delete,\
            state=DISABLED)
        self.deleteButton.grid(column=2, row=1, sticky=(N, W, E, S))
        self.buttonFrame.columnconfigure(1, weight=1)
        self.buttonFrame.columnconfigure(2, weight=1)
        self.buttonFrame.rowconfigure(1, weight=1)
        
        self.fileTree.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(column=2, row=1, sticky=(N, W, E, S))
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def bind2Tree(self):
        partitions = json.loads(self.data)
        print(partitions)
        assert type(partitions) == list
        for p in partitions:
            self.fileTree.insert("", "end", p, text=p, values = (p, "dir"))
            # levels = []
            # paths = data[p]
            # for path in paths:
            #     if path[-1] == "\n":
            #         path = path[:-1]
            #     if path == "/":
            #         continue
            #     level = path.count("\t")
            #     while path[0] == "\t":
            #         path = path[1:]
            #     #if path[-1] != "/":
            #     #    level -= 1
            #     if len(levels) == 0:
            #         if path[-1] == "/":
            #             levels.append({"dir": path, "level": level})
            #         self.fileTree.insert(p, "end", path, text=path, values=(path, ))
            #     elif level == 0:
            #         while len(levels) > 0:
            #             levels.pop()
            #         levels.append({"dir": path, "level": level})
            #         self.fileTree.insert(p, "end", path, text=path, values=(path, ))
            #     elif level <= levels[-1]["level"]:
            #         while level <= levels[-1]["level"]:
            #             levels.pop()
            #         self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
            #                 text=path, values=(levels[-1]["dir"] + path, ))
            #         if path[-1] == "/":
            #             levels.append({"dir": levels[-1]["dir"] + path, "level": level})
            #     else:
            #         self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
            #                 text=path, values=(levels[-1]["dir"] + path, ))
            #         if path[-1] == "/":
            #             levels.append({"dir": levels[-1]["dir"] + path, "level": level})

    def test(self):
        self.fileTree.insert("", "end", "123", text="1234", values=(123, ))
        self.fileTree.insert("", "end", "1234", text="123", values=(1234, ))


    def onSingle(self, event):
        self.item = self.fileTree.focus()
        if (self.item):
            if self.fileTree.item(self.item, 'values')[1] == "file":
                print("file")
                self.copyButton['state'] = NORMAL
            else:
                self.copyButton['state'] = DISABLED
            self.deleteButton['state'] = NORMAL
    def onDBLClick(self, event):
        self.item = self.fileTree.focus()
        
        if (self.item):
            serverPath = self.fileTree.item(self.item, 'values')[0]
            type = self.fileTree.item(self.item, 'values')[1]
            if type == "file":
                return
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.ip, self.port))
            self.conn.send(("GET " + serverPath).encode(encoding='utf8'))
            print("Command sent")
            data = b""
            while True:
                d = self.conn.recv(1024)
                data += d
                if (len(d)) < 1024:
                    break
            List = json.loads(data)
            for item, type in List:
                fullPath = os.path.join(serverPath, item)
                try:
                    self.fileTree.insert(serverPath, "end", fullPath, text="<" + type + "> " + item, values=(fullPath, type))
                except TclError:
                    pass
    def manipulateNameFromDirOrFile(self,s):
        if '<file> ' in s:
            return s[7:]
        elif '<dir> ' in s:
            return s[6:]
        else:
            return s
    def Copy(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port))

        self.item = self.fileTree.focus()
        dir = filedialog.askdirectory()
        name = self.fileTree.item(self.item, 'text').replace("<file> ", "")
        serverPath = self.fileTree.item(self.item, 'values')[0]
        a = True
        if os.path.isfile(os.path.join(dir, name)):
            a = messagebox.askyesno(message="Item already exists. Overwrite?",\
            icon='question', title="Copy")
        if a:
            self.conn.send(("GIVE " + serverPath).encode(encoding='utf8'))
            data = b""
            print(len(data))
            while True:
                    d = self.conn.recv(1024)
                    data += d
                    if len(d) < 1024:                    
                        break
            with open(os.path.join(dir, name), "wb") as ofile:
                ofile.write(data)
            
    def Delete(self):
        self.item = self.fileTree.focus()
        a = messagebox.askyesno(message="Are you sure you want to delete this item?",\
            icon='question', title="Delete")
        if not a:
            return
        serverPath = self.fileTree.item(self.item, 'values')[0]
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port))
        self.conn.send(("BANISH " + serverPath).encode(encoding='utf8'))
        response = self.conn.recv(1024).decode()
        if response == 'OK':
            self.fileTree.delete(self.item)
        else:
            messagebox.showerror(message=response)
            if response=='File already deleted':
                self.fileTree.delete(self.item)

    def sendSignal(self):
        self.conn.send("DIRSHW".encode())
        self.data = self.conn.recv(1024).decode()

    def startInstance(self):
        try:
            self.sendSignal()
            self.bind2Tree()
            self.ui.mainloop()
        except:
            pass
    @staticmethod
    def list_files(partition):
        ret = []
        for root, dirs, files in os.walk(partition):
            level = root.replace(partition, '').count(os.sep)
            indent = '\t' * (level)
            ret.append('{}{}/'.format(indent, os.path.basename(root)))
            subindent = '\t' * (level + 1)
            for f in files:
                ret.append('{}{}'.format(subindent, f))
        return ret

#ft = FileTree(None, '10.2.0.2', 1025)
# filepath =  "E:\\list.txt"
# with open(filepath, "w", encoding="utf8") as ofile:
#     ft.list_files(ofile)
#ft.startInstance()