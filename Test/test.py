import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.text = tk.Text(self, wrap="none")
        xsb = tk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        ysb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        self.text.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text.tag_configure("keyword", foreground="#b22222")

        # this probably isn't what you want to do in production, 
        # but it's good enough for illustrative purposes
        self.text.bind("<Any-KeyRelease>", self.highlight)
        self.text.bind("<Any-ButtonRelease>", self.highlight)

    def highlight(self, event=None):
        self.text.tag_remove("keyword", "1.0", "end")

        count = tk.IntVar()
        self.text.mark_set("matchStart", "1.0")
        self.text.mark_set("matchEnd", "1.0")

        while True:
            index = self.text.search("print", "matchEnd","end", count=count)
            if index == "": break # no match was found

            self.text.mark_set("matchStart", index)
            self.text.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text.tag_add("keyword", "matchStart", "matchEnd")

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()