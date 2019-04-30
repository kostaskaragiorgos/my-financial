from tkinter import *
#import os
from tkinter import messagebox as msg 
#import csv
from tkinter import simpledialog
class Myepxp2():
    def __init__(self,master):
        self.master = master
        self.master.title("MY EXPENSES")
        self.master.geometry("200x70")
        self.master.resizable(False,False)
        
        self.master.menu = Menu(self.master,bg="lightgray",fg="black")
        self.file_menu= Menu(self.master.menu,tearoff = 0, bg = "lightgray",fg = "black" )
        self.file_menu.add_command(label="Exit",command= self.exitmenu)
        self.master.menu.add_cascade(label="File",menu = self.file_menu)
        self.helpmenu = Menu(self.master.menu,tearoff=0)
        self.helpmenu.add_command(label="Help",command=self.helpmenu)
        self.master.menu.add_cascade(label="Help",menu=self.helpmenu)
        self.master.config(menu=self.master.menu)
        
        self.incomeb = Button(self.master,text = "INCOME",command= self.incomebf)
        self.incomeb.pack()
        self.expb = Button(self.master,text = "EXPENSE",command = self.expbf)
        self.expb.pack()
        
    def helpmenu(self):
        pass
    def exitmenu(self):
        pass
    def incomebf(self):
        inc = simpledialog.askfloat("Income","What is your income?",parent = self.master,minvalue = 0.0,maxvalue =10000000000.00 )
    def expbf(self):
        exp = simpledialog.askfloat("Expanse","What is your expanse?",parent = self.master,minvalue = 0.0,maxvalue =10000000000.00)

def main():
    root=Tk()
    myexp = Myepxp2(root)
    root.mainloop()
    
if __name__=='__main__':
    main()