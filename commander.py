from tkinter import *
from tkinter import ttk
import enum
class StateOut(enum.Enum):
    Nope = int(-1)
    LogOut = int(0)
    ShutDown = int(1)
    ShutDownWithTime = int(2)
# -1 is nope, 0 is logout, 1 is shutdown
class ShutdownCMD:
    def __init__(self, root):
        self.command = 'SHUTDOWN'
        self.isExcuted = StateOut.Nope.value
        self.parent = root
        
        self.root = Toplevel(root)
        self.root.title('Shut down')

        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        self.delay = IntVar(value=StateOut.Nope)
        self.delay_time = StringVar()

        self.immediate_check = ttk.Radiobutton(self.mainframe, text="Shut down immediately", 
                                    variable=self.delay, value=StateOut.ShutDown.value)
        self.delayed_check   = ttk.Radiobutton(self.mainframe, text="Shut down after (seconds):", 
                                    variable=self.delay, value=StateOut.ShutDownWithTime.value)
        self.signout_check = ttk.Radiobutton(self.mainframe, text="Log out", 
                                    variable=self.delay, value=StateOut.LogOut.value)

        self.immediate_check.grid(column=1, row=1,sticky='w')
        self.delayed_check.grid(column=2, row=1,sticky='w',padx=5)

        self.delay_time_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.delay_time)
        self.delay_time_entry.grid(column=3, row=1)

        self.signout_check.grid(column=1,row=2,sticky='w')

        self.subframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.subframe.grid(column=0, row=2)

        self.button = ttk.Button(self.subframe, text='OK', command=lambda:[self.confirm(),root.destroy()])
        self.button.grid(column=2, row=3)
    def confirm(self):
        self.isExcuted = self.delay.get()
    def NewInstance(self):
        self.root.mainloop()