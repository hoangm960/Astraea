if messagebox.askokcancel("Thông báo", "Xác nhận Kết thúc bài làm? \n(Chú ý không thể chỉnh sửa)"):
                    MainWindow.destroy()
                    MainWindow_new = GradientFrame(root,[350,700],colors = ("#00ffa9","#0d4dff"))
                    MainWindow_new.pack()
                    Label(MainWindow_new,text = ' Bạn đã nộp bài.', font = ('Arial Bold',20)).place(relx = 0.5, rely = 0.5, anchor = 'n')
                    self.Scoreboard()
