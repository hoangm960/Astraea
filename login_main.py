import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMainWindow, QSizeGrip, QWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from win32api import GetSystemMetrics
import main_ui
import pickle
import time


class User:
    def __init__(self, name, password, role, auto_saved):
        self.name = name
        self.password = password
        self.role = role
        self.auto_saved = auto_saved

class LoginWindow(QMainWindow):
    STATE_ECHOPASS = True
    with open('data/Users/User.txt','a+') as f:
        f.close()
    USER_PATH = "data/Users/User.txt"
    UI_PATH = "UI_Files/Login_gui.ui"
    users = []

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(self.UI_PATH, self)
        self.OkCancelFrame.hide()
        self.Accept.clicked.connect(lambda: self.close())
        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 200))
        self.bg_frame.setGraphicsEffect(self.shadow)

        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())
        self.eyeButton_SU.hide()
        self.eyeButton_SI.hide()
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}"
        )
        self.sizegrip.setToolTip("This was locked")
        self.eyeButton_SI.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeButton_SU.clicked.connect(
            lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeButton_SI_2.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.eyeButton_SU_2.clicked.connect(
            lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.SignIn_Bt.clicked.connect(lambda: self.check_SI())
        self.SignUp_Bt.clicked.connect(lambda: self.check_SU())

        def default():
            self.STATE_ECHOPASS = True

        self.ConvertButton.clicked.connect(lambda: default())
        self.ConvertButton_SU.clicked.connect(lambda: default())

        self.load_users()
        for user in self.users:
            if user.auto_saved:
                self.NameBox_SI.setText(user.name)
                self.PassBox_SI.setText(user.password)
                self.SavePass.setChecked(True)
                break

        self.frameError.hide()
        self.Complete_Frame.hide()
        self.SignUp_Frame.hide()
       
    def Error(self, text):
        self.frameError.show()
        self.Error_Content.setText(text)

    def load_users(self):
        self.users.clear()
        if os.path.getsize(self.USER_PATH) > 0:
            with open(self.USER_PATH, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                self.users = unpickler.load()

    # Check sign in
    def check_SI(self):
        self.load_users()
        name = self.NameBox_SI.text()
        password = self.PassBox_SI.text()
        for user in self.users:
            if name == "" or password == "":
                self.Error('Chưa điền đầy đủ thông tin đăng nhập')
            elif name not in user.name:
                self.Error('Tên tài khoản không tồn tại. Hãy nhập lại.')
            elif password != user.password:
                self.Error('Mật khẩu không chính xác. Hãy nhập lại.')
            else:
                if self.SavePass.isChecked() and not user.auto_saved:
                    user.auto_saved = True
                elif not self.SavePass.isChecked() and user.auto_saved:
                    user.auto_saved = False
                with open(self.USER_PATH, "wb") as f:
                    pickle.dump(self.users, f)
                f.close()
                self.close()
                main_ui.main(user.role)
                break
            QtCore.QTimer.singleShot(2000, lambda: self.frameError.hide())
           

    # Check your signing up
    def check_SU(self):
        check = True
        self.load_users()
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        for user in self.users:
            if len(name) < 6:
                self.Error('Yêu cầu độ dài tên tài khoản hơn 5 kí tự.')
                check = False

            elif name in user.name:
                self.Error('Tên tài khoản đã tồn tại. Hãy lựa chọn tên khác.')
                check = False

            elif len(password) < 8:
                self.Error('Yêu cầu độ dài mật khẩu hơn 7 kí tự')
                check = False

            else:
                for word in name:
                    if word not in "qwertyuiopasdfghjklzxcvbnm1234567890 ":
                        self.Error('Tên tài khoản không được chứa kí tự đặc biệt')
                        check = False
                    else:
                        for word in password:
                            if word not in "qwertyuiopasdfghjklzxcvbnm1234567890 ":
                                self.Error('Mật khẩu không được chứa kí tự đặc biệt')
                                check = False

        if check:
            with open(self.USER_PATH, "wb") as f:
                name = self.NameBox_SU.text()
                password = self.PassBox_SU.text()
                role = "teacher" if self.Teacher_SU.isChecked() else "student"
                self.users.append(User(name, password, role, False))
                pickle.dump(self.users, f)

            self.SignUp_Frame.hide()
            self.Complete_Frame.show()
            f.close()
        QtCore.QTimer.singleShot(2000, lambda: self.frameError.hide())

# </>-------------------
class Loading_Screen(QMainWindow):
    counter = 0
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_files/Loading_Screen.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(100)
        self.show()
    def delay(self, point, wait):
        if self.counter == point :
            time.sleep(wait) 
    def progress(self):
        self.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            self.main = LoginWindow()
            self.main.show()
            self.close()
        if self.counter == 20:
            self.timer.singleShot(1500, lambda: self.Loading_label.setText('Kiểm tra cài đặt ...'))
        if self.counter == 45:
            self.timer.singleShot(1500, lambda: self.Loading_label.setText('Thiết lập giao diện ...'))
        if self.counter == 73:
            self.timer.singleShot(1500, lambda: self.Loading_label.setText('Kết nối dữ liệu  ...'))     
        self.delay(7,0.1)
        self.delay(20,0.23)
        self.delay(44, 0.43)
        self.delay(73, 0.93)
        self.delay(80, 0.17)
        self.delay(97, 0.6)
        self.delay(98, 1)
        self.delay(99, 3.53)
        self.counter += 1

def main():
    app = QApplication(sys.argv)
    splash_window = Loading_Screen()
    splash_window.move(round(GetSystemMetrics(0) / 4), round(GetSystemMetrics(1) / 4))
    splash_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
