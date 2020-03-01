from tkinter import Tk, Button, Menu, Label, Text, OptionMenu, StringVar, END
from tkinter import messagebox as msg
import os 
import csv
import datetime
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
    def monexpother(self):
        """ calculates the other monthly expenses """
        sum_other = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as ot:
            reader = csv.reader(ot)
            for row in reader:
                if row[3] == str("Other"):
                    sum_other += float(row[1])
            ot.close()
        msg.showinfo("Monthly Expenses for other", "Monthly Expenses for other for the "+str(self.nowmonth)+" month is "+ str(sum_other))
    def monexptransportation(self):
        sum_transp = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as tp:
            reader = csv.reader(tp)
            for row in reader:
                if row[3] == str("Transportation"):
                    sum_transp += float(row[1])
            tp.close()
        msg.showinfo("Monthly Expenses for transportation", "Monthly Expenses for Transportation for the "+str(self.nowmonth)+ " month is "+ str(sum_transp))
    def monexpgrocery(self):
        sum_groc = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as o:
            reader = csv.reader(o)
            for row in reader:
                if row[3] == str("Grocery"):
                    sum_groc += float(row[1])
            o.close()
        msg.showinfo("Monthly Expenses for Grocery", "Monthly Expenses for Grocery for the "+str(self.nowmonth)+" month is " +str(sum_groc))
    def monexptaxes(self):
        sum_taxes = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as t:
            reader = csv.reader(t)
            for row in reader:
                if row[3] == str("Bills/Taxes"):
                    sum_taxes += float(row[1])
            t.close()
        msg.showinfo("Monthly Expenses for Bills/Taxes", "Monthly Expenses for Bills/Taxes for the "+str(self.nowmonth)+" month is "+str(sum_taxes))
    def monexp(self):
        sum = 0
        with open('expenses'+str(self.nowmonth)+'.csv', 'r') as r:
            reader = csv.reader(r)
            for row in reader:
                sum += float(row[1])
            r.close()
        msg.showinfo("Montly Expenses", "YOUR EXPENSES FOR THE "+str(self.nowmonth)+" MONTH IS "+str(sum))
    def addexp(self):
        valam = 0
        valdes = 0
        try:
            if float(self.textamount.get(1.0, END)) > 0:
                valam = 1
            else:
                msg.showerror("Value Error", "Enter a number higher than zero")
                self.textamount.delete(0, END)
        except:
            msg.showerror("Value Error", "Enter a number higher than zero")
            self.textamount.delete(1.0, END)
        if self.textdes.count(1.0, END) == (1, ):
            msg.showerror("Description Error", "Enter a description")
        else:
            valdes = 1
        if valam == 1 and valdes == 1:
            msg.showinfo("Expanse", "Day:"+str(datetime.date.today().day) +"\nAmount:"+str(self.textamount.get(1.0, END)) +"\nDescription:" + self.textdes.get(1.0, END) + "\nCategory:"+str(self.var_cat_list.get()))
            with open('expenses'+str(self.nowmonth)+'.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([str(datetime.date.today().day), str(self.textamount.get(1.0, END)), self.textdes.get(1.0, END), str(self.var_cat_list.get())])
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