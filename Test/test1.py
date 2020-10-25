from tkinter import *
from PIL import Image


root = Tk()
root.title("Game")


frame = Frame(root)
frame.pack()


canvas = Canvas(frame, bg="black", width=700, height=400)
canvas.pack()


background = PhotoImage(file="icons/bg1/vio.png")
canvas.create_image(350,200,image=background)

character = PhotoImage(file="icons/trán.png")
canvas.create_image(30,30,image=character)

root.mainloop()