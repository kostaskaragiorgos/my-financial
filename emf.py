""" creates an Emergency fund plan """
from tkinter import Tk, Menu, Button
from tkinter import messagebox as msg
from tkinter import simpledialog as sd
import os
import csv
import pandas as pd
def showplan():
    """ shows the emergency fund plans """
    df = pd.read_csv('Emergency Fund.csv')
    df = df.drop_duplicates(keep='first')
    msg.showinfo("EMERGENCY FUND", str(df))
def saveplan(mf, mongot, savam, mneeded):
    """ saves a plan to a csv file"""
    with open('Emergency Fund.csv', 'a+') as g:
        thewriter = csv.writer(g)
        thewriter.writerow([str(mf), str(mongot), str(savam), str(mneeded)])
def aboutmenu():
    """ about function """
    msg.showinfo("About", "About Emergency Fund \nVersion 1.0")
def helpmenu():
    """ help menu function """
    msg.showinfo("Help", "Press the button")
class Emergency_Fund():
    """ Emergency Fund class """
    def __init__(self, master):
        self.master = master
        self.master.title("Emergency Fund")
        self.master.geometry("250x120")
        self.master.resizable(False, False)
        if not os.path.exists('Emergency Fund.csv'):
            with open('Emergency Fund.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['EMERGENCY FUND', 'MONEY YOU HAVE', 'MONTHLY SAVINGS', 'MONTHS NEEDED'])
        self.planb = Button(self.master, text="Plan an emergency fund", command=self.plan)
        self.planb.pack()
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Plan an Emergency Fund", accelerator='Ctrl+P', command=self.plan)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.showplans = Menu(self.menu, tearoff=0)
        self.showplans.add_command(label="Show Plans", accelerator='Alt+P', command=showplan)
        self.menu.add_cascade(label="Show", menu=self.showplans)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Control-p>', lambda event: self.plan())
        self.master.bind('<Alt-p>', lambda event: showplan())
    def plan(self):
        """ creates an emergency fund plan """
        mf = sd.askfloat("Emergency Fund amount", "Enter the amount of the emergency fund", 
                         parent=self.master, minvalue=100, maxvalue=10000)
        while mf is None:
            mf = sd.askfloat("Emergency Fund amount", "Enter the amount of the emergency fund", 
                             parent=self.master, minvalue=100, maxvalue=10000)
            
        mongot = sd.askfloat("Amount of money You have", "Enter the amount of money you have",
                             parent=self.master, minvalue=0, maxvalue=mf-1)
        while mongot is None:
            mongot = sd.askfloat("Amount of money You have", "Enter the amount of money you have",
                                 parent=self.master, minvalue=0, maxvalue=mf-1)
        savam = sd.askfloat("Amount of savings", "Enter the amount of monthly savings",
                            parent=self.master, minvalue=50, maxvalue=100000)
        while savam is None:
            savam = sd.askfloat("Amount of savings", "Enter the amount of monthly savings",
                                parent=self.master, minvalue=50, maxvalue=100000)
        dif = mf - mongot
        mneeded = dif // savam
        msg.showinfo("MONTHS YOU NEED", "YOU NEED "+str(int(mneeded))+" month(s) to get "+str(mf)+" having "+str(mongot)+" saving "+str(savam)+" per month ")
        saveplan(mf, mongot, savam, mneeded)
    def exitmenu(self):
        """ exit menu function"""
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
def main():
    """ main function """
    root = Tk()
    Emergency_Fund(root)
    root.mainloop()
if __name__ == '__main__':
    main()
