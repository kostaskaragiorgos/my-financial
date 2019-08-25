from tkinter import *
from tkinter import messagebox as msg
from tkinter import simpledialog as sd

import os 
import csv
import pandas as pd

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
        self.file_menu.add_command(label = "Plan an Emergency Fund",accelerator = 'Ctrl+P',command= self.plan)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.showplans = Menu(self.menu, tearoff = 0)
        self.showplans.add_command(label = "Show Plans",accelerator = 'Alt+P',command = self.showplan)
        self.menu.add_cascade(label = "Show",menu =  self.showplans)
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator = 'Ctrl+I',command=self.aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event:self.aboutmenu())
        self.master.bind('<Control-p>',lambda event:self.plan())
        self.master.bind('<Alt-p>',lambda event:self.showplan())
        
    def showplan(self):
        df = pd.read_csv('Emergency Fund.csv')
        msg.showinfo("EMERGENCY FUND",str(df))
        
    
    def plan(self):
        mf = sd.askfloat("Emergency Fund amount","Enter the amount of the emergency fund", 
                         parent = self.master,minvalue = 100,maxvalue = 10000)
        while mf is None:
            mf = sd.askfloat("Emergency Fund amount","Enter the amount of the emergency fund", 
                         parent = self.master,minvalue = 100,maxvalue = 10000)
            
        mongot = sd.askfloat("Amount of money You have", "Enter the amount of money you have",
                             parent = self.master,minvalue = 0, maxvalue = mf-1)
        while mongot is None:
             mongot = sd.askfloat("Amount of money You have", "Enter the amount of money you have",
                             parent = self.master,minvalue = 0, maxvalue = mf-1)
            
        savam = sd.askfloat("Amount of savings","Enter the amount of monthly savings",
                            parent = self.master,minvalue = 50, maxvalue = 100000)
        while savam is None:
            savam = sd.askfloat("Amount of savings","Enter the amount of monthly savings",
                            parent = self.master,minvalue = 50, maxvalue = 100000)
        
        dif  = mf - mongot
        mneeded = dif // savam
        msg.showinfo("MONTHS YOU NEED", "YOU NEED "+str(int(mneeded))+" month(s) to get "+str(mf)+" having "+str(mongot)+" saving "+str(savam)+" per month ")
        flagex = 0
        with open('Emergency Fund.csv','r') as t:
            reader = csv.reader(t)
            for row in reader:
                if row[0] == str(mf) and row[1] == str(mongot) and row[2] == str(savam):
                    flagex = flagex+1
            t.close()
            
        if flagex ==0:
            with open('Emergency Fund.csv', 'a+') as g:
                thewriter = csv.writer(g)
                thewriter.writerow([str(mf),str(mongot),str(savam),str(mneeded)])
                g.close()
                
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
            
    
    def aboutmenu(self):
        msg.showinfo("About" ,"About Emergency Fund \nVersion 1.0")
    
    def helpmenu(self):
        msg.showinfo("Help", "Press the button")
        
def main():
    root=Tk()
    EF = Emergency_Fund(root)
    root.mainloop()
    
if __name__=='__main__':
    main()