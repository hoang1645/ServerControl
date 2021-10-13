from io import TextIOWrapper
import os
import sys
from tkinter import ttk
from tkinter import *
import socket


def list_files(startpath, output=sys.stdout):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)), file=output)
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f), file=output)

class FileTree():
    def __init__(self, root:str, parent):
        self.root = root
        self.parent = parent
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

        self.fileTree = ttk.Treeview(self.mainframe, padding="3 3 12 12")
        self.fileTree.grid(column=1, row=1, sticky=(N, W, E, S))
        self.scroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, \
            command=self.fileTree.yview)

        self.mainframe.columnconfigure(1, weight=5)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        
        self.fileTree.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(column=2, row=1, sticky=(N, W, E, S))
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    #THIS IS NOT TO BE USED IN THE CLIENT. THIS IS ONLY A TESTING METHOD.
    def list_files(self, output=sys.stdout):
        for root, dirs, files in os.walk(self.root):
            level = root.replace(self.root, '').count(os.sep)
            indent = '\t' * (level)
            print('{}{}/'.format(indent, os.path.basename(root)), file=output)
            subindent = '\t' * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f), file=output)

    def bind2Tree(self, filepath):
        with open(filepath, "r", encoding="utf8") as file:
            paths = file.readlines()
            levels = []
            for path in paths:
                if path[-1] == "\n":
                    path = path[:-1]
                #if path == "/":
                #    continue
                level = path.count("\t")
                while path[0] == "\t":
                    path = path[1:]
                #if path[-1] != "/":
                #    level -= 1
                if len(levels) == 0:
                    if path[-1] == "/":
                        levels.append({"dir": path, "level": level})
                    self.fileTree.insert("", "end", path, text=path)
                elif level == 0:
                    while len(levels) > 0:
                        levels.pop()
                    levels.append({"dir": path, "level": level})
                    self.fileTree.insert("", "end", path, text=path)
                elif level <= levels[-1]["level"]:
                    while level <= levels[-1]["level"]:
                        levels.pop()
                    self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
                         text=path)
                    if path[-1] == "/":
                        levels.append({"dir": levels[-1]["dir"] + path, "level": level})
                else:
                    self.fileTree.insert(levels[-1]["dir"], "end", levels[-1]["dir"] + path,\
                         text=path)
                    if path[-1] == "/":
                        levels.append({"dir": levels[-1]["dir"] + path, "level": level})
                    
                        

                    
                        

    def sendSignal(self, conn:socket.socket):
        conn.send("DIRSHW")
        data = ""
        while True:
            data += conn.recv(1024).decode(encoding="utf8")
            if not data:
                break

ft = FileTree("E:\\", None)
filepath =  "E:\list.txt"
with open(filepath, "w", encoding="utf8") as ofile:
    ft.list_files(ofile)

ft.bind2Tree(filepath)
ft.ui.mainloop()
