import tkinter as tk

def on_enter(e):
    myButton['background'] = '#00ff45'

def on_leave(e,myButton):
    myButton['background'] = '#32a852'

root = tk.Tk()
myButton = tk.Button(root,text="Click Me", bg='#32a852')
myButton.grid()


myButton.bind("<Enter>", on_enter)
myButton.bind("<Leave>", on_leave)

root.mainloop()