""" keep track of your income """
from tkinter import Tk, Label, Text, Button, StringVar, Menu, simpledialog
from tkinter import messagebox as msg, OptionMenu, END, filedialog
import datetime
import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def check_save(filename, df):
    """ checks the file type """
    if  filename.endswith(".txt"):
        savetxt(filename, df)
    elif filename.endswith(".csv"):
        savecsv(filename, df)
    else:
        msg.showerror("Abort", "Abort")
def savecsv(filename, df):
    """ saves  to csv """
    with open(filename+'.csv', 'a+') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["Other:", str(df[df['Category'] == "Other"]['Amount'].sum())])
        thewriter.writerow(["Salary:", str(df[df['Category'] == "Salary"]['Amount'].sum())])
        thewriter.writerow(["Total:", str(df['Amount'].sum())])
        thewriter.writerow(["Min:",
                            str(min([df[df['Category'] == "Other"]['Amount'].sum(),
                                     df[df['Category'] == "Salary"]['Amount'].sum()]))])
        thewriter.writerow(["Max:",
                            str(max([df[df['Category'] == "Other"]['Amount'].sum(),
                                     df[df['Category'] == "Salary"]['Amount'].sum()]))])
    msg.showinfo("SUCCESS", "Overview saved successfully")
def savetxt(filename, df):
    """ saves to txt """
    f = open(str(filename)+".txt", 'a')
    f.write("Other:"+ str(df[df['Category'] == "Other"]['Amount'].sum()))
    f.write("\nSalary:"+ str(df[df['Category'] == "Salary"]['Amount'].sum()))
    f.write("\nTotal:"+ str(df['Amount'].sum()))
    f.write("\nMin:"+ str(min([df[df['Category'] == "Other"]['Amount'].sum(),
                               df[df['Category'] == "Salary"]['Amount'].sum()])))
    f.write("\nMax:"+ str(max([df[df['Category'] == "Other"]['Amount'].sum(),
                               df[df['Category'] == "Salary"]['Amount'].sum()])))
    f.close()
    msg.showinfo("SUCCESS", "Overview saved successfully")
def aboutmenu():
    """ about menu function """
    msg.showinfo("About Income ", "Income\nVersion 1.0")
def foldercreate(foldername):
    """ creates folders and changes the current directory """
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    os.chdir(foldername)
def helpmenu():
    """ help menu function """
    msg.showinfo("Help", "Enter an amount, a description,"+
                 "choose a category and press the add income button")
class Income():
    """ income class """
    def __init__(self, master):
        self.master = master
        self.master.title("Income")
        self.master.geometry("250x170")
        self.master.resizable(False, False)
        # folders
        foldercreate('income')
        nowyear = datetime.date.today().year
        foldercreate(str(nowyear))
        #csv file
        self.nowmonth = datetime.date.today().month
        if not os.path.exists('income'+str(self.nowmonth)+'.csv'):
            with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Date', 'Amount', 'Description', 'Category'])
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
        self.file_menu.add_command(label="Save Overview as",
                                   accelerator='Ctrl+S', command=self.saveas)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.editmenu = Menu(self.menu, tearoff=0)
        self.editmenu.add_command(label="Clear Amount",
                                  accelerator='Ctrl+Z', command=self.clearamount)
        self.editmenu.add_command(label="Clear Description",
                                  accelerator='Alt+Z', command=self.cleardesc)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.show = Menu(self.menu, tearoff=0)
        self.show.add_command(label="Show Overview",
                              accelerator='Ctrl+N', command=self.show_overview)
        self.show.add_command(label="Show Bar chart",
                              accelerator='Ctrl+B',
                              command=lambda: self.Charts("Bar Chart of Income",
                                                          ["Other", "Salary"],
                                                          'bar',
                                                          ['r', 'g']))
        self.show.add_command(label="Show Pie chart",
                              accelerator='Ctrl+P',
                              command=lambda: self.Charts("Pie Chart of Income",
                                                          ["Other", "Salary"],
                                                          'pie',
                                                          ['r', 'g']))
        self.show.add_command(label="Show time series m", accelerator='Ctrl+T', command=self.timeseriesmonth)
        self.show.add_command(label="Show income info", accelerator='Alt+N', command=self.show_income_info)
        self.menu.add_cascade(label="Show", menu=self.show)
        self.showinc = Menu(self.menu, tearoff=0)
        self.showinc.add_command(label="Monthly Salary", accelerator='Alt+S', command=lambda: self.monthlyincome('Salary'))
        self.showinc.add_command(label="Monthly Other", accelerator='Alt+O', command=lambda: self.monthlyincome('Other'))
        self.showinc.add_command(label="Monthly Income", accelerator='Alt+M', command=lambda: self.monthlyincome(None))
        self.menu.add_cascade(label="Total Income", menu=self.showinc)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Control-t>', lambda event: self.timeseriesmonth())
        self.master.bind('<Control-s>', lambda event: self.saveas())
        self.master.bind('<Alt-o>', lambda event: self.monthlyincome('Other'))
        self.master.bind('<Alt-s>', lambda event: self.monthlyincome('Salary'))
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Alt-m>', lambda event: self.monthlyincome(None))
        self.master.bind('<Control-o>', lambda event: self.addinc())
        self.master.bind('<Control-z>', lambda event: self.clearamount())
        self.master.bind('<Alt-z>', lambda event: self.cleardesc())
        self.master.bind('<Control-p>',
                         lambda event: self.Charts("Pie Chart of Income",
                                                   ["Other", "Salary"],
                                                   'pie',
                                                   ['r', 'g']))
        self.master.bind('<Control-b>',
                         lambda event: self.Charts("Bar Chart of Income",
                                                   ["Other", "Salary"],
                                                   'bar',
                                                   ['r', 'g']))
        self.master.bind('<Control-n>', lambda event: self.show_overview())
        self.master.bind('<Alt-n>', lambda event: self.show_income_info())
    def show_income_info(self):
        """ shows income info """
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME INFO")
        else:
            df.replace(r'\r\n', ' ', regex=True, inplace=True)
            msg.showinfo("INCOME INFO", df.to_string())
    def timeseriesmonth(self):
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME")
        else:
            plt.plot(df['Date'], df['Amount'])
            plt.show()
    def saveas(self):
        """ Saves overview to a .txt or .csv file"""
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME TO SAVE")
        else:
            filenamesave = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("csv files", "*.csv"), ("all files", "*.*")))
            check_save(filenamesave, df)
    def show_overview(self):
        """ shows_overview"""
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME")
        else:
            minexp = min([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Salary"]['Amount'].sum()])
            maxexp = max([df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Salary"]['Amount'].sum()])
            msg.showinfo("Expenses Overview", "Other:" + str(df[df['Category'] == "Other"]['Amount'].sum()) +"\nSalary:" + str(df[df['Category'] == "Salary"]['Amount'].sum()) + "\nTotal:"+str(df['Amount'].sum())+ "\nMax:"+str(maxexp)+"\nMin:"+str(minexp))
    
    def chart_save_user_verification(self):
        """ user set an image file name """
        self.filechartname = simpledialog.askstring("CHART NAME", "Enter chart name", parent=self.master)
        while self.filechartname is None or (not self.filechartname.strip()):
            self.filechartname = simpledialog.askstring("CHART NAME", "Enter chart name", parent=self.master)
        return self.filechartname
    def savechartfunction(self, save):
        """ saves chart to an image file """
        if save:
            fname = self.chart_save_user_verification()
            plt.savefig(fname+'.png', dpi=100)
        else:
            msg.showinfo("NO FILE SAVED", "NO FILE SAVED")
    def Charts(self, title, categories, types, color):
        """ shows a bar chart of income"""
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        data = [df[df['Category'] == "Other"]['Amount'].sum(), df[df['Category'] == "Salary"]['Amount'].sum()]
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME")
        else:
            if types == 'bar':
                plt.bar(np.arange(2), data, color=color)
                plt.xticks(np.arange(2), categories)
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
    def cleardesc(self):
        """ clears description text field """
        self.textdes.delete(1.0, END)
    def monthlyincome(self, category):
        """ monthly income from salary """
        df = pd.read_csv('income'+str(self.nowmonth)+'.csv')
        if df['Amount'].sum() == 0:
            msg.showerror("ERROR", "NO INCOME")
        elif category is None:
            msg.showinfo("Montly Income", "YOUR INCOME FOR THE "+str(self.nowmonth)+" MONTH IS "+str(df['Amount'].sum()))
        else:
            msg.showinfo("Monthly income from "+str(category), "Monthly Income from "+str(category)+" for the "+str(self.nowmonth)+" month is "+ str(df[df['Category'] == category]['Amount'].sum()))
    def add_values_to_csv(self):
        """ adds income to a csv file """
        with open('income'+str(self.nowmonth)+'.csv', 'a+') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([str(datetime.date.today()), str(self.textamount.get(1.0, END)), self.textdes.get(1.0, END), str(self.var_cat_list.get())])
    def addinc(self):
        """ adds an income"""
        try:
            if float(self.textamount.get(1.0, END)) > 0 and (self.textdes.count(1.0, END) != (1, )):
                self.add_values_to_csv()
                msg.showinfo("Income info", "Amount: "+str(self.textamount.get(1.0, END))+"Description: "+self.textdes.get(1.0, END) +"Category: "+ str(self.var_cat_list.get()))
            else:
                msg.showerror("Value Error", "Enter a number higher than zero \nEnter a description")
        except ValueError:
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
