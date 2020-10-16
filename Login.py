from tkinter import BooleanVar, Button, Canvas, Entry, IntVar, Label, PhotoImage, Tk, messagebox, Checkbutton
from tkinter.constants import ACTIVE, DISABLED, FLAT
from tkinter.font import NORMAL
from gui import GUI
#----------------------------------------------------------------
#SignBox
def enter_leave(button_name, colour1, colour2):
    def on_enter(e):
        button_name['background'] = colour1
    def on_leave(e):
        button_name['background'] = colour2
    button_name.bind("<Enter>", on_enter)
    button_name.bind("<Leave>", on_leave)
def main():
    SignRoot = Tk()
    SignRoot.resizable(0,0)
    SignRoot.wm_attributes("-topmost",1)
    SignRoot.title('Cửa sổ đăng nhập - Pylearn')
    SignRoot.iconbitmap('icons/logo.ico')
    SignRoot.geometry('750x500+250+100')
    def DN():
        dataAccount = dict()
        with open('data/User.txt','r') as f:
            while True:
                name = f.readline().replace('\n','')
                dataAccount[name] = f.readline().replace('\n','')
                if name == '':
                    break
        SignInBoxs  = Canvas(SignRoot, width = 750, height = 500, bg = 'lightblue')
        Textbox = Label(SignInBoxs, text = 'ĐĂNG NHẬP TÀI KHOẢN', bg = 'lightblue', fg = 'blue', font = ('Arial Bold',20))
        Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
        Name = Label(SignInBoxs, text = 'Tên đăng nhập:', fg = 'black', bg = 'lightblue', font = str(50))
        Name.place(relx = 0.25, rely = 0.25)
        Nameentry = Entry(SignInBoxs, font = str(40))
        Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        Name = Label(SignInBoxs, text = 'Mật khẩu:', fg = 'black', bg = 'lightblue', font = str(50))
        Name.place(relx = 0.25, rely = 0.4)
        Passentry = Entry(SignInBoxs, font = str(40), show = '●')
        Passentry.place(relx = 0.5, rely=0.45, relwidth = 0.45, relheight = 0.08, anchor = 'n')
        with open('data/Autosave.txt','r') as f:
            textname = f.read()
            if textname != '':
                Nameentry.insert(0,textname)
                textpass = dataAccount[textname]
                Passentry.insert(0,textpass)
            f.close()
        PlayUp = PhotoImage(file=r'icons/tick.png')
        PlayUp = PlayUp.subsample(2,'2')
        PlayDown = PhotoImage(file=r'icons/untick.png')
        PlayDown = PlayDown.subsample(2,'2')
        def change():
            global changenumber
            if changenumber == 1:
                changenumber = 0
                TickButton.config(image = PlayUp)
            else:
                changenumber = 1
                TickButton.config(image = PlayDown)
        TickLabel = Label(SignInBoxs, text = 'Lưu mật khẩu?', bg = 'lightblue')
        TickLabel.place(relx = 0.52, rely = 0.73 )
        TickButton = Button(SignInBoxs, image = PlayDown, command = lambda: change(), relief = FLAT)
        TickButton.place(relx = 0.65, rely = 0.72, relheight = 0.05, relwidth = 0.05)
        SignInBoxs.pack()
        """"""""""""""""""" Chuyển trang đăng ký """""""""""""""""""""""""
        def DK():
            SignInBoxs. destroy()
            SignInBox = Canvas(SignRoot, width = 750, height = 500, bg = 'lightblue')
            Textbox = Label(SignInBox, text = 'ĐĂNG KÝ TÀI KHOẢN', bg = 'lightblue', fg = 'blue', font = ('Arial Bold', 20))
            Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
            Name = Label(SignInBox, text = 'Tên tài khoản*:', fg = 'black', bg = 'lightblue', font = str(50))
            Name.place(relx = 0.25, rely = 0.25)
            Nameentry = Entry(SignInBox, font = str(40))
            Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
            Name = Label(SignInBox, text = 'Mật khẩu*:', fg = 'black', bg = 'lightblue', font = str(50))
            Name.place(relx = 0.25, rely = 0.4)
            Passentry = Entry(SignInBox, font = str(40), show = '●')
            Passentry.place(relx = 0.5, rely=0.45, relwidth = 0.45, relheight = 0.08, anchor = 'n')                

            TickLabel = Label(SignInBox, text = 'Bạn là ?', bg = 'lightblue')
            TickLabel.place(relx = 0.3, rely = 0.55)
            var1 = BooleanVar()
            var2 = BooleanVar()
            def click(button, var):
                if var.get():
                    button.config(state = DISABLED)
                else:
                    button.config(state = NORMAL)
            TickButton1 = Checkbutton(SignInBox, text = 'học sinh : ', onvalue = True, offvalue = False, variable = var1, command = lambda: click(TickButton2, var1))
            TickButton1.place(relx = 0.38, rely = 0.55)
            TickButton2 = Checkbutton(SignInBox, text = 'giáo viên ', onvalue = True, offvalue = False, variable = var2, command = lambda: click(TickButton1, var2))
            TickButton2.place(relx = 0.57, rely = 0.55)
            def Quayve():
                SignInBox.destroy()
                DN()
            buttonDK = Button(SignInBox, text = 'Đã có tài khoản? Quay trở về trang đăng nhập.', fg = 'blue', command = lambda: Quayve(), relief = FLAT)
            buttonDK.place(relx = 0.5, rely = 0.8, relwidth = 0.4, relheight = 0.035, anchor = 'n')                
            SignInBox.pack()
            """ Kiểm tra thông tin đăng ký """
            def saves():
                again = True
                with open(r'data/User.txt','a+') as f:
                    newname = Nameentry.get()
                    password = Passentry.get() 
                    error =  Label(SignInBox)
                    if newname == '':
                        error = Label(SignInBox, text = "                  Yêu cầu nhập Tên             ", bg = 'lightblue', fg = 'red', font = str(30))
                        error.place(relx = 0.47, rely = 0.25)
                        again = False
                    if password == '':  
                        error = Label(SignInBox, text = "                    Yêu cầu nhập password       ", bg = 'lightblue', fg = 'red', font = str(30))
                        error.place(relx = 0.47, rely = 0.4)
                        again = False
                    else:
                        for i in newname.lower():
                            if i not in 'qwertyuiopasdfghjklzxcvbnm1234567890 ':
                                error = Label(SignInBox, text = "Yêu cầu không dấu, kí tự đặc biệt", bg = 'lightblue', fg = 'red', font = str(30))
                                error.place(relx = 0.65, rely = 0.25, anchor = 'n')
                                again = False
                        for i in password.lower():
                            if i not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                                error = Label(SignInBox, text = "Yêu cầu không chứa kí tự đặc biệt", bg = 'lightblue', fg = 'red', font = str(30))
                                error.place(relx = 0.45, rely = 0.4)
                                again = False
                        if len(password) < 3:
                            error = Label(SignInBox, text = "Mật khẩu tối thiểu 3 kí tự", bg = 'lightblue', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if len(newname)<7:
                            error = Label(SignInBox, text = "Tên tài khoản tối thiểu 7 kí tự", bg = 'lightblue', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if newname in dataAccount.keys() and newname != '':
                            error = Label(SignInBox, text = "Tên tài khoản đã tồn tại.", bg = 'lightblue', fg = 'red', font = str(30))
                            error.place(relx = 0.5, rely = 0.6, relwidth = 0.45, anchor = 'n')
                            again = False
                        if not var1.get() and not var2.get():
                            error = Label(SignInBox, text = "Chưa xác định học sinh hay giáo viên.", bg = 'lightblue', fg = 'red', font = str(30))
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
                            SignInBox.destroy()
                            complete = Label(SignRoot, text = 'Đăng ký đã hoàn thành.', bg = 'white', fg = 'blue', font = ('Arial Bold',20))
                            complete.place(relx = 0.5, rely = 0.4, anchor = 'n')
                            SaveButton = Button(SignRoot, text = 'Quay về', font = ('Arial Bold',10), activebackground = 'white', command = lambda: DN(), relief = FLAT)
                            SaveButton.place(relx = 0.5, rely = 0.6, relwidth = 0.2, relheight = 0.08, anchor = 'n')
                            f.close()
            def on_closing():
                if messagebox.askokcancel("Thông báo", "Thoát giao diện đăng nhập?"):
                    SignRoot.destroy()
            SignRoot.protocol("WM_DELETE_WINDOW", on_closing)
            SaveButton = Button(SignInBox, text = 'Đăng ký', bg = 'white', command = lambda: saves(), relief = FLAT)
            SaveButton.place(relx = 0.5, rely = 0.68, relwidth = 0.15, relheight = 0.08, anchor = 'n')
            enter_leave(SaveButton, '#00b594', 'white')
        """"""""""""""""""" Kiểm tra thông tin đăng nhập """""""""""""""""""""""""
        def check():
            if Nameentry.get() == '' or Passentry.get() == '':
                error = Label(SignInBoxs, text = "Điền đẩy đủ trường thông tin", bg = 'lightblue', fg = 'red', font = str(30))
                error.place(relx = 0.5, rely = 0.55, relwidth = 0.45, anchor = 'n')
            else:            
                checktk = False
                checkmk = False
                if Nameentry.get() in dataAccount.keys():
                    checktk = True
                    if dataAccount[Nameentry.get()] == Passentry.get():
                        checkmk = True
                    else:
                        error = Label(SignInBoxs, text = "Mật khẩu không chính xác", bg = 'lightblue', fg = 'red', font = str(30))
                        error.place(relx = 0.5, rely = 0.55, relwidth = 0.45, anchor = 'n')
                        checkmk = False
                        checktk = False
                else:
                    error = Label(SignInBoxs, text = "Tài khoản không tồn tại", bg = 'lightblue', fg = 'red', font = str(30))
                    error.place(relx = 0.5, rely = 0.55, relwidth = 0.45, anchor = 'n')
                    checkmk = False
                    checktk = False
                if checkmk == True and checktk == True:
                    global nameAccount
                    nameAccount = Nameentry.get()
                    if changenumber == 0:
                        with open('data/Autosave.txt','w') as file:
                            file.write(nameAccount)
                            file.close()
                    with open('data/HostList.txt','r') as hostf:
                        HostAccount = list()
                        while True:
                            name = hostf.readline().replace('\n','')
                            if name == '':
                                break
                            else:
                                HostAccount.append(name)
                        nameAccount = Nameentry.get()
                        if nameAccount in HostAccount:
                            SignRoot.destroy()
                            GUI("teacher").Main()
                        else:
                            SignRoot.destroy()
                            GUI("student").Main()
                        hostf.close()
                f.close()
                
        SaveButton = Button(SignInBoxs, text = 'Đăng nhập', bg = 'white', command = lambda: check(), relief = FLAT)
        SaveButton.place(relx = 0.5, rely = 0.62, relwidth = 0.15, relheight = 0.08, anchor = 'n')
        enter_leave(SaveButton,'#00b594','white')
        buttonDK = Button(SignInBoxs, text = 'Chưa có tài khoản? Đăng ký ngay', fg = 'blue', command = lambda: DK(), relief = FLAT)
        buttonDK.place(relx = 0.5, rely = 0.8, relwidth = 0.4, relheight = 0.035, anchor = 'n')
    DN()
    SignRoot.wait_window()

# --------------------------------------
changenumber = 1
change_number = False
nameAccount = ''
        
    
        
