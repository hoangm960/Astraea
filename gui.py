import os
import webbrowser
from tkinter import (Button, Canvas, Checkbutton, Frame, Label, Listbox, PhotoImage,
                      Scrollbar, Text, Tk)
from tkinter.constants import BOTH, DISABLED, END, FLAT, LEFT, RIGHT, WORD, Y
import subprocess
import pygetwindow as gw

def highlight_button(button_name, colour1, colour2):
    def on_enter(e):
        button_name['background'] = colour1
    def on_leave(e):
        button_name['background'] = colour2
    button_name.bind("<Enter>", on_enter)
    button_name.bind("<Leave>", on_leave)

class GUI:
    
    class SocialFrame(Frame):

        class YoutubeButton(Button):
            def __init__(self, root, *args, **kwargs):
                Button.__init__(self, root, *args, **kwargs)
                self.place(relx = 0, rely =0)
                photoYT = PhotoImage(file = r"icons/youtubeButton.png")
                photoimageYT = photoYT.subsample(7,'7')
                self.config(image= photoimageYT, command = lambda: self.open_youtube())

            def open_youtube(self):
                return webbrowser.open("http://youtube.com",new = 2)

        class FacebookButton(Button):
            def __init__(self, root, *args, **kwargs):
                Button.__init__(self, root, *args, **kwargs)
                self.place(relx =0.08, rely =0)
                photoFB = PhotoImage(file = r"icons/facebookButton.png")
                photoimageFB = photoFB.subsample(7, '7') 
                self.config(image = photoimageFB, command = lambda: self.open_facebook())

            def open_facebook(self):
                return webbrowser.open("https://facebook.com", new = 2)

        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.5, rely = 0.84, relwidth = 0.2, relheight = 0.05, anchor = 'n')

        def get_button(self):
            self.place(relx = 0, rely = 0.97, relwidth = 1, relheight = 0.03)
            self.YoutubeButton(self, relief = FLAT)
            self.FacebookButton(self, relief = FLAT)


    class EditButton(Button):
        def __init__(self, root, *args, **kwargs):
            Button.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.5, rely = 0.84, relwidth = 0.2, relheight = 0.05, anchor = 'n')
            highlight_button(self, '#41a38c', '#347d6c')


    class CheckButton(Button):
        def __init__(self, root, *args, **kwargs):
            Button.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.5, rely = 0.88, relwidth = 0.2, relheight = 0.05, anchor = 'n')
            highlight_button(self, '#30e651', '#39c459')
    

    class Scoreboard(Tk):
        class LessonFrame(Frame):
            def __init__(self, root, *args, **kwargs):
                Frame.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.01, rely = 0.01, relwidth = 0.95, relheight = 0.04)
            
            def get_content(self):
                Lesson = Label(self, text = 'Lesson 1 : GETTING STARTED', bg = '#6292bf', fg = 'white', font = ('Arial Bold',10))
                Lesson.place(relx = 0,rely = 0)
        class TitleFrame(Frame):
            def __init__(self, root, *args, **kwargs):
                Frame.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.01, rely = 0.05, relwidth = 0.98, relheight = 0.04)
            
            def get_content(self):
                Content = Label(self, text =' Bài tập với lệnh print', bg = '#addcf0', fg = 'white', font = ('Arial Bold',10))
                Content.place(relx = 0.03,rely = 0.01)

        class ContentFrame(Frame):
            def __init__(self, root, *args, **kwargs):
                Frame.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.01, rely = 0.1, relwidth = 0.98, relheight = 0.1)
            
            def get_content(self):
                Content = Label(self, text ='Bài tập 1', bg = '#88d6f7', fg = '#00344a', font = ('Arial Bold',10))
                Content.place(relx = 0.03, rely = 0.1, relwidth = 0.95)


        def __init__(self, *args, **kwargs):
            Tk.__init__(self, *args, **kwargs)
            self.title('Kết quả bài làm')
            self.geometry('700x500+250+100')
            self.resizable(0,0)
            self.wm_attributes("-topmost", 1)
            self.attributes('-toolwindow',1)

        def get_canvas(self):
            MarkBG = Canvas(self, bg = '#6292bf', width = 800, height = 600)
            MarkBG.pack()

            self.LessonFrame(MarkBG, bg = '#6292bf').get_content()
            
            self.TitleFrame(self, bg = '#addcf0').get_content()

            self.ContentFrame(self, bg = 'white').get_content()


    class Tasks_frame(Frame):
        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.4)

        def get_frame(self):
            Sb = Scrollbar(self)
            text = Text(self, height= 50, width=100, yscrollcommand= Sb.set, state= DISABLED)
            Sb.config(command= text.yview)
            Sb.pack(side = RIGHT, fill = Y)
            text.pack(side= LEFT, fill= BOTH, expand= True)

            with open("Text.txt", "r",encoding = 'utf8') as f:
                lines = f.readlines()
                for line in lines:
                    Tickbox = Checkbutton(self, activebackground= '#43e64b', bg= 'white', text= line, justify= LEFT, wraplength= 200)
                    text.window_create(END, window= Tickbox)
                    text.insert(END, "\n")


    class Tutorial_Frame(Frame):
        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.1, rely = 0.55, relwidth = 0.8, relheight = 0.3)
        
        def get_frame(self):
            Sb = Scrollbar(self)
            text = Text(self, height= 50, width=100, yscrollcommand=Sb.set, font=("Arial", 12), wrap=WORD, state=DISABLED)
            Sb.config(command= text.yview)
            Sb.pack(side = RIGHT, fill = Y)
            text.pack(side= LEFT, fill= BOTH, expand= True) 
            with open("text2.txt", "r", encoding = 'utf8') as f:
                text.insert(END, f.read())


    def __init__(self, role):
        self.role = role
    # Command on Button---------------

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

    def create_text(self, MainWindow, relx, rely, relwidth, relheight):
        frame = Frame(MainWindow)
        frame.place(relx = relx, rely = rely, relwidth = relwidth, relheight = relheight)
        
        Sb = Scrollbar(frame)
        text = Text(frame, height= 50, width=100, yscrollcommand= Sb.set)
        Sb.config(command= text.yview)
        Sb.pack(side = RIGHT, fill = Y)
        text.pack(side= LEFT, fill= BOTH, expand= True)

        
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
        
        # self.open_vscode()

        # Button---------------

        #----------------------
        self.SocialFrame(MainWindow).get_button()
        
        #---------------
        
        if self.role.lower() == 'teacher':
            self.EditButton(MainWindow, bg = '#347d6c', text = 'Sửa đổi', fg = 'white', font = ('Arial Bold',10))
        elif self.role.lower() == 'student':
            self.CheckButton(MainWindow, bg = '#39c459', text = 'Kiểm tra', fg = 'white', font = ('Arial Bold',10))

        self.Tasks_frame(MainWindow).get_frame()
        
        self.Tutorial_Frame(MainWindow).get_frame()

        # def on_closing():
        #     if messagebox.askokcancel("Thông báo", "Xác nhận đóng chương trình?"):
        #         root.destroy()
        #         os.system("TASKKILL /F /IM Code.exe")
        # root.protocol("WM_DELETE_WINDOW", on_closing)

        self.Scoreboard().get_canvas()
        root.mainloop()
    