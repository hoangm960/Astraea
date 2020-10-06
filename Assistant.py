import time
from tkinter import (Button, Canvas, Entry, Label, OptionMenu, PhotoImage,
                     StringVar, Tk, messagebox)
from tkinter.constants import FLAT
#----------------------------------------------------------------
#SignBox

def sign():
    SignRoot = Tk()
    SignRoot.resizable(0,0)
    SignRoot.title('Cửa sổ đăng nhập - Pylearn')
    SignRoot.geometry('750x500+250+100')
    SignInBox = Canvas(SignRoot, width = 750, height = 500, bg = 'lightblue')
    Textbox = Label(SignInBox, text = 'ĐĂNG KÝ TÀI KHOẢN', bg = 'lightblue', fg = 'blue', font = ('Arial Bold',20))
    Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
    Name = Label(SignInBox, text = 'Tên đăng nhập *:', fg = 'black', bg = 'lightblue', font = str(50))
    Name.place(relx = 0.25, rely = 0.25)
    Nameentry = Entry(SignInBox, font = str(40))
    Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
    Name = Label(SignInBox, text = 'Mật khẩu*:', fg = 'black', bg = 'lightblue', font = str(50))
    Name.place(relx = 0.25, rely = 0.4)
    Passentry = Entry(SignInBox, font = str(40))
    Passentry.place(relx = 0.5, rely=0.48, relwidth = 0.45, relheight = 0.08, anchor = 'n')
    SignInBox.pack()
    def saves():
        again = True
        with open(r'data/User.txt','w') as f:
            newname = Nameentry.get()
            password = Passentry.get() 
            error =  Label(SignInBox)
            if newname == '':
                error = Label(SignInBox, text = "Yêu cầu nhập Tên", bg = 'lightblue', fg = 'red', font = str(30))
                error.place(relx = 0.4, rely = 0.25, relwidth = 0.45)
                again = False
            if password == '':  
                error = Label(SignInBox, text = "Yêu cầu nhập password", bg = 'lightblue', fg = 'red', font = str(30))
                error.place(relx = 0.4, rely = 0.4, relwidth = 0.45)
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
                if again == True:
                    f.write(newname)
                    password = '\n' + password
                    f.write(password)
                    SignInBox.destroy()
                    complete = Label(SignRoot, text = 'Đăng ký đã hoàn thành.', bg = 'white', fg = 'blue', font = ('Arial Bold',20))
                    complete.place(relx = 0.5, rely = 0.4, anchor = 'n')
                    SignRoot.destroy()
                    f.close()
    SaveButton = Button(SignInBox, text = 'Đăng ký', activebackground = 'lightgreen', command = lambda: saves(), relief = FLAT)
    SaveButton.place(relx = 0.5, rely = 0.6, relwidth = 0.15, relheight = 0.08, anchor = 'n')
    SignRoot.wait_window()
# --------------------------------------

def main():
    #------Root
    with open('data/User.txt','r') as f:
        check = f.read()
        if check == '':
            sign()
        f.close()
    with open('data/User.txt','r') as f:
        User = ['','']
        User[0] = f.readline().replace('\n','')
        User[1] = f.readline().replace('\n','')
        if User[0] == '':
            messagebox.askquestion('Thông báo', 'Chưa hoàn tất nhập. Chắc chắn thoát?')
        f.close()
