import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QPalette
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
from encryption import *
from random import randrange


class User:
    def __init__(self, name, password, role, name_user, auto_saved):
        self.name = name
        self.password = password
        self.role = role
        self.auto_saved = auto_saved
        self.name_user = name_user


class LoginWindow(QMainWindow):
    UI_PATH = "UI_Files/Login_gui.ui"

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        LoginFunctions.uiDefinitions(self)

        self.OkCancelFrame.move(290, 220)

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
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    KEY_PATH = "data/encryption/users.key"

    @classmethod
    def uiDefinitions(cls, self):

        self.OkCancelFrame.hide()
        self.frameError.hide()
        self.eyeHide.hide()
        self.eyeHide_SU.hide()
        self.stacked_widget.setCurrentIndex(0)
        self.NoteName.hide()
        self.NotePass.hide()
        self.NoteUser.hide()
        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        cls.connect_btn(self)
        cls.setup_sizegrip(self)
        cls.load_users()
        cls.check_autosave(self)
        cls.move_TaskClose(self)

    @classmethod
    def move_TaskClose(cls, self):
        self.OkCancelFrame.move(
            round((self.frame.width() - 400) / 2),
            round((self.frame.height() - 180) / 2),
        )

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
        self.btn_maximize.clicked.connect(lambda: cls.move_TaskClose(self))
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())
        self.Accept.clicked.connect(lambda: self.close())
        self.eyeHide.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeHide_SU.clicked.connect(
            lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeShow.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.eyeShow_SU.clicked.connect(
            lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.SignIn_Bt.clicked.connect(lambda: cls.check_SI(self))
        self.SignUp_Bt.clicked.connect(lambda: cls.check_SU(self))
        self.ConvertButton.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )
        self.ConvertButton_SU.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        self.ConvertButton_4.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        self.ConvertButton.clicked.connect(lambda: default())

        def default():
            self.STATE_ECHOPASS = True
            self.PassBox_SU.clear()
            self.NameBox_SU.clear()
            self.UserBox.clear()
            self.NoteName.hide()
            self.NotePass.hide()
            self.NoteUser.hide()
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
    def load_users(cls):
        cls.users.clear()
        decrypt(cls.USER_PATH_ENCRYPTED, cls.USER_PATH, cls.KEY_PATH)
        time.sleep(1)
        if os.path.getsize(cls.USER_PATH) > 0:
            with open(cls.USER_PATH, "rb") as f:
                unpickler = pickle.Unpickler(f)
                cls.users = unpickler.load()
        get_key(cls.KEY_PATH)
        encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)

    @classmethod
    def check_SI(cls, self):
        name = self.NameBox_SI.text()[:31]
        password = self.PassBox_SI.text()[:22]
        for user in cls.users:
            if name == "" or password == "":
                cls.Error(self, "Chưa điền đầy đủ thông tin đăng nhập")
            elif name not in user.name:
                cls.Error(self, "Tên tài khoản không tồn tại. Hãy nhập lại.")
            elif password != user.password:
                cls.Error(self, "Mật khẩu không chính xác. Hãy nhập lại.")
            else:
                for i in range(len(cls.users)):
                    cls.users[i].auto_saved = False
                if self.SavePass.isChecked():
                    cls.users[cls.users.index(user)].auto_saved = True

                decrypt(cls.USER_PATH_ENCRYPTED, cls.USER_PATH, cls.KEY_PATH)
                time.sleep(1)
                with open(cls.USER_PATH, "wb") as f:
                    pickle.dump(cls.users, f)
                encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)

                self.close()
                main_ui.main(user.role)
                break
            QtCore.QTimer.singleShot(3000, lambda: self.frameError.hide())

    @classmethod
    def check_SU(cls, self):
        check = True
        name = self.NameBox_SU.text()[:31]
        password = self.PassBox_SU.text()[:26]
        name_account = self.UserBox.text()[:30]

        for user in cls.users:
            if (
                len(name) < 6
                or name in user.name
                or list(
                    set(
                        False
                        for i in name.lower()
                        if i not in "qwertyuiopasdfghjklzxcvbnm1234567890 "
                    )
                )
                == [False]
            ):
                self.NoteName.show()
                check = False
            else:
                self.NoteName.hide()
        if len(password) < 8 or list(
            set(
                False
                for i in password.lower()
                if i not in "qwertyuiopasdfghjklzxcvbnm1234567890 "
            )
        ) == [False]:
            self.NotePass.show()
            check = False
        else:
            self.NotePass.hide()
        if len(name_account) < 6 or name_account.replace(" ", "").isalnum() is False:
            self.NoteUser.show()
            check = False
        else:
            self.NoteUser.hide()
        if check:
            decrypt(cls.USER_PATH_ENCRYPTED, cls.USER_PATH, cls.KEY_PATH)
            with open(cls.USER_PATH, "wb") as f:
                name = self.NameBox_SU.text()
                password = self.PassBox_SU.text()
                role = "teacher" if self.Teacher_SU.isChecked() else "student"
                cls.users.append(User(name, password, role, name_account, False))
                pickle.dump(cls.users, f)

            encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)
            self.stacked_widget.setCurrentIndex(2)


class Loading_Screen(QMainWindow):
    counter = 0

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_files/Loading_Screen.ui", self)
        self.move(
            round((GetSystemMetrics(0) - self.width()) / 2),
            round((GetSystemMetrics(1) - self.height()) / 2),
        )

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)
        self.show()

    def delay(self, point, wait):
        if self.counter == point:
            time.sleep(wait)

    def progress(self):
        self.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            self.main = LoginWindow()
            self.main.setGeometry(
                round((GetSystemMetrics(0) - self.main.width()) / 2),
                round((GetSystemMetrics(1) - self.main.height()) / 5),
                self.main.width(),
                self.main.height(),
            )
            self.main.show()
            self.close()
        if self.counter == 20:
            self.timer.singleShot(
                1500, lambda: self.Loading_label.setText("Kiểm tra cài đặt ...")
            )
        if self.counter == 45:
            self.timer.singleShot(
                2905, lambda: self.Loading_label.setText("Thiết lập giao diện ...")
            )
        if self.counter == 73:
            self.timer.singleShot(
                1500, lambda: self.Loading_label.setText("Kết nối dữ liệu  ...")
            )
        self.delay(randrange(5, 10), 0.1)
        self.delay(randrange(20, 30), 0.23)
        self.delay(randrange(40, 50), 0.43)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(80, 90), 0.17)
        self.delay(randrange(90, 99), 0.6)
        self.delay(99, 1)
        self.counter += 1


def main():
    app = QApplication(sys.argv)
    splash_window = Loading_Screen()
    splash_window.show()
    sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
