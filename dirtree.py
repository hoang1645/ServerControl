from io import TextIOWrapper
import os
import sys
import threading
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import socket
import json

class FileTree():
    def __init__(self, parent, ip='127.0.0.1', port=1025):
        self.parent = parent
        assert ip
        assert port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        if parent:
            self.ui = Toplevel(parent)
        else:
            self.ui = Tk()
        self.ui.title('Files')
        self.ui.geometry("640x360")
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

    def bind2Tree(self, data:str):
        partitions = json.loads(data)
        assert type(partitions) == list
        for p in partitions:
            self.fileTree.insert("", "end", p, text=p)
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
            self.copyButton['state'] = NORMAL
            self.deleteButton['state'] = NORMAL
    def onDBLClick(self, event):
        self.item = self.fileTree.focus()
        serverPath = self.fileTree.item(self.item, 'values')[0]
        self.conn.send(("GET " + serverPath).encode())
        data = b""
        while True:
            d = self.conn.recv(1024)
            if not d:
                break
            data += d
        List = json.loads(data)
        for item in List:
            fullPath = os.path.join(serverPath, item)
            self.fileTree.insert(serverPath, "end", fullPath, text=item, values=(fullPath, ))
        pass
    def Copy(self):
        dir = filedialog.askdirectory()
        name = self.fileTree.item(self.item, 'text')
        serverPath = self.fileTree.item(self.item, 'values')[0]
        with open(os.path.join(dir, name), "wb") as ofile:
            self.conn.send(("GIVE " + serverPath).encode())
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                ofile.write(data)

    def Delete(self):
        messagebox.askyesno(message="Are you sure you want to delete this item?",\
            icon='question', title="Delete")
        serverPath = self.fileTree.item(self.item, 'values')[0]
        self.conn.send(("BANISH " + serverPath).encode())
        data = ""
        while True:
            dd = self.conn.recv(1024).decode(encoding="utf8")
            if not dd:
                break
            data += dd
        olds = self.fileTree.get_children()
        for old in olds:
            self.fileTree.delete(old)
        self.bind2Tree(data)

    def sendSignal(self):
        self.conn.send("DIRSHW".encode())
        self.data = ""
        while True:
            dd = self.conn.recv(1024).decode(encoding="utf8")
            if not dd:
                break
            self.data += dd
    
    def waitForLoad(self):
        self.wait = Tk()
        mframe = ttk.Frame(self.wait)
        mframe.grid(column=0, row=0)
        self.wait.geometry('300x200')
        self.wait.resizable(FALSE,FALSE)
        ttk.Label(mframe, text="Loading").grid(column=1, row=1)
        self.wait.columnconfigure(0, weight=1)
        self.wait.rowconfigure(0, weight=1)
        self.wait.mainloop()


    def startInstance(self):
        self.sendSignal()
        self.bind2Tree(self.data)
        
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

#ft = FileTree(None, '10.19.0.8', 1025)
# filepath =  "E:\\list.txt"
# with open(filepath, "w", encoding="utf8") as ofile:
#     ft.list_files(ofile)

# ft.bind2Tree(filepath)
# ft.test()
# ft.ui.mainloop()
#paths = [FileTree.list_files(path) for path in ["C:\\", "D:\\", "E:\\", "F:\\"]]
#print(paths)
#print(FileTree.list_files("C:\\"))