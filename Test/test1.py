from tkinter import Tk, Checkbutton, DISABLED
root = Tk()
check = Checkbutton(text="Click Me", state=DISABLED)
check.grid()
root.mainloop()