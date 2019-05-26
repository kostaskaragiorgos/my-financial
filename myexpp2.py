from tkinter import *
from tkinter import messagebox as msg 
from tkinter import simpledialog

import datetime
import os
import csv

class Myepxp2():
    def __init__(self,master):
        self.master = master
        self.master.title("MY EXPENSES")
        self.master.geometry("220x70")
        if os.path.exists('Expanse.csv') == False:
            with open('Expanse.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Date','Amount'])
                f.close()  
        self.master.resizable(False,False)
        if os.path.exists('Income.csv') == False:
            with open('Income.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Date','Amount'])
                f.close()    
        
        if os.path.exists('Yearly_Income.csv') == False:
            with open('Yearly_Income.csv','a+') as y:
                thewriter = csv.writer(y)
                thewriter.writerow(['Month','Amount'])
                y.close()
        
        self.master.menu = Menu(self.master,bg="lightgray",fg="black")
        
        self.file_menu= Menu(self.master.menu,tearoff = 0, bg = "lightgray",fg = "black" )
        self.file_menu.add_command(label = "Add Income",accelerator = "Alt+O",command = self.incomebf)
        self.file_menu.add_command(label = "Add Expense",accelerator = "Alt+E",command = self.expbf)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command= self.exitmenu)
        self.master.menu.add_cascade(label="File",menu = self.file_menu)
        
        self.showmenu = Menu(self.master.menu,tearoff = 0)
        self.showmenu.add_command(label = "Show Yearly Income",command = self.yearlyinc)
        self.showmenu.add_command(label = "Show Income For This Month",command = self.minc)
        self.master.menu.add_cascade(label = "Income",menu = self.showmenu)
        
        self.showmenuexp = Menu(self.master.menu , tearoff = 0)
        self.showmenuexp.add_command(label = "Show Yearly Expenses", command = self.yearlyexp)
        self.showmenuexp.add_command(label = "Show Expenses For This Month",command = self.monthexp)
        self.master.menu.add_cascade(label = "Expenses",menu = self.showmenuexp)
        
        self.helpmenu = Menu(self.master.menu,tearoff=0)
        self.helpmenu.add_command(label = "About",accelerator = 'Ctrl+I',command = self.aboutmenu)
        self.helpmenu.add_command(label="Help",accelerator = 'Ctrl+F1',command=self.helpmenuf)
        self.master.menu.add_cascade(label="Help",menu=self.helpmenu)
        
        self.master.config(menu=self.master.menu)
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event:self.helpmenuf())
        self.master.bind('<Control-i>',lambda event : self.aboutmenu())
        self.master.bind('<Alt-o>',lambda event:self.incomebf())
        self.master.bind('<Alt-e>',lambda event: self.expbf())
        
        self.incomeb = Button(self.master,text = "INCOME",command= self.incomebf)
        self.incomeb.pack()
        self.expb = Button(self.master,text = "EXPENSE",command = self.expbf)
        self.expb.pack()
    
    def yearlyexp(self):
        pass
    
    def monthexp(self):
        pass
    
    
    def yearlyinc(self):
        pass
    
    
    def minc(self):
        pass
    
    
    def aboutmenu(self):
        msg.showinfo("About","About MY EXPENSES \nVersion 1.0\n")
    
    def helpmenuf(self):
        msg.showinfo("Help", "This app helps you to measure your expenses\n"
                     +"1.Press the INCOME button to save your income value to a csv file \n"
                     +"2.Press the EXPENSE button to save you expense to a csv file \n")
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
            
            
    def incomebf(self):
        inc = simpledialog.askfloat("Income","What is your income?",parent = self.master,minvalue = 0.0,maxvalue =10000000000.00 )
        now = datetime.datetime.today().strftime('%d-%m-%Y')
        if os.path.exists('Income.csv') == True:
            with open('Income.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([now,inc])
                f.close()  
                
    def expbf(self):
        exp = simpledialog.askfloat("Expanse","What is your expanse?",parent = self.master,minvalue = 0.0,maxvalue =10000000000.00)
        now = datetime.datetime.today().strftime('%d-%m-%Y')
        if os.path.exists('Expanse.csv') == True:
            with open('Expanse.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([now,exp])
                f.close()
def main():
    root=Tk()
    myexp = Myepxp2(root)
    root.mainloop()
    
if __name__=='__main__':
    main()
