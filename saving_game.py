""" saving game """
from tkinter import Tk, Menu, Button
from tkinter import messagebox as msg
import random
import os
import csv
def helpmenu():
    """ help menu function """
    msg.showinfo("Help", "Press the roll button and save up the total amount")
def aboutmenu():
    """ about menu function """
    msg.showinfo("About", "Saving Game\nVersion 1.0")
class SavingGame():
    """ saving game class """
    def __init__(self, master):
        self.master = master
        self.master.title("Saving Game")
        self.master.geometry("150x150")
        self.master.resizable(False, False)
        if not os.path.exists('Saving_Game.csv'):
            with open('Saving_Game.csv', 'a+') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Amount'])
                f.close()
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Roll", accelerator='Alt+S', command=self.rolld)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())
        self.master.bind('<Alt-s>', lambda event: self.rolld())
        self.rollb = Button(self.master, text="Roll", command=self.rolld)
        self.rollb.pack()
    def exitmenu(self):
        """ exit menu function """
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    def rolld(self):
        """ roll button function """
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        msg.showinfo("Saving Amount", "Dice 1:"+str(d1)+"\nDice 2:"+str(d2)+"\nThis week you have to save "+str(d1+d2))
        with open('Saving_Game.csv', 'a+') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(str(d1+d2))
def main():
    """ main function """
    root = Tk()
    SavingGame(root)
    root.mainloop()
if __name__ == '__main__':
    main()
