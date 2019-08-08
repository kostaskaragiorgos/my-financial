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
        os.chdir("income")
        
        nowyear = datetime.date.today().year
        
        if os.path.exists(str(nowyear)) == False:
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        os.chdir(str(nowyear))
        
        #csv file
        self.nowmonth = datetime.date.today().month
        if os.path.exists('income'+str(self.nowmonth)+'.csv') == False:
            with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
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
        
        self.incomeb =Button(self.master,text = "Add Income",command = self.addinc) 
        self.incomeb.pack()

        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label = "Add Income",accelerator = 'Ctrl+O',command = self.addinc)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.showinc = Menu(self.menu,tearoff = 0)
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
        
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event:self.aboutmenu())
        self.master.bind('<Alt-m>',lambda event:self.moninc())
        self.master.bind('<Control-o>',lambda event:self.addinc())
        self.master.bind('<Alt-y>',lambda event:self.yinc())
        
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
                            r.close()
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
            r.close()
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
                thewriter.writerow([str(self.textamount.get(1.0,END)),self.textdes.get(1.0,END)])
                f.close()
            
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
            
    
    def aboutmenu(self):
        msg.showinfo("About Income ","Income\nVersion 1.0")

    
    def helpmenu(self):
        pass
    
        
def main():
    root=Tk()
    I = Income(root)
    root.mainloop()
    
if __name__=='__main__':
    main()