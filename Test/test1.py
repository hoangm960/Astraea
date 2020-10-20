from tkinter import *
from PIL import ImageTk

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
        SignInBoxs  = Canvas(SignRoot, width = 750, height = 500)
        SignInBoxs.pack(expand = YES, fill = BOTH)
        image = ImageTk.PhotoImage(file = r"icons/hello.png")
        SignInBoxs.create_image(0,0, image = image, anchor = NW)
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
        
        # checked = BooleanVar()
        # AutosaveButton = Checkbutton(SignInBoxs, background= 'lightblue', text= 'Lưu mật khẩu?', variable= checked, onvalue= True, offvalue= False)
        # AutosaveButton.place(relx = 0.65, rely = 0.72)
        
        # with open('data/Autosave.txt','r') as f:
        #     textname = f.read()
        #     if textname != '':
        #         Nameentry.insert(0,textname)
        #         textpass = dataAccount[textname]
        #         Passentry.insert(0,textpass)
        #         AutosaveButton.select()
        #     f.close()

        SignInBoxs.pack()
        SignRoot.wait_window()
    DN()
main()