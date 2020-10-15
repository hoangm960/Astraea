import os
from tkinter import Frame, Label, Menu, Scrollbar, Text, Tk, filedialog, font
from tkinter.constants import BOTTOM, END, RIGHT, E, X, Y

root = Tk()
root.title("Pylearn Editor")
root.iconbitmap("icons/logo.ico")
root.geometry("1200x690+250+100")


def new_file():
    text.delete("1.0", END)
    root.title("New File - Pylearn Editor")
    status_bar.config(text="New File        ")


def open_file():
    text.delete("1.0", END)

    text_file = filedialog.askopenfilename(
        title="Open File",
        filetypes=(
            ("Text Files", "*.txt"),
            ("Word Document 2010-2016", "*.docx"),
            ("Word Document 2003", "*.doc"),
            ("All Files", "*.*"),
        ),
    )

    name = text_file
    status_bar.config(text=f"{name}        ")
    name = os.path.basename(name)
    root.title(f"{name} - Pylearn Editor")

    text_file = open(text_file, "r")
    stuff = text_file.read()

    text.insert(END, stuff)

def save_as():
	

frame = Frame(root)
frame.pack(pady=5)

text_scroll = Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)

text = Text(
    frame,
    width=97,
    height=25,
    font=("Times New Roman", 16),
    yscrollcommand=text_scroll.set,
)
text.pack()

text_scroll.config(command=text.yview)

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save")
file_menu.add_command(label="Save as", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

root.mainloop()
