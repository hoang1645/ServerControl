import time
from tkinter import *
from tkinter import messagebox

class TimerWindow(Frame):
    def __init__(self,rawSeconds, master=None):
        Frame.__init__(self, master)
        self.rawSeconds = rawSeconds
        self.master = Toplevel(master)
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=1)
        self.master.columnconfigure(2,weight=1)

        self.hour=StringVar()
        self.minute=StringVar()
        self.second=StringVar()

        self.hour.set('0')
        self.minute.set('0')
        self.second.set('0')

        timerLabel = Label(self.master,text='Countdown Timer')
        timerLabel.grid(row=0,column=0,sticky='w',padx=10,pady=10)

        hourEntry= Entry(self.master, width=10, font=("",18,""), textvariable=self.hour,justify='center')
        hourEntry.grid(row=1,column=0,sticky='w',padx=10,pady=10)
  
        minuteEntry= Entry(self.master, width=10, font=("",18,""),textvariable=self.minute,justify='center')
        minuteEntry.grid(row=1,column=1)
  
        secondEntry= Entry(self.master, width=10, font=("",18,""),textvariable=self.second,justify='center')
        secondEntry.grid(row=1,column=2,sticky='e',padx=10,pady=10)

    def load(self):
        self.master.wm_title("Countdown Timer")
        self.master.geometry("100x100")
        self.master.mainloop()
    
    def submit(self):
        temp = self.rawSeconds
        while temp > -1:
            mins, secs = divmod(temp,60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))
            self.master.update()
            time.sleep(1)
            if temp == 0:
                messagebox.showinfo("Time Countdown", "Time's up!")
                self.master.destroy()
            temp -= 1