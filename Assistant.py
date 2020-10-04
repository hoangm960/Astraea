
import webbrowser
from tkinter import (Button, Canvas, Entry, Label, OptionMenu, PhotoImage,
                     StringVar, Tk, messagebox)
from tkinter.constants import FLAT

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

#----------------------------------------------------------------
#SignBox
def sign():
    SignRoot = Tk()
    SignRoot.resizable(0,0)
    SignRoot.title('Account box')
    SignRoot.geometry('750x500+250+100')
    SignInBox = Canvas(SignRoot, width = 750, height = 500, bg = 'lightblue')
    Textbox = Label(SignInBox, text = 'SIGN UP YOUR NEW USER', bg = 'lightblue', fg = 'blue', font = ('Arial Bold',20))
    Textbox.place(relx = 0.5, rely = 0.1, anchor = 'n')
    Name = Label(SignInBox, text = 'Your name *:', fg = 'black', bg = 'lightblue', font = str(50))
    Name.place(relx = 0.25, rely = 0.25)
    Nameentry = Entry(SignInBox, font = str(40))
    Nameentry.place(relx = 0.5, rely=0.3, relwidth = 0.45, relheight = 0.08, anchor = 'n')
    Name = Label(SignInBox, text = 'Your facebook link: (skip to default: facebook.com)', fg = 'black', bg = 'lightblue', font = str(50))
    Name.place(relx = 0.25, rely = 0.4)
    FBentry = Entry(SignInBox, font = str(40))
    FBentry.place(relx = 0.5, rely=0.45, relwidth = 0.45, relheight = 0.08, anchor = 'n')
    Name = Label(SignInBox, text = 'Your email link: (skip to default: gmail.com)', fg = 'black', bg = 'lightblue', font = str(50))
    Name.place(relx = 0.25, rely = 0.55)
    EMentry = Entry(SignInBox, font = str(40))
    EMentry.place(relx = 0.5, rely=0.6, relwidth = 0.45, relheight = 0.08, anchor = 'n')
    Webname = StringVar(SignInBox)
    Webname.set('Choose your Webbrowser:')
    MenuOption = OptionMenu(SignInBox, Webname,"Google Chrome","Internet Explorer")
    MenuOption.place(relx = 0.5, rely = 0.7, relwidth = 0.25, relheight = 0.07, anchor = 'n')
    SignInBox.pack()
    def saves():
        again = True
        with open(r'data\User.txt','w') as f:
            newname = Nameentry.get()
            error = Label(SignInBox)
            if newname == '':
                error = Label(SignInBox, text = "You should sign up your Name", bg = 'lightblue', fg = 'red', font = str(30))
                error.place(relx = 0.4, rely = 0.25, relwidth = 0.45)  
            elif Webname.get() == 'Choose your Webbrowser:':
                error = Label(SignInBox, text = "You have to choose Webbrowser", bg = 'lightblue', fg = 'red', font = str(30))
                error.place(relx = 0.4, rely = 0.25, relwidth = 0.45)
            else:
                # for i in newname:
                #     if i not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890 ':
                #         error = Label(SignInBox, text = "Your name musn't contain any special characters", bg = 'lightblue', fg = 'red', font = str(30))
                #         error.place(relx = 0.4, rely = 0.25)
                #         again = False
                if again == True:
                    f.write(newname)
                    newlink = '\n' + FBentry.get()
                    if newlink == '\n':
                        newlink+='Facebook.com'
                    f.write(newlink)
                    newGmail = '\n' + EMentry.get()
                    if newGmail == '\n':
                        newGmail+='Gmail.com'
                    f.write(newGmail)
                    newWeb = '\n' + str(Webname.get())
                    f.write(newWeb)
                    SignInBox.destroy()
                    complete = Label(SignRoot, text = 'You have been completed.', bg = 'white', fg = 'blue', font = ('Arial Bold',20))
                    complete.place(relx = 0.5, rely = 0.4, anchor = 'n')
                    f.close()
    SaveButton = Button(SignInBox, text = 'SIGN UP', activebackground = 'lightgreen', command = lambda: saves(), relief = FLAT)
    SaveButton.place(relx = 0.5, rely = 0.8, relwidth = 0.15, relheight = 0.08, anchor = 'n')
    SignRoot.wait_window()
        
# --------------------------------------


#------Root
def main():
    f = open('data/User.txt','r')
    check = f.readline()
    User = ['', '', '', '']
    if str(check) == '':
        sign()

    User[0] = (f.readline().replace('\n',''))
    User[1] = (f.readline().replace('\n',''))
    User[2] = (f.readline().replace('\n',''))
    User[3] = (f.readline().replace('\n',''))
    if User[0] == '': 
        messagebox.showinfo('Notification','You have to complete this form.')
        exit()
    if User[3] == 'Google Chrome':
        web_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    elif User[3] == 'Internet Explorer':
        web_path = 'C:/Program Files/internet explorer/iexplore.exe %s'
    f.close()
