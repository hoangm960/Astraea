from os import system
from tkinter import BooleanVar, Button, Canvas, Entry, Frame, IntVar, Label, PhotoImage, Text, Tk, messagebox, Checkbutton
from tkinter import ttk
import tkinter as tk
from tkinter.constants import ACTIVE, BOTH, CENTER, DISABLED, FLAT, NW, RAISED, SUNKEN, YES
from tkinter.font import NORMAL
from tkinter.ttk import Style
from gui import GUI
import encription

#----------------------------------------------------------------
#SignBox

def hightlight_border(obj,frame):
    obj.bind("<FocusIn>", lambda evt: frame.state(["focus"]))
    obj.bind("<FocusOut>", lambda evt: frame.state(["!focus"]))

def highlight_button(button_name, colour1, colour2):
    def on_enter(e):
        button_name['background'] = colour1
    def on_leave(e):
        button_name['background'] = colour2
    button_name.bind("<Enter>", on_enter)
    button_name.bind("<Leave>", on_leave)

def destroy(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def main():
    SignRoot = Tk()
    # SignRoot.resizable(0,0)
    SignRoot.wm_attributes("-topmost",1)
    SignRoot.title('Cửa sổ đăng nhập - Pylearn')
    SignRoot.iconbitmap('icons/logo.ico')
    # SignRoot.geometry('1980x720+0+0')
    w, h = SignRoot.winfo_screenwidth(), SignRoot.winfo_screenheight()
    SignRoot.geometry("%dx%d+0+0" % (w, h))

    img1 = tk.PhotoImage("frameFocusBorder", data="""
    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
    Ry/99NIz//oGrZpUUEAAOw==""")
    img2 = tk.PhotoImage("frameBorder", file = 'icons/trán.png')
    style = Style()
    style.element_create("RoundedFrame", "image", "frameBorder",
        ("focus", "frameFocusBorder"),border = 30,  sticky="nsew")
    style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
    SignInBoxes  = Canvas(SignRoot, width = w, height = h)
    SignInBoxes.pack(expand = True, fill = BOTH)
    image = tk.PhotoImage(file="icons/Background.png")
    SignInBoxes.create_image(0,0, image = image, anchor = 'n')
    
    SignInFrame = ttk.Frame(SignInBoxes, style= "RoundedFrame")
    SignInFrame.place(relx = 0.08, rely = 0.36, relwidth = 0.5, relheight = 0.5)
    # SignInFrame = Frame(SignInBoxes, bg = 'white')
    # SignInFrame.place(relx = 0.08, rely = 0.36, relwidth= 0.5, relheight= 0.5)
    
    ENCRIPTED_PATH = 'data/User.encrypted'
    DECRIPTED_PATH = 'data/User.txt'

    def DN():
        destroy(SignInFrame)
        encription.decript(ENCRIPTED_PATH, DECRIPTED_PATH)
        dataAccount = dict()
        with open('data/User.txt','r') as f:
            while True:
                name = f.readline().replace('\n','')
                dataAccount[name] = f.readline().replace('\n','')
                if name == '':
                    break
        encription.get_key()
        encription.encript(DECRIPTED_PATH, ENCRIPTED_PATH)
        Textbox = Label(SignInFrame, text = 'ĐĂNG NHẬP TÀI KHOẢN', compound = CENTER, fg = 'blue', font = ('Arial Bold',20), bd = -2)
        Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
        Name = Label(SignInFrame, text = 'Tên đăng nhập:', fg = 'blue', compound = CENTER, font = ('Arial Bold',10), bd = -2)
        Name.place(relx = 0.25, rely = 0.25)
        
        # TextFrame = ttk.Frame(SignInFrame, style="RoundedFrame")
        # TextFrame.place(relx = 0.5, rely = 0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        # NameBox = Text(TextFrame, borderwidth = 0, highlightthickness = 0, bg = 'white', font = str(40))
        # NameBox.pack(fill = 'both', expand = 1)
                
        Nameframe = ttk.Frame(SignInFrame, style="RoundedFrame", padding=10)
        Nameframe.place(relx = 0.5, rely = 0.3, relwidth = 0.45, relheight = 0.12, anchor = 'n')
        NameBox = tk.Entry(Nameframe, borderwidth=0, font = ('Arial Bold', 10), bg = "white", highlightthickness=0)
        NameBox.pack(fill = 'both', expand = True)
        NameBox.bind("<FocusIn>", lambda evt: Nameframe.state(["focus"]))
        NameBox.bind("<FocusOut>", lambda evt: Nameframe.state(["!focus"]))

        # Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        
        Name = Label(SignInFrame, text = 'Mật khẩu:', fg = 'blue', compound = CENTER, font = ('Arial Bold',10), bd = -2)
        Name.place(relx = 0.25, rely = 0.45)
        # Passentry = Entry(SignInFrame, font = str(40), show = '●')
        # Passentry.place(relx = 0.5, rely=0.45, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        
        Nameframe = ttk.Frame(SignInFrame, style="RoundedFrame", padding=10)
        Nameframe.place(relx = 0.5, rely = 0.5, relwidth = 0.45, relheight = 0.12, anchor = 'n')
        Passentry = tk.Entry(Nameframe, borderwidth=0, show = '●', font = ('Arial Bold', 10), bg = "white", highlightthickness=0)
        Passentry.pack(fill = 'both', expand = True)
        Passentry.bind("<FocusIn>", lambda evt: Nameframe.state(["focus"]))
        Passentry.bind("<FocusOut>", lambda evt: Nameframe.state(["!focus"]))
        
        checked = BooleanVar()
        AutosaveButton = Checkbutton(SignInFrame, background= 'white', text= 'Lưu mật khẩu?', variable= checked, onvalue= True, offvalue= False)
        AutosaveButton.place(relx = 0.65, rely = 0.72)
        
        with open('data/Autosave.txt','r') as f:
            textname = f.read()
            if textname != '':
                NameBox.insert(0,textname)
                textpass = dataAccount[textname]
                Passentry.insert(0,textpass)
                AutosaveButton.select()
            f.close()

        SaveButton = Button(SignInFrame, text = 'Đăng nhập', bg = 'white', command = lambda: check(), relief = FLAT)
        SaveButton.place(relx = 0.5, rely = 0.7, relwidth = 0.15, relheight = 0.08, anchor = 'n')
        highlight_button(SaveButton,'#00b594','white')
        buttonDK = Button(SignInFrame, text = 'Chưa có tài khoản? Đăng ký ngay', fg = 'blue', command = lambda: DK(), relief = FLAT)
        buttonDK.place(relx = 0.5, rely = 0.85, relwidth = 0.4, relheight = 0.035, anchor = 'n')
        """"""""""""""""""" Chuyển trang đăng ký """""""""""""""""""""""""
        def DK():
            destroy(SignInFrame)
            Textbox = Label(SignInFrame, text = 'ĐĂNG KÝ TÀI KHOẢN', compound = CENTER, fg = 'Purple', font = ('Arial Bold', 20), bd = -2)
            Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
            Name = Label(SignInFrame, text = 'Tên tài khoản*:', fg = 'purple', compound = CENTER, font = ('Arial Bold',10), bd = -2)
            Name.place(relx = 0.25, rely = 0.25)
            Nameentry = Entry(SignInFrame, font = str(40))
            Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
            Name = Label(SignInFrame, text = 'Mật khẩu*:', fg = 'purple', compound = CENTER,font = ('Arial Bold',10), bd = -2)
            Name.place(relx = 0.25, rely = 0.4)
            Passentry = Entry(SignInFrame, font = str(40), show = '●')
            Passentry.place(relx = 0.5, rely=0.45, relwidth = 0.45, relheight = 0.08, anchor = 'n')                

            TickLabel = Label(SignInFrame, text = 'Bạn là ', bg = 'white')
            TickLabel.place(relx = 0.3, rely = 0.55)
            def click(button, var):
                if var.get():
                    button.config(state = DISABLED)
                else:
                    button.config(state = NORMAL)
            var1 = BooleanVar()
            var2 = BooleanVar()
            TickButton1 = Checkbutton(SignInFrame, text = 'học sinh ', onvalue = True, offvalue = False, variable = var1, command = lambda: click(TickButton2, var1))
            TickButton1.place(relx = 0.38, rely = 0.55)
            TickButton2 = Checkbutton(SignInFrame, text = 'giáo viên ', onvalue = True, offvalue = False, variable = var2, command = lambda: click(TickButton1, var2))
            TickButton2.place(relx = 0.57, rely = 0.55)
            buttonDK = Button(SignInFrame, text = 'Đã có tài khoản? Quay trở về trang đăng nhập.', fg = 'blue', command = lambda: DN(), relief = FLAT)
            buttonDK.place(relx = 0.5, rely = 0.8, relwidth = 0.4, relheight = 0.035, anchor = 'n')                
            """ Kiểm tra thông tin đăng ký """
            def saves():
                again = True
                encription.decript(ENCRIPTED_PATH, DECRIPTED_PATH)
                with open(r'data/User.txt','a+') as f:
                    newname = Nameentry.get()
                    password = Passentry.get() 
                    error =  Label(SignInFrame)
                    if newname == '':
                        error = Label(SignInFrame, text = "                  Yêu cầu nhập Tên             ", bg = 'white', fg = 'red', font = str(30))
                        error.place(relx = 0.47, rely = 0.25)
                        again = False
                    if password == '':  
                        error = Label(SignInFrame, text = "                    Yêu cầu nhập password         ", bg = 'white', fg = 'red', font = str(30))
                        error.place(relx = 0.47, rely = 0.4)
                        again = False
                    else:
                        for i in newname.lower():
                            if i not in 'qwertyuiopasdfghjklzxcvbnm1234567890 ':
                                error = Label(SignInFrame, text = "Yêu cầu không dấu, kí tự đặc biệt", bg = 'white', fg = 'red', font = str(30))
                                error.place(relx = 0.65, rely = 0.25, anchor = 'n')
                                again = False
                        for i in password.lower():
                            if i not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                                error = Label(SignInFrame, text = "Yêu cầu không chứa kí tự đặc biệt", bg = 'white', fg = 'red', font = str(30))
                                error.place(relx = 0.45, rely = 0.4)
                                again = False
                        if len(password) < 3:
                            error = Label(SignInFrame, text = "Mật khẩu tối thiểu 3 kí tự", bg = 'white', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if len(newname)<7:
                            error = Label(SignInFrame, text = "Tên tài khoản tối thiểu 7 kí tự", bg = 'white', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if newname in dataAccount.keys() and newname != '':
                            error = Label(SignInFrame, text = "Tên tài khoản đã tồn tại.", bg = 'white', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if not var1.get() and not var2.get():
                            error = Label(SignInFrame, text = "Chưa xác định học sinh hay giáo viên.", bg = 'white', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if again == True:
                            newname = newname + '\n'
                            f.write(newname)
                            if var1.get() == False:
                                with open('data/HostList.txt','a+') as file_host:
                                    file_host.write(newname)
                                    file_host.close()
                            password = password + '\n'
                            f.write(password)
                            destroy(SignInFrame)
                            complete = Label(SignInFrame, text = 'Đăng ký đã hoàn thành.', bg = 'white', fg = 'blue', font = ('Arial Bold',20))
                            complete.place(relx = 0.5, rely = 0.4, anchor = 'n')
                            SaveButton = Button(SignInFrame, text = 'Quay về', font = ('Arial Bold',10), activebackground = 'white', command = lambda: DN(), relief = FLAT)
                            SaveButton.place(relx = 0.5, rely = 0.6, relwidth = 0.2, relheight = 0.08, anchor = 'n')
                encription.get_key()
                encription.encript(DECRIPTED_PATH, ENCRIPTED_PATH)

            def on_closing():
                if messagebox.askokcancel("Thông báo", "Thoát giao diện đăng nhập?"):
                    SignRoot.destroy()
            SignRoot.protocol("WM_DELETE_WINDOW", on_closing)
            SaveButton = Button(SignInFrame, text = 'Đăng ký', bg = 'white', command = lambda: saves(), relief = FLAT)
            SaveButton.place(relx = 0.5, rely = 0.68, relwidth = 0.15, relheight = 0.08, anchor = 'n')
            highlight_button(SaveButton, '#00b594', 'white')
            SignRoot.wait_window()
        """"""""""""""""""" Kiểm tra thông tin đăng nhập """""""""""""""""""""""""
        def check():
            if NameBox.get() == '' or Passentry.get() == '':
                error = Label(SignInFrame, text = "Điền đẩy đủ trường thông tin", bg = 'white', fg = 'red', font = str(30))
                error.place(relx = 0.5, rely = 0.65, relwidth = 0.45, anchor = 'n')
            else:            
                checktk = False
                checkmk = False
                if NameBox.get() in dataAccount.keys():
                    checktk = True
                    if dataAccount[NameBox.get()] == Passentry.get():
                        checkmk = True
                    else:
                        error = Label(SignInFrame, text = "Mật khẩu không chính xác", bg = 'white', fg = 'red', font = str(30))
                        error.place(relx = 0.5, rely = 0.65, relwidth = 0.45, anchor = 'n')
                        checkmk = False
                        checktk = False
                else:
                    error = Label(SignInFrame, text = "Tài khoản không tồn tại", bg = 'white', fg = 'red', font = str(30))
                    error.place(relx = 0.5, rely = 0.65, relwidth = 0.45, anchor = 'n')
                    checkmk = False
                    checktk = False
                if checkmk == True and checktk == True:
                    nameAccount = NameBox.get()
                    if checked.get() == True:
                        with open('data/Autosave.txt','w') as file:
                            file.write(nameAccount)
                            file.close()
                    else:
                        with open('data/Autosave.txt','w') as file:
                            file.write('')
                            file.close()

                    with open('data/HostList.txt','r') as hostf:
                        HostAccount = list()
                        while True:
                            name = hostf.readline().replace('\n','')
                            if name == '':
                                break
                            else:
                                HostAccount.append(name)
                        nameAccount = NameBox.get()
                        if nameAccount in HostAccount:
                            SignRoot.destroy()
                            GUI("teacher").Main()
                        else:
                            SignRoot.destroy()
                            GUI("student").Main()
                        hostf.close()
                f.close()
                
        SignRoot.wait_window()
    DN()
    

        
        
