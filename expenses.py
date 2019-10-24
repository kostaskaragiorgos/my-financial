from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import os 
import csv
import datetime

class Expenses():
    def __init__(self,master):
        self.master = master
        self.master.title("Expenses")
        self.master.geometry("250x120")
        self.master.resizable(False,False)
       # folders 
        if os.path.exists("expenses") == False:
            os.mkdir("expenses")
            os.chdir("expenses")
        else:
            os.chdir("expenses")
        
        nowyear = datetime.date.today().year
        
        if os.path.exists(str(nowyear)) == False:
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        else:
            os.chdir(str(nowyear))
        
        #csv file
        self.nowmonth = datetime.date.today().month
        if os.path.exists('expenses'+str(self.nowmonth)+'.csv') == False:
            with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Day','Amount','Description','Category'])
                f.close()
                
        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.show = Menu(self.menu,tearoff = 0)
        self.show.add_command(label = 'Show Monthly Expenses',accelerator = 'Alt+S',command = self.monexp)
        self.menu.add_cascade(label = "Show",menu = self.show )
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator= 'Ctrl+I',command=self.aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event:self.aboutmenu())
        self.master.bind('<Alt-s>',lambda event: self.monexp())
        
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
        
        category_list = list(["Bills/Taxes","Grocery","Transportation","Other"])
        self.var_cat_list = StringVar(master)
        self.var_cat_list.set(category_list[0])
        self.popupcatlistmenu = OptionMenu(self.master,self.var_cat_list,*category_list)
        self.popupcatlistmenu.pack()
        
        self.incomeb =Button(self.master,text = "Add Expense",command = self.addexp) 
        self.incomeb.pack()
    
    def monexp(self):
        sum = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as r:
            reader = csv.reader(r)
            next(reader)
            for row in reader:
                sum += int(row[1])
            r.close()
        msg.showinfo("Montly Expenses","YOUR EXPENSES FOR THE "+str(self.nowmonth)+" MONTH IS "+str(sum))
        
    def addexp(self):
        valam = 0
        valdes = 0
        try:
            if float(self.textamount.get(1.0,END)) > 0:
                valam = 1
            else:
                msg.showerror("Value Error", "Enter a number higher than zero")
                self.textamount.delete(0,END)
        except:
            msg.showerror("Value Error", "Enter a number higher than zero")
            self.textamount.delete(1.0,END)
        if self.textdes.count(1.0,END) == (1,):
            msg.showerror("Description Error", "Enter a description")
        else:
            valdes = 1
        if valam == 1 and valdes == 1:
            msg.showinfo("Expanse","Day:"+str(datetime.date.today().day) +"\nAmount:"+str(self.textamount.get(1.0,END)) +"\nDescription:" + self.textdes.get(1.0,END) + "\nCategory:"+str(self.var_cat_list.get()))
            with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([str(datetime.date.today().day),str(self.textamount.get(1.0,END)),self.textdes.get(1.0,END),str(self.var_cat_list.get())])
                f.close()
            
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    
    def helpmenu(self):
        pass
    
    def aboutmenu(self):
        msg.showinfo("About","Expenses\nVersion 1.0")

        
def main():
    root=Tk()
    E = Expenses(root)
    root.mainloop()
    
if __name__=='__main__':
    main()