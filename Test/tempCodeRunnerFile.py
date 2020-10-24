def destroy():
    for widget in frame.winfo_children():
        widget.destroy()