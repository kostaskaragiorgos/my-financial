from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os 
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
        else:
            os.chdir("income")
        
        nowyear = datetime.date.today().year
        
        if os.path.exists(str(nowyear)) == False:
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        else:
            os.chdir(str(nowyear))
        
        #csv file
        self.nowmonth = datetime.date.today().month
        if os.path.exists('income'+str(self.nowmonth)+'.csv') == False:
            with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Amount','Description','Category'])
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
        
        category_list = list(["Salary","Other"])
        self.var_cat_list = StringVar(master)
        self.var_cat_list.set(category_list[0])
        self.popupcatlistmenu = OptionMenu(self.master,self.var_cat_list,*category_list)
        self.popupcatlistmenu.pack()
        
        self.incomeb =Button(self.master,text = "Add Income",command = self.addinc) 
        self.incomeb.pack()

        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label = "Add Income",accelerator = 'Ctrl+O',command = self.addinc)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.showinc = Menu(self.menu,tearoff = 0)
        self.showinc.add_command(label = "Monthly Salary",accelerator = 'Alt+S',command = self.monsal)
        self.showinc.add_command(label = "Monthly Other",accelerator = 'Alt+O',command = self.monoth)
        self.showinc.add_command(label = "Monthly Income",accelerator = 'Alt+M',command = self.moninc)
        self.showinc.add_command(label = "Yearly income",accelerator = 'Alt+Y',command = self.yinc)
        self.menu.add_cascade(label = "Total Income",menu = self.showinc)
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator = 'Ctrl+I',command=self.aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        
        self.master.bind('<Alt-o>',lambda event:self.monoth())
        self.master.bind('<Alt-s>',lambda event:self.monsal())
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event:self.aboutmenu())
        self.master.bind('<Alt-m>',lambda event:self.moninc())
        self.master.bind('<Control-o>',lambda event:self.addinc())
        self.master.bind('<Alt-y>',lambda event:self.yinc())
        
        
    
    def monsal(self):
        sum_mon_salary = 0
        with open('income'+str(self.nowmonth)+'.csv','r') as ot:
            reader = csv.reader(ot)
            next(reader)
            for row in reader:
                if row[2] == str("Salary"):
                    sum_mon_salary += float(row[0])
        msg.showinfo("Monthly income from Salay","Monthly Income from salary for the "+str(self.nowmonth)+" month is "+ str(sum_mon_salary))
    
    
    def monoth(self):
        sum_other = 0
        with open('income'+str(self.nowmonth)+'.csv','r') as ot:
            reader = csv.reader(ot)
            next(reader)
            for row in reader:
                if row[2] == str("Other"):
                    sum_other += float(row[0])
        msg.showinfo("Monthly income from other","Monthly Income from other for the "+str(self.nowmonth)+" month is "+ str(sum_other))
    
    
        
    def yinc(self):
        data = []
        avmonths = []
        avdata = 0
        thismonth = datetime.date.today().month
        for i in range(thismonth+1):
            if os.path.exists('income'+str(i)+'.csv') == True:
                avdata += 1
        if avdata != thismonth:
            msg.showerror("Error ", "I have not that much data")
            if msg.askyesno("Available Data","Do you want me to plot the available data??") ==True:
                for i in range(thismonth+1):
                    sum = 0
                    if os.path.exists('income'+str(i)+'.csv'):
                        avmonths = i
                        with open('income'+str(i)+'.csv', 'r') as r:
                            reader = csv.reader(r)
                            next(reader)
                            for row in reader:
                                sum += int(row[0])
                        data=sum
                f = Figure(figsize=(4,5), dpi=100)
                ax = f.add_subplot(111)
                rects1 = ax.bar(avmonths,data)
                canvas = FigureCanvasTkAgg(f,Tk())
                canvas.get_tk_widget().pack()    
                        
                    
            
    def moninc(self):
        sum = 0
        with open('income'+str(self.nowmonth)+'.csv', 'r') as r:
            reader = csv.reader(r)
            next(reader)
            for row in reader:
                sum += int(row[0])
        msg.showinfo("Montly Income","YOUR INCOME FOR THE "+str(self.nowmonth)+" MONTH IS "+str(sum))
    
    def addinc(self):
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
            with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([str(self.textamount.get(1.0,END)),self.textdes.get(1.0,END),str(self.var_cat_list.get())])
            msg.showinfo("Income info","Amount: "+str(self.textamount.get(1.0,END))+"Description: "+self.textdes.get(1.0,END) +"Category: "+ str(self.var_cat_list.get()))
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
            
    
    def aboutmenu(self):
        msg.showinfo("About Income ","Income\nVersion 1.0")

    
    def helpmenu(self):
        msg.showinfo("Help","Enter an amount, a description, choose a category and press the add income button")
    
        
def main():
    root=Tk()
    I = Income(root)
    root.mainloop()
    
if __name__=='__main__':
    main()
