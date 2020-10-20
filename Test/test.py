import tkinter

DIM = 100

root = tkinter.Tk()
frame = tkinter.Frame(root)

circle = tkinter.Canvas(frame)
circle.create_oval(5, 5, DIM-5, DIM-5, fill="red")

frame.grid()
circle.grid(row=1, column=1)

##################################
def click(event):
    root.quit()

circle.bind("<Button-1>", click)
##################################

root.mainloop()