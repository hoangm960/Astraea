import os
import webbrowser
from tkinter import (Button, Canvas, Checkbutton, Entry, Frame, Label, Listbox, PhotoImage,
                      Scrollbar, Text, Tk, messagebox)
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

from tkinter import Canvas
from tkinter.constants import *

from PIL import Image, ImageDraw, ImageTk

basestring = str

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class GradientFrame(Canvas):

    def __init__(self, master, from_color, to_color, width=None, height=None, orient=HORIZONTAL, steps=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        if steps is None:
            if orient == HORIZONTAL:
                steps = height
            else:
                steps = width

        if isinstance(from_color, basestring):
            from_color = hex2rgb(from_color)
            
        if isinstance(to_color, basestring):
            to_color = hex2rgb(to_color)

        r,g,b = from_color
        dr = float(to_color[0] - r)/steps
        dg = float(to_color[1] - g)/steps
        db = float(to_color[2] - b)/steps

        if orient == HORIZONTAL:
            if height is None:
                raise ValueError("height can not be None")
            
            self.configure(height=height)
            
            if width is not None:
                self.configure(width=width)

            img_height = height
            img_width = self.winfo_screenwidth()

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                y0 = int(float(img_height * i)/steps)
                y1 = int(float(img_height * (i+1))/steps)

                draw.rectangle((0, y0, img_width, y1), fill=(int(r),int(g),int(b)))
        else:
            if width is None:
                raise ValueError("width can not be None")
            self.configure(width=width)
            
            if height is not None:
                self.configure(height=height)

            img_height = self.winfo_screenheight()
            img_width = width
            
            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                x0 = int(float(img_width * i)/steps)
                x1 = int(float(img_width * (i+1))/steps)

                draw.rectangle((x0, 0, x1, img_height), fill=(int(r),int(g),int(b)))
        
        self._gradient_photoimage = ImageTk.PhotoImage(image)

        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)

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
    
    class EditBoard():
        class EditTk(Tk):
            class TitleFrame(Frame):
                def __init__(self, root, *args, **kwargs):
                    Frame.__init__(self, root, *args, **kwargs)
                    self.place(relx = 0.01, rely = 0.05, relwidth = 0.98, relheight = 0.3)
                    Content = Label(self, text =' Số bài tập', bg = '#addcf0', fg = 'white', font = ('Arial Bold',10))
                    Content.place(relx = 0.5,rely = 0, relheight = 0.25, anchor = 'n')

            class NumFrame(Frame):
                def __init__(self, root, *args, **kwargs):
                    Frame.__init__(self, root, *args, **kwargs)
                    self.place(relx = 0.01, rely = 0.1, relwidth = 0.98, relheight = 0.4)
                    Content = Entry(self, font = ('Arial Bold',10))
                    Content.place(relx = 0.5, rely = 0.3, relwidth = 0.5, relheight = 0.3, anchor = 'n')    
                    OKButton = Button(self, text = 'OK', font = ('Arial bold',10), relief = FLAT, command = lambda: self.check(Content))
                    highlight_button(OKButton, '#2efff8', 'white')
                    OKButton.place(relx = 0.5 , rely = 0.83, anchor = 'n')
                def check(self, Content):
                    try:
                        self.ContentNum = int(Content.get())
                    except:
                        Error = Label(self, text = 'Số liệu không phù hợp', fg = 'red', font = ('Arial Bold',10), bg = '#6292bf')
                        Error.place(relx = 0.5, rely = 0.72, anchor = 'n')
                    

            def __init__(self, *args, **kwargs):
                Tk.__init__(self, *args, **kwargs)
                self.title('Cửa sổ chỉnh sửa')
                self.geometry('700x500+250+100')
                self.resizable(0,0)
                self.wm_attributes("-topmost", 1)
                self.attributes('-toolwindow',1)
                self.get_canvas()
                self.mainloop()

            def get_canvas(self):
                MarkBG = Canvas(self, bg = '#6292bf', width = 800, height = 600)
                MarkBG.pack()
                self.TitleFrame(MarkBG,bg = '#6292bf')
                self.NumFrame(MarkBG, bg = '#6292bf')

        class ConfigTk(Tk):
            class ContentFrame(Frame):
                def __init__(self, root, y, *args, **kwargs):
                    Frame.__init__(self, root, *args, **kwargs)
                    self.place(relx = 0, y = 0, anchor = 'n')
                    # Box1 = Entry(self)
                    # Box1.place(x =  20, y = 0, height = 40)
                    # Box2 = Entry(self)
                    # Box2.place(x = 50, y = 0, height = 40)
                    # Box3 = Entry(self)
                    # Box3.place(x = 80, y = 0, height = 40)
                    # Box4 = Entry(self)
                    # Box4.place(x = 110, y = 0, height = 40)
                    # Box5 = Entry(self)
                    # Box5.place(x = 140, y = 0, height = 40)   
            
            def __init__(self, *args, **kwargs):
                Tk.__init__(self, *args, **kwargs)
                self.title('Cửa sổ chỉnh sửa')
                self.geometry('700x500+250+100')
                self.resizable(0,0)
                self.wm_attributes("-topmost", 1)
                self.attributes('-toolwindow',1)
                self.get_canvas()
                self.mainloop()

            def get_canvas(self):
                ConfigCanvas = Canvas(self, bg = '#6292bf', width = 800, height = 600)
                ConfigCanvas.pack()
                self.ContentFrame(ConfigCanvas, 0)

        def __init__(self):
            self.EditTk()
            self.ConfigTk()
            
                    
    class Scoreboard(Tk):
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
            Tk.__init__(self)
            self.title('Kết quả bài làm')
            self.geometry('700x500+250+100')
            self.resizable(0,0)
            self.wm_attributes("-topmost", 1)
            self.attributes('-toolwindow',1)

        def get_canvas(self):
            MarkBG = Canvas(self, bg = '#6292bf', width = 800, height = 600)
            MarkBG.pack()
            self.TitleFrame(MarkBG, bg = '#6292bf')
            self.ContentFrame(MarkBG)

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
        MainWindow = GradientFrame(root, from_color="#00ffa9", to_color="#0d4dff", height=1000)
        MainWindow.pack()
        root.attributes('-toolwindow',1)
        
        # self.open_vscode()

        # Button---------------

        #----------------------
        # self.SocialFrame(MainWindow).get_button()
        
        #---------------
        
        if self.role.lower() == 'teacher':
            self.EditButton(MainWindow, bg = '#347d6c', text = 'Sửa đổi', fg = 'white', font = ('Arial Bold',10),command = lambda: self.EditBoard())
        elif self.role.lower() == 'student':
            def EditFunction():
                self.Scoreboard().get_canvas()
                root.destroy()
                
            self.CheckButton(MainWindow, bg = '#39c459', text = 'Kiểm tra', fg = 'white', font = ('Arial Bold',10), command = lambda: EditFunction())

        self.Tasks_frame(MainWindow).get_frame()
        
        self.Tutorial_Frame(MainWindow).get_frame()

        # def on_closing():
        #     if messagebox.askokcancel("Thông báo", "Xác nhận đóng chương trình?"):
        #         root.destroy()
        #         os.system("TASKKILL /F /IM Code.exe")
        # root.protocol("WM_DELETE_WINDOW", on_closing)

        # root.wait_window()
        root.mainloop()
    