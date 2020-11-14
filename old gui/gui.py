from ctypes import alignment
import os
import subprocess
from tkinter import ttk
import tkinter as tk
import typing
import webbrowser
from tkinter import (Button, Canvas, Checkbutton, Entry, Frame, Label, Listbox,
                     PhotoImage, Scrollbar, Text, Tk, Toplevel, messagebox)
from tkinter.constants import (ALL, BOTH, BOTTOM, CENTER, DISABLED, END, FLAT,
                               HORIZONTAL, LEFT, NW, RIGHT, TOP, VERTICAL, WORD, X,
                               Y)
# from PIL import ImageTk, Image
import pygetwindow as gw
import check_algorithm
import Login

def highlight_button(button_name, colour1, colour2):
    def on_enter(e):
        button_name['background'] = colour1
    def on_leave(e):
        button_name['background'] = colour2
    button_name.bind("<Enter>", on_enter)
    button_name.bind("<Leave>", on_leave)

class GradientFrame(Canvas):
    __tag = "GradientFrame"

    hex_format = "#%04x%04x%04x"
    top2bottom = 1
    left2right = 2


    def __init__(self,parent,geometry,colors=("red","black"),direction=top2bottom,**kw):
        
        Canvas.__init__(self,parent,width=geometry[0],height=geometry[1],**kw)

        self.__geometry = geometry
        self.__colors = colors
        self.__direction = direction

        self.__drawGradient()

        
    def __drawGradient(self):

        self.delete(self.__tag)

        limit = self.__geometry[0] if self.__direction == self.left2right else self.__geometry[1]
       
        red1,green1,blue1 = self.winfo_rgb(self.__colors[0])
        red2,green2,blue2 = self.winfo_rgb(self.__colors[1])

        r_ratio = float(red2 - red1) / limit
        g_ratio = float(green2 - green1) / limit
        b_ratio = float(blue2 - blue1) / limit

        for pixel in range(limit):
            
            red = int( red1 + ( r_ratio * pixel ) )
            green = int( green1 + ( g_ratio * pixel ) )
            blue = int( blue1 + ( b_ratio * pixel ) )

            color = self.hex_format % (red,green,blue)

            x1 = pixel if self.__direction == self.left2right else 0
            y1 = 0 if self.__direction == self.left2right else pixel
            x2 = pixel if self.__direction == self.left2right else self.__geometry[0]
            y2 = self.__geometry[1] if self.__direction == self.left2right else pixel

            self.create_line(x1,y1,x2,y2 , tag=self.__tag , fill=color)


    def setColors(self,colors):

        self.__colors = colors
        self.__drawGradient()


    def setDirection(self,direction):

        if direction in (self.left2right,self.top2bottom):
            self.__direction = direction
            self.__drawGradient()
        else:
            raise ValueError('The "direction" parameter must be self.left2right or self.top2bottom')
        

    def setGeometry(self,geometry):

        self.config(width=geometry[0],height=geometry[1])
        self.__geometry = geometry
        self.__drawGradient()

class GUI:

    class SocialFrame(Frame):

        class YoutubeButton(Button):
            def __init__(self, root, *args, **kwargs):
                Button.__init__(self, root, *args, **kwargs)
                self.place(relx = 0, rely = 0)
                photoYT = PhotoImage(file = r"icons/youtubeButton.png")
                photoimageYT = photoYT.subsample(7,'7')
                self.config(image= photoimageYT, command = lambda: self.open_youtube())
                

            def open_youtube(self):
                return webbrowser.open("http://youtube.com",new = 2)
        
        class FacebookButton(Button):
            def open_facebook(self):
                return webbrowser.open("https://facebook.com", new = 2)
            def __init__(self, root, *args, **kwargs):
                Button.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.1, rely = 0)
                photoFB = PhotoImage(file = r"icons/facebookButton.png")
                photoimageFB = photoFB.subsample(7, '7') 
                self.config(image = photoimageFB, command = lambda: self.open_facebook())

        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0, rely = 0.97, relwidth = 1, relheight = 0.03)

        def get_button(self):
            self.YoutubeButton(self, relief = FLAT)
            self.FacebookButton(self, relief = FLAT)

    class EditButton(Button):
        def __init__(self, root, *args, **kwargs):
            Button.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.5, rely = 0.88, relwidth = 0.2, relheight = 0.05, anchor = 'n')
            highlight_button(self, '#41a38c', '#347d6c')


    class CheckButton(Button):
        def __init__(self, root, *args, **kwargs):
            Button.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.5, rely = 0.88, relwidth = 0.2, relheight = 0.05, anchor = 'n')
            highlight_button(self, '#30e651', '#39c459')
    

    class Scoreboard(Toplevel):
        class TitleFrame(Frame):
            def __init__(self, root, *args, **kwargs):
                Frame.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.01, rely = 0.01, relwidth = 0.97, relheight = 0.2)
                Lesson = Label(self, text = 'Lesson 1 : GETTING STARTED', bg = '#6292bf', fg = 'white', font = ('Arial Bold',10))
                Lesson.place(relx = 0, rely = 0, relwidth = 0.97)

                Content = Label(self, text =' Bài tập với lệnh print', bg = '#addcf0', fg = 'white', font = ('Arial Bold',10))
                Content.place(relx = 0.03, rely = 0.2)

        class ContentFrame(Frame):
            def __init__(self, root, *args, **kwargs):
                Frame.__init__(self, root, *args, **kwargs)
                self.place(relx = 0.01, rely = 0.1, relwidth = 0.98, relheight = 0.8)
                Content = Label(self, text ='Bài tập 1', bg = '#88d6f7', fg = '#00344a', font = ('Arial Bold',10))
                Content.place(relx = 0.03, rely = 0.18, relwidth = 0.95)    
                
        def __init__(self):
            Toplevel.__init__(self)
            self.title('Kết quả bài làm')
            self.geometry('700x500+250+100')
            self.resizable(0,0)
            MarkBG = Canvas(self, bg = '#6292bf', width = 800, height = 600,borderwidth=0, highlightthickness=0)
            MarkBG.pack()
            self.TitleFrame(MarkBG, bg = '#6292bf')
            self.ContentFrame(MarkBG)

    class Tasks_frame(Frame):
        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.4)
            Sb = Scrollbar(self)
            text = Text(self, height= 50, width=100, yscrollcommand= Sb.set, font=("Arial", 12), wrap=WORD,state= DISABLED)
            Sb.config(command= text.yview)
            Sb.pack(side = RIGHT, fill = Y)
            text.pack(side= LEFT, fill= BOTH, expand= True)

            with open("Text.txt", "r",encoding = 'utf8') as f:
                lines = f.readlines()
                for line in lines:
                    Tickbox = Checkbutton(self, activebackground= '#43e64b', bg= 'white', text= line, justify= LEFT, wraplength= 230)
                    text.window_create(END, window= Tickbox)
                    text.insert(END, "\n")


    class Tutorial_Frame(Frame):
        def __init__(self, root, *args, **kwargs):
            Frame.__init__(self, root, *args, **kwargs)
            self.place(relx = 0.1, rely = 0.55, relwidth = 0.8, relheight = 0.3)
            Sb = Scrollbar(self)
            text = Text(self, height= 50, width=100, yscrollcommand= Sb.set, font= ("Arial", 12), wrap= WORD)
            Sb.config(command= text.yview)
            Sb.pack(side = RIGHT, fill = Y)
            text.pack(side= LEFT, fill= BOTH, expand= True) 
            with open("text2.txt", "r", encoding = 'utf8') as f:
                text.insert(END, f.read())
            text.config(state= DISABLED)


    def __init__(self, role):
        self.role = role
    # Command on Button---------------

    def open_vscode(self):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        vs_window = gw.getWindowsWithTitle("Visual Studio Code")[0]
        vs_window.moveTo(0, 0)
        
    def Main(self):
        #---------------
        
        root = Tk()
        root.resizable(0,0)
        root.title('Pylearn')
        root.iconbitmap('icons/logo.ico')
        root.wm_attributes("-topmost", 1)
        root.geometry('350x700+1010+0')
        MainWindow = GradientFrame(root,[350,700],colors = ("#00ffa9","#0d4dff"))
        MainWindow.pack()
        
        # self.open_vscode()

        # Button---------------

        #----------------------
        # self.SocialFrame(MainWindow).get_button()
        
        #---------------
        
        if self.role.lower() == 'teacher':
            import frame_edit
            self.EditButton(MainWindow, bg = '#347d6c', text = 'Sửa đổi', fg = 'white', font = ('Arial Bold',10), command = lambda: frame_edit.EditWindow())
        elif self.role.lower() == 'student':
            def destroyMain():
                if messagebox.askokcancel("Thông báo", "Xác nhận Kết thúc bài làm? \n(Chú ý không thể chỉnh sửa)"):
                    MainWindow.destroy()
                    MainWindow_new = GradientFrame(root,[350,700],colors = ("#00ffa9","#0d4dff"))
                    MainWindow_new.pack()
                    Label(MainWindow_new,text = ' Bạn đã nộp bài.', font = ('Arial Bold',20)).place(relx = 0.5, rely = 0.5, anchor = 'n')
                    self.Scoreboard()

            self.CheckButton(MainWindow, bg = '#39c459', text = 'Kiểm tra', fg = 'white', font = ('Arial Bold',10), command = lambda: destroyMain())


        self.Tasks_frame(MainWindow)        
        self.Tutorial_Frame(MainWindow)

        # def on_closing():
        #     if messagebox.askokcancel("Thông báo", "Xác nhận đóng chương trình?"):
        #         root.destroy()
        #         os.system("TASKKILL /F /IM Code.exe")
        # root.protocol("WM_DELETE_WINDOW", on_closing)

        # root.wait_window()
        root.mainloop()
    