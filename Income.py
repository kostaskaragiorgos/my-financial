from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog

import os 
import pandas as pd
import csv
import datetime

class Income():
    def __init__(self,master):
        self.master = master
        self.master.title("Income")
        self.master.geometry("250x120")
        self.master.resizable(False,False)
       # folders 
        if os.path.exists("income") == False:
            os.mkdir("income")
            os.chdir("income")
        os.chdir("income")
        
        nowyear = datetime.date.today().year
        
        if os.path.exists(str(nowyear)) == False:
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        os.chdir(str(nowyear))
        
        #csv file
        nowmonth = datetime.date.today().month
        if os.path.exists('income'+str(nowmonth)+'.csv') == False:
            with open('income'+str(nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Amount','Description'])
                f.close()
        
        #basic gui
        self.amountl = Label(self.master,
                               text = "Enter the amount")
        self.amountl.pack()
        
        self.textamount = Text(self.master,height = 1 )
        self.textamount.pack()
        
        self.desl = Label(self.master,text = "Enter the description")
        self.desl.pack()
        
        self.textdes = Text(self.master,height = 1 )
        self.textdes.pack()
        
        self.incomeb =Button(self.master,text = "Add Income") 
        self.incomeb.pack()
        
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
        
    def exitmenu():
        pass
    
    def aboutmenu():
        pass
    def helpmenu():
        pass
    
        
def main():
    root=Tk()
    I = Income(root)
    root.mainloop()
    
if __name__=='__main__':
    main()