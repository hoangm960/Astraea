import os
import webbrowser
from tkinter import (Button, Canvas, Frame, Listbox, OptionMenu, PhotoImage,
                     Scrollbar, StringVar, Tk)
from tkinter.constants import END, FLAT, LEFT, RIGHT, Y
import subprocess
import pygetwindow as gw


# Command on Button---------------
 # Edit Button
def RunEdit():
    pass
 # Youtube Button
def open_youtube():
    return webbrowser.open("http://youtube.com",new = 2)
 # Facebook Button
def open_facebook():
    return webbrowser.open("https://facebook.com", new = 2)
 # Visual Studio Code Button

# def open_vscode():
#     return os.system(r"VScode\Code.exe")
 # Check code Button
def test():
    pass

def open_vscode():
    file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
    subprocess.call(file)
    vs_window = gw.getWindowsWithTitle("Visual Studio Code")[0]
    vs_window.moveTo(0, 0)

def read_file(filename):
    f = open(filename)
    text = f.read()
    f.close()
    return text
#---------------
root = Tk()
root.resizable(0,0)
root.title('Pylearn')
root.wm_attributes("-topmost", 1)
root.geometry('350x700+1010+0')
MainWindow = Canvas (root, width = 350, height = 700, bg = 'lightblue')
MainWindow.pack()
#root.overrideredirect(1)
root.attributes('-toolwindow',1)

open_vscode()

# Button---------------
frameOption = Frame(MainWindow)
frameOption.place(relx = 0.01, rely = 0.01, relwidth = 9.6, relheight = 0.04)
variable1 = StringVar(frameOption)

variable1.set('Option1')
#variable1.trace('w', RunEdit)
MenuOption1 =  OptionMenu(frameOption, variable1, "TextBox", "Settings")
MenuOption1.pack(side = LEFT)

variable2 = StringVar(frameOption)
variable2.set('Option2')
#variable2.trace('w', affect)
MenuOption2 = OptionMenu(frameOption, variable2, "TextBox2","Settings2")
MenuOption2.pack(side = LEFT)

variable3 = StringVar(frameOption)
variable3.set('Option3')
#variable2.trace('w', affect)
MenuOption3 = OptionMenu(frameOption, variable3, "TextBox3","Settings3")
MenuOption3.pack(side = LEFT)


variable4 = StringVar(frameOption)
variable4.set('Option4')
#variable2.trace('w', affect)
MenuOption4 = OptionMenu(frameOption, variable4, "TextBox4","Settings4")
MenuOption4.pack(side = LEFT)

#----------------------
frameYT = Frame(MainWindow)
frameYT.place(relx = 0.15, rely = 0.82, relwidth = 0.17, relheight = 0.05)
photoYT = PhotoImage(file = r"icon\youtubeButton.png")
photoimageYT = photoYT.subsample(3, str(3))
Button(frameYT, image = photoimageYT, relief = FLAT, command = lambda: open_youtube()).place(x = 0, y =0)

frameFB = Frame(MainWindow)
frameFB.place(relx = 0.65, rely = 0.82, relwidth = 0.17, relheight = 0.05)
photoFB = PhotoImage(file = r"icon\facebookButton.png")
photoimageFB = photoFB.subsample(3, str(3)) 
Button(frameFB, image = photoimageFB, relief = FLAT, command = lambda: open_facebook()).place(x = 0, y =0)

frameCheck = Frame(MainWindow)
frameCheck.place(relx = 0.4, rely = 0.9, relwidth = 0.198, relheight = 0.06)
buttonCheck = Button(frameCheck, width = 8, height = 2, bg = 'green', command = test, text = 'CHECK',
activebackground = 'lightgreen', relief = FLAT)
buttonCheck.place(relx = 0, rely =0)
#---------------
text = read_file("Text.txt")
frame = Frame(MainWindow)
frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.7)
  
Sb = Scrollbar(frame)
Sb.pack(side = RIGHT, fill = Y)    
mylist = Listbox(frame, width = 45, height =32, yscrollcommand = Sb.set )  
mylist.insert(END, text)
mylist.pack(side = LEFT)  
Sb.config(command = mylist.yview)

root.mainloop()
