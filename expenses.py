""" keep track of your expenses """
from tkinter import Tk, Button, Menu, Label, Text, OptionMenu, StringVar, END
from tkinter import messagebox as msg
import os 
import csv
import datetime
import pandas as pd
def aboutmenu():
    """ about menu class """
    msg.showinfo("About", "Expenses\nVersion 1.0")
class Expenses():
    """ expenses class """
    def __init__(self, master):
        self.master = master
        self.master.title("Expenses")
        self.master.geometry("250x140")
        self.master.resizable(False, False)
       # folders 
        if not os.path.exists("expenses"):
            os.mkdir("expenses")
            os.chdir("expenses")
        else:
            os.chdir("expenses")
        nowyear = datetime.date.today().year
        if not os.path.exists(str(nowyear)):
            os.mkdir(str(nowyear))
            os.chdir(str(nowyear))
        else:
            os.chdir(str(nowyear))
        #csv file
        self.nowmonth = datetime.date.today().month
        if not os.path.exists('expenses'+str(self.nowmonth)+'.csv'):
            with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Day', 'Amount', 'Description', 'Category']) 
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Clear Amount", accelerator='Ctrl+Z', command=self.clearamount)
        self.edit_menu.add_command(label="Clear Description", accelerator='Alt+Z', command=self.cleardes)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.show = Menu(self.menu, tearoff=0)
        self.show.add_command(label="Show Monthly Other", accelerator='Alt+O', command=self.monexpother)
        self.show.add_command(label="Show Monthly Transportation", accelerator='Alt+T', command=self.monexptransportation)
        self.show.add_command(label="Show Monthly Grocery", accelerator='Alt+G', command=self.monexpgrocery)
        self.show.add_command(label="Show Monthly Bills/Taxes", accelerator='Alt+B', command=self.monexptaxes)
        self.show.add_command(label='Show Monthly Expenses', accelerator='Alt+S', command=self.monexp)
        self.menu.add_cascade(label="Show", menu=self.show)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1')
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-o>', lambda event: self.monexpother())
        self.master.bind('<Alt-t>', lambda event: self.monexptransportation())
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>')
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Alt-s>', lambda event: self.monexp())
        self.master.bind('<Alt-b>', lambda event: self.monexptaxes())
        self.master.bind('<Alt-g>', lambda event: self.monexpgrocery())
        self.master.bind('<Control-z>', lambda event: self.clearamount())
        self.master.bind('<Alt-z>', lambda event: self.cleardes())
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
        category_list = list(["Bills/Taxes", "Grocery", "Transportation", "Other"])
        self.var_cat_list = StringVar(master)
        self.var_cat_list.set(category_list[0])
        self.popupcatlistmenu = OptionMenu(self.master, self.var_cat_list, *category_list)
        self.popupcatlistmenu.pack()
        self.incomeb = Button(self.master, text="Add Expense", command=self.addexp) 
        self.incomeb.pack()
    def clearamount(self):
        """ clears amount text field """
        self.textamount.delete(1.0, END)
    def cleardes(self):
        """ clears description text field """
        self.textdes.delete(1.0, END)
    def monexpother(self):
        """ calculates the other monthly expenses """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly Expenses for other", "Monthly Expenses for other for the "+str(self.nowmonth)+" month is "+ str(df[df['Category'] == "Other"]['Amount'].sum()))
    def monexptransportation(self):
        """ shows monthly expenses for transportation"""
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly Expenses for transportation", "Monthly Expenses for Transportation for the "+str(self.nowmonth)+ " month is "+ str(df[df['Category'] == "Transportation"]['Amount'].sum()))
    def monexpgrocery(self):
        """ shows expenses for grocery"""
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly Expenses for Grocery", "Monthly Expenses for Grocery for the "+str(self.nowmonth)+" month is " +str(df[df['Category'] == "Grocery"]['Amount'].sum()))
    def monexptaxes(self):
        """ shows expenses for bills/Taxes """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        msg.showinfo("Monthly Expenses for Bills/Taxes", "Monthly Expenses for Bills/Taxes for the "+str(self.nowmonth)+" month is "+str(df[df['Category'] == "Grocery"]['Amount'].sum()))
    def monexp(self):
        """ shows montly Expenses"""
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        msg.showinfo("Montly Expenses", "YOUR EXPENSES FOR THE "+str(self.nowmonth)+" MONTH IS "+str(df['Amount'].sum()))
    def addexp(self):
        """ adds an expense"""
        try:
            if float(self.textamount.get(1.0, END)) > 0 and (not self.textdes.count(1.0, END) == (1, )):
                with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow([str(datetime.date.today().day), str(self.textamount.get(1.0, END)), self.textdes.get(1.0, END), str(self.var_cat_list.get())])
                msg.showinfo("Expanse", "Day:"+str(datetime.date.today().day) +"\nAmount:"+str(self.textamount.get(1.0, END)) +"\nDescription:" + self.textdes.get(1.0, END) + "\nCategory:"+str(self.var_cat_list.get()))
            else:
                msg.showerror("Value Error", "Enter a number higher than zero\n Enter a description")
        except:
            msg.showerror("Value Error", "Enter a number higher than zero\n Enter a description")
        self.textamount.delete(1.0, END)
        self.textdes.delete(1.0, END)
    def exitmenu(self):
        """ exit menu function """
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
def main():
    """ main function """
    root = Tk()
    Expenses(root)
    root.mainloop()
if __name__ == '__main__':
    main()