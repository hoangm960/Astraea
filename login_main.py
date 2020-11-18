import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QSizeGrip,
    QWidget,
)
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
    file = open('data/Users/User.txt', 'a+')
    file.close()
    USER_PATH = "data/Users/User.txt"
    UI_PATH = "UI_Files/Login_gui.ui"
    users = []

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        LoginFunctions.uiDefinitions(self)

        def moveWindow(event):
            if LoginFunctions.returnStatus() == True:
                LoginFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class LoginFunctions(LoginWindow):
    users = []
    GLOBAL_STATE = False
    STATE_ECHOPASS = True

    @classmethod
    def uiDefinitions(cls, self):
        self.OkCancelFrame.hide()
        self.frameError.hide()
        self.eyeButton_SU.hide()
        self.eyeButton_SI.hide()
        self.stacked_widget.setCurrentIndex(0)

        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        cls.connect_btn(self)
        cls.setup_sizegrip(self)
        cls.check_autosave(self)

    @classmethod
    def create_dropshadow(cls, self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 200))
        self.bg_frame.setGraphicsEffect(self.shadow)

    @classmethod
    def connect_btn(cls, self):
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize.clicked.connect(lambda: cls.maximize_restore(self))
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())
        self.Accept.clicked.connect(lambda: self.close())
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
        self.SignIn_Bt.clicked.connect(lambda: cls.check_SI(self))
        self.SignUp_Bt.clicked.connect(lambda: cls.check_SU(self))
        self.ConvertButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ConvertButton_SU.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ConvertButton_4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ConvertButton.clicked.connect(lambda: default())
        def default():
            self.STATE_ECHOPASS = True
            self.PassBox_SU.clear()
            self.NameBox_SU.clear()
            self.Student_SU.setChecked(True)

    @classmethod
    def setup_sizegrip(cls, self):
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}"
        )
        self.sizegrip.setToolTip("This was locked")

    @classmethod
    def check_autosave(cls, self):
        cls.load_users(self)
        for user in cls.users:
            if user.auto_saved:
                self.NameBox_SI.setText(user.name)
                self.PassBox_SI.setText(user.password)
                self.SavePass.setChecked(True)
                break

    @classmethod
    def returnStatus(cls):
        return cls.GLOBAL_STATE
    
    @classmethod
    def maximize_restore(cls, self):
        status = cls.GLOBAL_STATE

        if status == False:
            cls.GLOBAL_STATE = True
            self.showMaximized()
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.btn_maximize.setToolTip("Maximize")

    @classmethod
    def Error(cls, self, text):
        self.frameError.show()
        self.Error_Content.setText(text)

    @classmethod
    def load_users(cls, self):
        cls.users.clear()
        if os.path.getsize(self.USER_PATH) > 0:
            with open(self.USER_PATH, "rb") as f:
                unpickler = pickle.Unpickler(f)
                cls.users = unpickler.load()

    @classmethod
    def check_SI(cls, self):
        cls.load_users(self)
        name = self.NameBox_SI.text()
        password = self.PassBox_SI.text()
        for user in cls.users:
            if name == "" or password == "":
                cls.Error(self, 'Chưa điền đầy đủ thông tin đăng nhập')
            elif name not in user.name:
                cls.Error(self, 'Tên tài khoản không tồn tại. Hãy nhập lại.')
            elif password != user.password:
                cls.Error(self, 'Mật khẩu không chính xác. Hãy nhập lại.')
            else:
                for i in range(len(cls.users)):
                    cls.users[i].auto_saved = False
                if self.SavePass.isChecked():
                    cls.users[cls.users.index(user)].auto_saved = True
                with open(self.USER_PATH, "wb") as f:
                    pickle.dump(cls.users, f)

                self.close()
                main_ui.main(user.role)
                break
            QtCore.QTimer.singleShot(3000, lambda: self.frameError.hide())
           

    @classmethod
    def check_SU(cls, self):
        check = True
        cls.load_users(self)
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        for user in cls.users:
            if len(name) < 6:
                cls.Error(self, 'Yêu cầu độ dài tên tài khoản hơn 5 kí tự.')
                check = False

            elif name in user.name:
                cls.Error(self, 'Tên tài khoản đã tồn tại. Hãy lựa chọn tên khác.')
                check = False

            elif len(password) < 8:
                cls.Error(self, 'Yêu cầu độ dài mật khẩu hơn 7 kí tự')
                check = False

            else:
                if name.isalnum() is False:
                    if name.replace(' ','').isalnum() is True:
                        pass
                    else:
                        cls.Error(self, 'Tên tài khoản không được chứa kí tự đặc biệt')
                        check = False
                else:        
                    if password.isalnum() is False:
                        if password.replace(' ','').isalnum() is True:
                            pass
                        else: 
                            cls.Error(self, 'Mật khẩu không được chứa kí tự đặc biệt')
                            check = False

        if check:
            with open(self.USER_PATH, "wb") as f:
                name = self.NameBox_SU.text()
                password = self.PassBox_SU.text()
                role = "teacher" if self.Teacher_SU.isChecked() else "student"
                cls.users.append(User(name, password, role, False))
                pickle.dump(cls.users, f)

            self.stacked_widget.setCurrentIndex(2)
        QtCore.QTimer.singleShot(3000, lambda: self.frameError.hide())

class Loading_Screen(QMainWindow):
    counter = 0
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_files/Loading_Screen.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)
        self.show()
    def delay(self, point, wait):
        if self.counter == point :
            time.sleep(wait) 
    def progress(self):
        self.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            self.main = LoginWindow()
            LOGIN_WIDTH = 999
            LOGIN_HEIGHT = 700
            self.main.setGeometry(round((GetSystemMetrics(0) - LOGIN_WIDTH)/2), round((GetSystemMetrics(1) - LOGIN_HEIGHT)/5), LOGIN_WIDTH, LOGIN_HEIGHT)
            self.main.show()
            self.close()
        if self.counter == 20:
            self.timer.singleShot(1500, lambda: self.Loading_label.setText('Kiểm tra cài đặt ...'))
        if self.counter == 45:
            self.timer.singleShot(2905, lambda: self.Loading_label.setText('Thiết lập giao diện ...'))
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
