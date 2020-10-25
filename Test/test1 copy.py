from tkinter import *

root = Tk()
text = Text(root)
text.place(relwidth = 0.5, relheight = 0.1)
Button(root, command = print(text.get())).place(relx =0.5, rely = 0.5, anchor = 'n', relwidth = 0.1, relheight = 0.07)
root.mainloop()
root.wait_window()