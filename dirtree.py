from io import TextIOWrapper
import os
import sys
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import socket
import json

class FileTree():
    def __init__(self, parent, conn:socket.socket):
        self.parent = parent
        self.conn = conn
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


    #THIS IS NOT TO BE USED IN THE CLIENT. THIS IS ONLY A TESTING METHOD.
    #This is to be used in the server.
    def list_files(self, output=sys.stdout):
        for root, dirs, files in os.walk(self.root):
            level = root.replace(self.root, '').count(os.sep)
            indent = '\t' * (level)
            print('{}{}/'.format(indent, os.path.basename(root)), file=output)
            subindent = '\t' * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f), file=output)

    def bind2Tree(self, data:str):
        data = json.loads(data)
        assert type(data) == dict
        partitions = list(data.keys())
        for p in partitions:
            self.fileTree.insert("", "end", p, text=p)
            levels = []
            paths = data[p]
            for path in paths:
                if path[-1] == "\n":
                    path = path[:-1]
                if path == "/":
                    continue
                level = path.count("\t")
                while path[0] == "\t":
                    path = path[1:]
                #if path[-1] != "/":
                #    level -= 1
                if len(levels) == 0:
                    if path[-1] == "/":
                        levels.append({"dir": path, "level": level})
                    self.fileTree.insert(p, "end", path, text=path, values=(path, ))
                elif level == 0:
                    while len(levels) > 0:
                        levels.pop()
                    levels.append({"dir": path, "level": level})
                    self.fileTree.insert(p, "end", path, text=path, values=(path, ))
                elif level <= levels[-1]["level"]:
                    while level <= levels[-1]["level"]:
                        levels.pop()
                    self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
                            text=path, values=(levels[-1]["dir"] + path, ))
                    if path[-1] == "/":
                        levels.append({"dir": levels[-1]["dir"] + path, "level": level})
                else:
                    self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
                            text=path, values=(levels[-1]["dir"] + path, ))
                    if path[-1] == "/":
                        levels.append({"dir": levels[-1]["dir"] + path, "level": level})

    def test(self):
        self.fileTree.insert("", "end", "123", text="1234", values=(123, ))
        self.fileTree.insert("", "end", "1234", text="123", values=(1234, ))


    def onDBLClick(self, event):
        self.item = self.fileTree.focus()
        if (self.item):
            self.copyButton['state'] = NORMAL
            self.deleteButton['state'] = NORMAL
    def Copy(self):
        dir = filedialog.askdirectory()
        name = self.fileTree.item(self.item, 'text')
        serverPath = self.fileTree.item(self.item, 'values')[0]
        with open(os.path.join(dir, name), "wb") as ofile:
            self.conn.send("GIVE " + serverPath)
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                ofile.write(data)

    def Delete(self):
        messagebox.askyesno(message="Are you sure you want to delete this item?",\
            icon='question', title="Delete")
        serverPath = self.fileTree.item(self.item, 'values')[0]
        self.conn.send("BANISH " + serverPath)
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
        self.conn.send("DIRSHW")
        data = ""
        while True:
            dd = self.conn.recv(1024).decode(encoding="utf8")
            if not dd:
                break
            data += dd
        return data

    def startInstance(self):
        data = self.sendSignal()
        self.bind2Tree(data)
        self.ui.mainloop()

# ft = FileTree(None, None)
# filepath =  "E:\\list.txt"
# with open(filepath, "w", encoding="utf8") as ofile:
#     ft.list_files(ofile)

# ft.bind2Tree(filepath)
# ft.test()
# ft.ui.mainloop()
