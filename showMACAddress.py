from tkinter import *
from tkinter import ttk

# -1 is nope, 0 is logout, 1 is shutdown
class MACAddressWindow:
    def __init__(self, root,macTuple):
        self.root = Toplevel(root)
        self.root.title('Show MAC Address')

        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        columns = ('Field','Value')
        self.tree = ttk.Treeview(self.mainframe, columns=columns, show='headings',height=12)
        self.tree.grid(column=0, row=0, sticky=(N,W),padx=16,pady=16)
        self.tree.column('Field', width=300, anchor='center',stretch=NO)
        self.tree.column('Value', width=300, anchor='center',stretch=NO)
        
        self.tree.heading('Field', text='Field')
        self.tree.heading('Value', text='Value')
        for value in macTuple:
            self.tree.insert('', 'end', values=value)
    def NewInstance(self):
        try:
            self.root.mainloop()
        except:
            pass