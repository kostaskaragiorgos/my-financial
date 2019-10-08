from tkinter import *
from tkinter import messagebox as msg
import random

class Saving_game():
    def __init__(self,master):
        self.master = master
        self.master.title("Saving Game")
        self.master.geometry("150x150")
        self.master.resizable(False,False)
        
        self.menu = Menu(self.master)
        
        self.file_menu = Menu(self.menu,tearoff = 0)
        self.file_menu.add_command(label="Exit",accelerator= 'Alt+F4',command = self.exitmenu)
        self.menu.add_cascade(label = "File",menu=self.file_menu)
        
        self.about_menu = Menu(self.menu,tearoff = 0)
        self.about_menu.add_command(label = "About",accelerator= 'Ctrl+I',command=self.aboutmenu)
        self.menu.add_cascade(label="About",menu=self.about_menu)
        
        self.help_menu = Menu(self.menu,tearoff = 0)
        self.help_menu.add_command(label = "Help",accelerator = 'Ctrl+F1',command=self.helpmenu)
        self.menu.add_cascade(label="Help",menu=self.help_menu)
        
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>',lambda event: self.exitmenu())
        self.master.bind('<Control-F1>',lambda event: self.helpmenu())
        self.master.bind('<Control-i>',lambda event: self.aboutmenu())
        
        
        self.rollb = Button(self.master,text = "Roll",command = self.rolld)
        self.rollb.pack()
    
    
    def exitmenu(self):
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    
    def helpmenu(self):
        pass
    
    def aboutmenu(self):
        pass
    
    def rolld(self):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        msg.showinfo("Saving Amount","Dice 1:"+str(d1)+"\nDice 2:"+str(d2)+"\nThis week you have to save "+str(d1+d2))
        
def main():
    root=Tk()
    S = Saving_game(root)
    root.mainloop()
    
if __name__=='__main__':
    main()