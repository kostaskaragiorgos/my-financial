""" keep track of your income """
from tkinter import Tk, Label, Text, Button, StringVar, Menu
from tkinter import messagebox as msg, OptionMenu, END
import datetime
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
def aboutmenu():
    """ about menu function """
    msg.showinfo("About Income ", "Income\nVersion 1.0")
def helpmenu():
    """ help menu function """
    msg.showinfo("Help", "Enter an amount, a description, choose a category and press the add income button")
class Income():
    """ income class """
    def __init__(self, master):
        self.master = master
        self.master.title("Income")
        self.master.geometry("250x160")
        self.master.resizable(False, False)
       # folders 
        if not os.path.exists("income"):
            os.mkdir("income")
            os.chdir("income")
        else:
            os.chdir("income")
        nowyear = datetime.date.today().year
        if not os.path.exists(str(nowyear)):
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        else:
            os.chdir(str(nowyear))
        #csv file
        self.nowmonth = datetime.date.today().month
        if not os.path.exists('income'+str(self.nowmonth)+'.csv'):
            with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Amount', 'Description', 'Category'])
        #basic gui
        self.amountl = Label(self.master,
                             text="Enter the amount")
        self.amountl.pack()
        self.textamount = Text(self.master, height=1)
        self.textamount.pack()
        self.desl = Label(self.master, text="Enter the description")
        self.desl.pack()
        self.textdes = Text(self.master, height=1)
        self.textdes.pack()
        category_list = list(["Salary", "Other"])
        self.var_cat_list = StringVar(master)
        self.var_cat_list.set(category_list[0])
        self.popupcatlistmenu = OptionMenu(self.master, self.var_cat_list, *category_list)
        self.popupcatlistmenu.pack()
        self.incomeb = Button(self.master, text="Add Income", command=self.addinc) 
        self.incomeb.pack()
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Add Income", accelerator='Ctrl+O', command=self.addinc)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.editmenu = Menu(self.menu, tearoff=0)
        self.editmenu.add_command(label="Clear Amount", accelerator='Ctrl+Z', command=self.clearamount)
        self.editmenu.add_command(label="Clear Description", accelerator='Alt+Z', command=self.cleardesc)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.charts = Menu(self.menu, tearoff=0)
        self.charts.add_command(label="Show Pie chart", accelerator='Ctrl+P', command=self.piechart)
        self.menu.add_cascade(label="Show", menu=self.charts)
        self.showinc = Menu(self.menu, tearoff=0)
        self.showinc.add_command(label="Monthly Salary", accelerator='Alt+S', command=self.monsal)
        self.showinc.add_command(label="Monthly Other", accelerator='Alt+O', command=self.monoth)
        self.showinc.add_command(label="Monthly Income", accelerator='Alt+M', command=self.moninc)
        self.menu.add_cascade(label="Total Income", menu=self.showinc)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-o>', lambda event: self.monoth())
        self.master.bind('<Alt-s>', lambda event: self.monsal())
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Alt-m>', lambda event: self.moninc())
        self.master.bind('<Control-o>', lambda event: self.addinc())
        self.master.bind('<Control-z>', lambda event: self.clearamount())
        self.master.bind('<Alt-z>', lambda event: self.cleardesc())
        self.master.bind('<Control-p>', lambda event: self.piechart())
    def piechart(self):
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        slices = [df[df['Category'] == "Salary"]['Amount'].sum(), df[df['Category'] == "Other"]['Amount'].sum()]
        cat = ['Salary', 'Other']
        col = ['red', 'green']
        plt.pie(slices, labels=cat, colors=col, startangle=90, autopct='%1.1f%%')
        plt.show()
    def clearamount(self):
        """ clears amount text field """
        self.textamount.delete(1.0, END)
    def cleardesc(self):
        """ clears description text field """
        self.textdes.delete(1.0, END)
    def monsal(self):
        """ monthly income from salary """
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly income from Salay", "Monthly Income from salary for the "+str(self.nowmonth)+" month is "+ str(df[df['Category'] == "Salary"]['Amount'].sum()))
    def monoth(self):
        """ monthly income from other ways except salary """
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly income from other", "Monthly Income from other for the "+str(self.nowmonth)+" month is "+ str(df[df['Category'] == "Other"]['Amount'].sum()))
    def moninc(self):
        """ total monthly income """
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        msg.showinfo("Montly Income", "YOUR INCOME FOR THE "+str(self.nowmonth)+" MONTH IS "+str(df['Amount'].sum()))
    def addinc(self):
        """ adds an income"""
        try:
            if float(self.textamount.get(1.0, END)) > 0 and (not self.textdes.count(1.0, END) == (1, )):
                with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow([str(self.textamount.get(1.0, END)), self.textdes.get(1.0, END), str(self.var_cat_list.get())])
                msg.showinfo("Income info", "Amount: "+str(self.textamount.get(1.0, END))+"Description: "+self.textdes.get(1.0, END) +"Category: "+ str(self.var_cat_list.get()))
            else:
                msg.showerror("Value Error", "Enter a number higher than zero \nEnter a description")
        except:
            msg.showerror("Value Error", "Enter a number higher than zero \nEnter a description")
        self.textamount.delete(1.0, END)
        self.textdes.delete(1.0, END)
    def exitmenu(self):
        """ exit menu function """
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
def main():
    """ main function """
    root = Tk()
    Income(root)
    root.mainloop()
if __name__ == '__main__':
    main()
