from tkinter import *
import Login 
from gui import GradientFrame
from PIL import Image, ImageTk
from tkinter import messagebox

def EditWindow():
    tk = Toplevel()    
    tk.title('Cửa sổ chỉnh sửa')
    tk.resizable(0,0)
    tk.iconbitmap('icons/logo.ico')
    ContentLesson = ''
    ContentNum = 1
    EditCanvas = Canvas(tk, bg = '#6292bf', width = 800, height = 600,borderwidth=0, highlightthickness=0)
    EditCanvas.pack()
    EditFrame = GradientFrame(EditCanvas,[800,600],colors = ("#7df5db","#ffdc42"),direction= 2,borderwidth=0, highlightthickness=0)
    EditFrame.pack()
        
    def EditWindow():
        Login.destroy(EditFrame)
        NameLesson = Label(EditFrame, text = 'Tên bài tập:', fg = 'blue', compound = CENTER, font = ('Arial Bold',15), bd = -2)
        NameLesson.place(relx = 0.15, rely = 0.3)
        Lessonentry = Entry(EditFrame, justify = CENTER, font = str(40))
        Lessonentry.place(relx = 0.55, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        Lessonentry.insert(0,ContentLesson)
        NumFrame = Label(EditFrame, text = 'Số bài tập:', fg = 'blue', compound = CENTER, font = ('Arial Bold',15), bd = -2)
        NumFrame.place(relx = 0.15, rely = 0.5)
        Content = Entry(EditFrame, justify = CENTER, font = str(40))
        Content.place(relx = 0.55, rely=0.5, relwidth = 0.25, relheight = 0.08, anchor = 'n')
        Content.insert(0,ContentNum)
        ButtonNext = Button(EditFrame, text = 'Tiếp tục', fg = 'blue', bg = 'white', command = lambda: check())
        ButtonNext.place(relx = 0.65, rely = 0.8, relwidth = 0.23, relheight = 0.1)
    # def create_config_canvas():    
    #     ConfigCanvas = self.MainCanvas(self, bg = '#6292bf', width = 800, height = 600)
    #     ConfigCanvas.configure(scrollregion= ConfigCanvas.bbox("all"))
    #     ConfigCanvas.create_frames(self.ContentNum)
        def create_config_canvas(cannvas):
            frameLesson = Frame(cannvas)
            frameLesson.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.1)
            FrameLesson = GradientFrame(frameLesson,[800,60],colors = ("#00ffa9","#0d4dff"),direction= 2,borderwidth=0, highlightthickness=0)
            FrameLesson.pack()
            Login.set('icons/logo.png', FrameLesson, 50,50, 0.05,0.1)
            label = Label(FrameLesson, text = ContentLesson, fg = 'purple', bg = 'white', font = ('Arial Bold', 13)) 
            label.place(relx = 0.2, rely = 0.25, relwidth = 0.6, relheight = 0.5)
            def TurnBack():
                if messagebox.askokcancel('Thông báo','Hủy các thiết lập hiện tại?'):
                    EditWindow()
            TurnbackButton = Button(FrameLesson, text = 'Trở lại', command = lambda: TurnBack(), fg = 'blue', bg = 'white', relief = FLAT)
            TurnbackButton.place(relx = 0.85, rely = 0.25, relwidth = 0.1, relheight = 0.4)
            height = 0
            for _ in range(ContentNum):
                height += 0.25
                frame = Frame(EditFrame, bg = 'white')
                frame.place(relx = 0.1, rely = height, relwidth = 0.6, relheight = 0.15)   
        def check():
            global ContentLesson
            global ContentNum
            try:
                ContentNum = int(Content.get())
                ContentLesson = str(Lessonentry.get())
                if ContentNum < 0:
                    raise ValueError
                if ContentLesson == '':
                    ContentLesson = 'No named'
                Login.destroy(EditFrame)
                create_config_canvas(EditFrame)
            except ValueError:
                Error = Label(EditFrame, text = 'Số liệu không phù hợp', fg = 'red', font = ('Arial Bold',10), bg = 'white')
                Error.place(relx = 0.5, rely = 0.72, anchor = 'n')
    EditWindow()