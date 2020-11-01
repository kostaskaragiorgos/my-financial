""" keep track of your expenses """
from tkinter import Tk, Button, Menu, Label, Text, OptionMenu, StringVar, END
from tkinter import messagebox as msg, simpledialog
from tkinter import filedialog
import os
import csv
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def savetxt(filename, df, minexp, maxexp):
    """ save overview to a .txt file """
    cat = ['Other', 'Transportation', 'Grocery', 'Bills/Taxes']
    f = open(str(filename)+".txt", 'a')
    for i in cat:
        f.write(str(i)+"\n" + str(df[df['Category'] == i]['Amount'].sum()))
    f.write("\nTotal:"+ str(df['Amount'].sum()))
    f.write("\nMin:"+ str(minexp))
    f.write("\nMax:"+ str(maxexp))
    msg.showinfo("SUCCESS", "Overview saved successfully")
def savecsv(filename, df, minexp, maxexp):
    """ save overview to a .csv file """
    cat = ['Other', 'Transportation', 'Grocery', 'Bills/Taxes']
    with open(filename+'.csv', 'a+') as f:
        thewriter = csv.writer(f)
        for i in cat:
            thewriter.writerow([i, str(df[df['Category'] == i]['Amount'].sum())])
        thewriter.writerow(["Total:", str(df['Amount'].sum())])
        thewriter.writerow(["Min:", str(minexp)])
        thewriter.writerow(["Max:", str(maxexp)])
    msg.showinfo("SUCCESS", "Overview saved successfully")
def check_save(filenamesave, df, minexp, maxexp):
    """ saves the overview by type """
    if  filenamesave.endswith(".txt"):
        savetxt(filenamesave, df, minexp, maxexp)
    elif filenamesave.endswith(".csv"):
        savecsv(filenamesave, df, minexp, maxexp)
    else:
        msg.showerror("Abort", "Abort")
def helpmenu():
    """ help menu """
    msg.showinfo("Help", "You can keep track of your expenses")
def aboutmenu():
    """ about menu class """
    msg.showinfo("About", "Expenses\nVersion 1.0")
def foldercreate(foldername):
    """ creates a folder and sets it as current directory """
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    os.chdir(foldername)
class Expenses():
    """ expenses class """
    def __init__(self, master):
        self.master = master
        self.master.title("Expenses")
        self.master.geometry("250x170")
        self.master.resizable(False, False)
       # folders
        foldercreate("expenses")
        nowyear = datetime.date.today().year
        foldercreate(str(nowyear))
        #csv file
        self.nowmonth = datetime.date.today().month
        self.filenamesave = ""
        if not os.path.exists('expenses'+str(self.nowmonth)+'.csv'):
            with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Date', 'Amount', 'Description', 'Category'])
        if not os.path.exists('expenses budget'+str(self.nowmonth)+'.csv'):
            with open('expeses budget'+ str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Grocery Budget', 'Other Budget', 'Transportation Budget', 'Bills/Taxes Budget'])
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Add Expense",
                                   accelerator='Ctrl+O', command=self.addexp)
        self.file_menu.add_command(label="Save Overview as",
                                   accelerator='Ctrl+S', command=self.saveas)
        self.file_menu.add_command(label="Exit",
                                   accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Clear Amount",
                                   accelerator='Ctrl+Z', command=self.clearamount)
        self.edit_menu.add_command(label="Clear Description",
                                   accelerator='Alt+Z', command=self.cleardes)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.budget_menu = Menu(self.menu, tearoff=0)
        self.submenu = Menu(self.budget_menu, tearoff=0)
        self.submenu.add_command(label="Set Grocery budget",
                                 accelerator='Alt+P', command=self.setgrocerybudget)
        self.submenu.add_command(label="Set Other budget",
                                 accelerator='Alt+Q', command=self.setotherbudget)
        self.submenu.add_command(label="Set Transportation budget",
                                 accelerator='Ctrl+Q', command=self.settransportationbudget)
        self.submenu.add_command(label="Set Bills/Taxes",
                                 accelerator='Ctrl+W', command=self.setbillsortaxesbudget)
        self.budget_menu.add_cascade(label="Set budget", menu=self.submenu, underline=0)
        self.budget_menu.add_command(label="Show budget")
        self.menu.add_cascade(label="Budget", menu=self.budget_menu)
        self.charts = Menu(self.menu, tearoff=0)
        self.charts.add_command(label="Bar Chart", accelerator='Ctrl+B',
                                command=lambda: self.Charts("Bar Chart of Expenses",
                                                            ["Other", "Transportation", "Grocery", "Bills/Taxes"],
                                                            'bar', ['r', 'g', 'y', 'b']))
        self.charts.add_command(label="Pie Chart", accelerator='Ctrl+P',
                                command=lambda: self.Charts("Pie Chart of Expenses",
                                                            ["Other", "Transportation", "Grocery", "Bills/Taxes"],
                                                            'pie', ['r', 'g', 'y', 'b']))
        self.charts.add_command(label="Show time series m",
                                accelerator='Ctrl+T', command=self.timeseriesmonth)
        self.menu.add_cascade(label="Charts", menu=self.charts)
        self.show = Menu(self.menu, tearoff=0)
        self.show.add_command(label="Show Monthly Other",
                              accelerator='Alt+O',
                              command=lambda: self.monthlyexpenses('Other'))
        self.show.add_command(label="Show Monthly Transportation",
                              accelerator='Alt+T',
                              command=lambda: self.monthlyexpenses('Transportation'))
        self.show.add_command(label="Show Monthly Grocery",
                              accelerator='Alt+G',
                              command=lambda: self.monthlyexpenses('Grocery'))
        self.show.add_command(label="Show Monthly Bills/Taxes",
                              accelerator='Alt+B',
                              command=lambda: self.monthlyexpenses('Bills/Taxes'))
        self.show.add_command(label='Show Monthly Expenses',
                              accelerator='Alt+S',
                              command=lambda: self.monthlyexpenses(None))
        self.show.add_command(label="Show Overview",
                              accelerator='Ctrl+N',
                              command=self.show_overview)
        self.show.add_command(label="Show Expenses Info",
                              accelerator='Alt+N',
                              command=self.show_expenses_info)
        self.menu.add_cascade(label="Show", menu=self.show)
        self.showtrans = Menu(self.menu, tearoff=0)
        self.showtrans.add_command(label="Show Number of Total Transactions",
                                   accelerator='Alt+W',
                                   command= lambda: self.monthlytransactions(None))
        self.showtrans.add_command(label="Show Number of (Other) Transactions",
                                   accelerator='Alt+I',
                                   command= lambda: self.monthlytransactions('Other'))
        self.showtrans.add_command(label="Show Number of (Transportation) Transactions",
                                   accelerator='Alt+E',
                                   command= lambda: self.monthlytransactions('Transportation'))
        self.showtrans.add_command(label="Show Number of (Grocery) Transactions",
                                   accelerator='Ctrl+E',
                                   command= lambda: self.monthlytransactions('Grocery'))
        self.showtrans.add_command(label="Show Number of (Bills/Taxes) Transactions",
                                   accelerator='Ctrl+Y',
                                   command= lambda: self.monthlytransactions('Bills/Taxes'))
        self.menu.add_cascade(label="Transactions", menu=self.showtrans)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About",
                                    accelerator='Ctrl+I',
                                    command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.master.config(menu=self.menu)
        self.master.bind('<Alt-i>', lambda event: self.monthlytransactions('Other'))
        self.master.bind('<Alt-w>', lambda event: self.monthlytransactions(None))
        self.master.bind('<Alt-e>', lambda event: self.monthlytransactions('Transportation'))
        self.master.bind('<Control-e>', lambda event: self.monthlytransactions('Grocery'))
        self.master.bind('<Control-y>', lambda event:self.monthlytransactions('Bills/Taxes'))
        self.master.bind('<Alt-p>', lambda event: self.setgrocerybudget())
        self.master.bind('<Alt-q>', lambda event: self.setotherbudget())
        self.master.bind('<Control-q>', lambda event: self.settransportationbudget())
        self.master.bind('<Control-w>', lambda event: self.setbillsortaxesbudget())
        self.master.bind('<Control-t>', lambda event: self.timeseriesmonth())
        self.master.bind('<Control-s>', lambda event: self.saveas())
        self.master.bind('<Control-o>', lambda event: self.addexp())
        self.master.bind('<Alt-o>', lambda event: self.monthlyexpenses('Other'))
        self.master.bind('<Alt-t>', lambda event: self.monthlyexpenses('Transportation'))
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Alt-s>', lambda event: self.monthlyexpenses(None))
        self.master.bind('<Alt-b>', lambda event: self.monthlyexpenses('Bills/Taxes'))
        self.master.bind('<Alt-g>', lambda event: self.monthlyexpenses('Grocery'))
        self.master.bind('<Control-z>', lambda event: self.clearamount())
        self.master.bind('<Alt-z>', lambda event: self.cleardes())
        self.master.bind('<Control-p>', lambda event: self.Charts("Pie Chart of Expenses", ["Other", "Transportation", "Grocery", "Bills/Taxes"], 'pie', ['r', 'g', 'y', 'b']))
        self.master.bind('<Control-b>', lambda event: self.Charts("Bar Chart of Expenses", ["Other", "Transportation", "Grocery", "Bills/Taxes"], 'bar', ['r', 'g', 'y', 'b']))
        self.master.bind('<Control-n>', lambda event: self.show_overview())
        self.master.bind('<Alt-n>', lambda event: self.show_expenses_info())
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
    def setbillsortaxesbudget(self):
        """ sets a bills/taxes budget """
        self.billsortaxes_budget = simpledialog.askfloat("Bills/Taxes Budget", "Enter your bills/taxes budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
        while self.billsortaxes_budget is None:
            self.billsortaxes_budget = simpledialog.askfloat("Bills/Taxes Budget", "Enter your bills/taxes budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
    def settransportationbudget(self):
        """ sets a transportation budget"""
        self.transportation_budget = simpledialog.askfloat("Transportation Budget", "Enter your transportation budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
        while self.transportation_budget is None:
            self.transportation_budget = simpledialog.askfloat("Transportation Budget", "Enter your transportation budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
    def setotherbudget(self):
        """ sets other budget"""
        self.other_budget = simpledialog.askfloat("Other Budget", "Enter your other budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
        while self.other_budget is None:
            self.other_budget = simpledialog.askfloat("Other Budget", "Enter your other budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
    def setgrocerybudget(self):
        """ sets a grocery budget """
        self.grocery_budeget = simpledialog.askfloat("Grocery Budget", "Enter your gorcery budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
        while self.grocery_budeget is None:
            self.grocery_budeget = simpledialog.askfloat("Grocery Budget", "Enter your gorcery budget", parent=self.master, minvalue=1.0, maxvalue=10_000.00)
    def show_expenses_info(self):
        """ shows expenses info """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO EXPENSES INFO")
        else:
            df.replace(r'\r\n', ' ', regex=True, inplace=True)
            msg.showinfo("EXPENSES INFO", df.to_string())
    def timeseriesmonth(self):
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("No Expenses", "No Expenses")
        else:
            plt.plot(df['Date'], df['Amount'])
            plt.show()
    def saveas(self):
        """ saves overview """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("No Expenses", "No Expenses")
        else:
            minexp = min([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Transportation"]['Amount'].sum(), df[df['Category'] == "Grocery"]['Amount'].sum(), df[df['Category'] == "Bills/Taxes"]['Amount'].sum()])
            maxexp = max([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Transportation"]['Amount'].sum(), df[df['Category'] == "Grocery"]['Amount'].sum(), df[df['Category'] == "Bills/Taxes"]['Amount'].sum()])
            filenamesave = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("csv files", "*.csv"), ("all files", "*.*")))
            check_save(filenamesave, df, minexp, maxexp)
    def chart_save_user_verification(self):
        """ user enters the name of the file """
        self.filechartname = simpledialog.askstring("CHART NAME", "Enter chart name", parent=self.master)
        while self.filechartname is None or (not self.filechartname.strip()):
            self.filechartname = simpledialog.askstring("CHART NAME", "Enter chart name", parent=self.master)
        return self.filechartname
    def savechartfunction(self, save):
        """ saves the chart to an image file """
        if save:
            fname = self.chart_save_user_verification()
            plt.savefig(fname+'.png', dpi=100)
        else:
            msg.showinfo("NO FILE SAVED", "NO FILE SAVED")
    def show_overview(self):
        """ shows overview """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("No Expenses", "No Expenses")
        else:
            minexp = min([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Transportation"]['Amount'].sum(), df[df['Category'] == "Grocery"]['Amount'].sum(), df[df['Category'] == "Bills/Taxes"]['Amount'].sum()])
            maxexp = max([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Transportation"]['Amount'].sum(), df[df['Category'] == "Grocery"]['Amount'].sum(), df[df['Category'] == "Bills/Taxes"]['Amount'].sum()])
            msg.showinfo("Expenses Overview", "Other:" + str(df[df['Category'] == "Other"]['Amount'].sum()) + "\nTransportation:" + str(df[df['Category'] == "Transportation"]['Amount'].sum())+
                         "\nGrocery:" + str(df[df['Category'] == "Grocery"]['Amount'].sum()) + "\nBills/Taxes:" + str(df[df['Category'] == "Bills/Taxes"]['Amount'].sum())+ "\nTotal:"+str(df['Amount'].sum())+ "\nMax:"+str(maxexp)+"\nMin:"+str(minexp))
    def Charts(self, title, categories, ctype, color):
        """ expenses  charts by ctype"""
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        data = [df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Transportation"]['Amount'].sum(), df[df['Category'] == "Grocery"]['Amount'].sum(), df[df['Category'] == "Bills/Taxes"]['Amount'].sum()]
        if df['Amount'].sum() == 0:
            msg.showerror("No Expenses", "No Expenses")
        else:
            if ctype == 'bar':
                plt.bar(np.arange(4), data, color=color)
                plt.xticks(np.arange(4), categories)
            else:
                plt.pie(data, labels=categories, colors=color, startangle=90, autopct='%1.1f%%')
            plt.title(title)
            save = msg.askyesno("SAVE CHART", "DO YOU WANT TO SAVE THE CHART")
            self.savechartfunction(save)
            plt.show()
            plt.draw()
    def clearamount(self):
        """ clears amount text field """
        self.textamount.delete(1.0, END)
    def cleardes(self):
        """ clears description text field """
        self.textdes.delete(1.0, END)
    def monthlytransactions(self, category):
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("No Transactions", "No Transactions")
        elif category is None:
            msg.showinfo("Total Transactions", "The total transactions for the " + str(self.nowmonth) + " month are " + str(df.shape[0]))
        else:
            msg.showinfo("Monthly Transactions for "+
                         str(category),
                         "Monthly Transactrions for "+
                         str(category)+
                         " for the "+
                         str(self.nowmonth)+
                         " month are "+
                         str(len([df['Category'] == category])))

    def monthlyexpenses(self, category):
        """ calculates the monthly expenses by category """
        df = pd.read_csv('expenses'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("No Expenses", "No Expenses")
        elif category is None:
            msg.showinfo("Montly Expenses",
                         "YOUR EXPENSES FOR THE "+
                         str(self.nowmonth)+
                         " MONTH IS "+
                         str(df['Amount'].sum()))
        else:
            msg.showinfo("Monthly Expenses for "+
                         str(category),
                         "Monthly Expenses for "+
                         str(category)+
                         " for the "+
                         str(self.nowmonth)+
                         " month is "+
                         str(df[df['Category'] == category]['Amount'].sum()))
    def save_exp_to_csv(self):
        """ saves expenses to a csv file """
        with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([str(datetime.date.today().day), str(self.textamount.get(1.0, END)), self.textdes.get(1.0, END), str(self.var_cat_list.get())])
    def addexp(self):
        """ adds an expense"""
        try:
            if float(self.textamount.get(1.0, END)) >= 0 and (self.textdes.count(1.0, END) != (1, )):
                self.save_exp_to_csv()
                msg.showinfo("Expanse", "Date:"+str(datetime.date.today()) +"\nAmount:"+str(self.textamount.get(1.0, END)) +"\nDescription:" + self.textdes.get(1.0, END) + "\nCategory:"+str(self.var_cat_list.get()))
            else:
                msg.showerror("Value Error", "Enter a number higher than zero\nEnter a description")
        except ValueError:
            msg.showerror("Value Error", "Enter a number higher than zero\nEnter a description")
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
    