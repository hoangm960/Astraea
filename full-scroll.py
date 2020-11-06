import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        

        self.canvas.bind_all("<Configure>", self.onFrameConfigure)
        
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    
root = tk.Tk()
frame = ScrollableFrame(root)
for i in range(50):
    ttk.Label(frame.scrollable_frame, text="Sample scrolling label").pack()
frame.place(relx= 0, rely = 0, relwidth= 1, relheight= 0.9)
root.mainloop()
