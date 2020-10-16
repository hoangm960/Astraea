import os
import webbrowser
from tkinter import (Button, Canvas, Frame, PhotoImage,
                      Scrollbar, Text, Tk)
from tkinter.constants import DISABLED, END, FLAT, RIGHT, WORD, Y
import subprocess
import pygetwindow as gw
import Login

class GUI:
    def __init__(self, role):
        self.role = role

    # Command on Button---------------
    # Edit Button
    def RunEdit(self):
        pass
    # Youtube Button
    def open_youtube(self):
        return webbrowser.open("http://youtube.com",new = 2)
    # Facebook Button
    def open_facebook(self):
        return webbrowser.open("https://facebook.com", new = 2)

    def test(self):
        pass

    def open_vscode(self):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        vs_window = gw.getWindowsWithTitle("Visual Studio Code")[0]
        vs_window.moveTo(0, 0)

    def read_file(self, filename):
        f = open(filename)
        text = f.read()
        f.close()
        return text

    def create_social_button(self, frame):
        frame.place(relx = 0, rely = 0.97, relwidth = 1, relheight = 0.03)
        photoYT = PhotoImage(file = r"icons/youtubeButton.png")
        photoimageYT = photoYT.subsample(7,'7')
        Button(frame, image = photoimageYT, relief = FLAT, command = lambda: self.open_youtube()).place(relx = 0, rely =0)
        photoFB = PhotoImage(file = r"icons/facebookButton.png")
        photoimageFB = photoFB.subsample(7, '7') 
        Button(frame, image = photoimageFB, relief = FLAT, command = lambda: self.open_facebook()).place(relx =0.08, rely =0)

    def create_edit_button(self, MainWindow):
        buttonEdit = Button(MainWindow, bg = '#347d6c', text = 'Sửa đổi', fg = 'white', font = ('Arial Bold',10))
        buttonEdit.place(relx = 0.5, rely = 0.84, relwidth = 0.2, relheight = 0.05, anchor = 'n')
        Login.enter_leave(buttonEdit, '#41a38c', '#347d6c')

    def create_test_button(self, MainWindow):
        buttonCheck = Button(MainWindow, bg = '#39c459', text = 'Kiểm tra', fg = 'white', font = ('Arial Bold',10))
        buttonCheck.place(relx = 0.5, rely = 0.84, relwidth = 0.2, relheight = 0.05, anchor = 'n')
        Login.enter_leave(buttonCheck, '#30e651', '#39c459')

    def Main(self):
        #---------------
        
        root = Tk()
        root.resizable(0,0)
        root.title('Pylearn')
        root.iconbitmap('icons/logo.ico')
        root.wm_attributes("-topmost", 1)
        root.geometry('350x700+1010+0')
        MainWindow = Canvas (root, width = 350, height = 700, bg = 'gray')
        MainWindow.pack()
        root.attributes('-toolwindow',1)
        
        self.open_vscode()

        # Button---------------

        #----------------------
        frame = Frame(MainWindow)
        self.create_social_button(frame)
        
        #---------------
        frame = Frame(MainWindow)
        frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.7)
        
        if self.role.lower() == 'teacher':
            self.create_edit_button(MainWindow)
        elif self.role.lower() == 'student':
            self.create_test_button(MainWindow)

        Sb = Scrollbar(frame)
        Sb.pack(side = RIGHT, fill = Y)
        text = Text(frame)
        with open("Text.txt", "r") as f:
            text.insert(END, f.read())
        text.configure(yscrollcommand=Sb.set, font=("Times New Roman", 10, "normal"), wrap=WORD, state=DISABLED)
        text.pack() 

        # def on_closing():
        #     if messagebox.askokcancel("Thông báo", "Xác nhận đóng chương trình?"):
        #         root.destroy()
        #         os.system("TASKKILL /F /IM Code.exe")
        # root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()

        