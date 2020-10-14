import tkinter as tk
root = tk.Tk()
readOnlyText = tk.Text(root)
readOnlyText.insert(1.0,"ABCDEF")
readOnlyText.configure(state='disabled')
readOnlyText.pack()

root.mainloop()