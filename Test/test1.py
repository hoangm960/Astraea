from tkinter import *

master = Tk()
master.resizable(False, False)
master.geometry('430x480+50+50')
master.title("Ping Check")
master.config(bg="white")

layer = PhotoImage(file = r"icons/VScode.png")
topFrame = Label(text="Ping Checker", image=layer, fg="black", font="Bahnschrift 14")
topFrame.place(x=11,y=10)
master.wait_window()