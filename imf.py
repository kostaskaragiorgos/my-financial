from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import simpledialog as sd

import os 
import csv
import datetime

class Emergency_Fund():
    def __init__(self,master):
        self.master = master
        self.master.title("Emergency Fund")
        self.master.geometry("250x120")
        self.master.resizable(False,False)
        
        if os.path.exists('Emergency Fund.csv') == False:
            with open('Emergency Fund.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['EMERGENCY FUND','MONEY YOU HAVE','MONTHLY SAVINGS','MONTHS NEEDED'])
                f.close()
        
        self.planb = Button(self.master,text = "Plan an emergency fund",command = self.plan)
        self.planb.pack()
        
        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator = 'Ctrl+I',command=self.aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        
    
    def plan(self):
        mf = sd.askfloat("Emergency Fund amount","Enter the amount of the emergency fund", 
                         parent = self.master,minvalue = 100,maxvalue = 10000)
        mongot = sd.askfloat("Amount of money You have", "Enter the amount of money you have",
                             parent = self.master,minvalue = 0, maxvalue = mf-1)
        savam = sd.askfloat("Amount of savings","Enter the amount of monthly savings",
                            parent = self.master,minvalue = 50, maxvalue = 100000)
        
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
            
    
    def aboutmenu(self):
        pass
    
    def helpmenu(self):
        pass    
        
def main():
    root=Tk()
    EF = Emergency_Fund(root)
    root.mainloop()
    
if __name__=='__main__':
    main()