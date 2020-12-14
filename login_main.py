import os
import pickle
import sys
import time
from random import randrange

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect,
                             QMainWindow)
from win32api import GetMonitorInfo, MonitorFromPoint

import main_ui
from encryption import *

FILE = ""
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]


class User:
    def __init__(self, name, password, role, name_user, id, auto_saved):
        self.name = name
        self.password = password
        self.role = role
        self.auto_saved = auto_saved
        self.name_user = name_user
        self.id = id

class LoginWindow(QMainWindow):
    UI_PATH = "UI_Files/Login_gui.ui"

    def __init__(self, pg):
        self.pg = pg if pg else None

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        LoginFunctions.uiDefinitions(self)

        self.OkCancelFrame.move(440, 247)

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
    enabled = "qwertyuiopasdfghjklzxcvbnm1234567890 @/._"
    GLOBAL_STATE = False
    STATE_ECHOPASS = True
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    KEY_PATH = "data/encryption/users.key"
    OPENED_USER = "data/Users/opened_user.ou"

    @classmethod
    def uiDefinitions(cls, self):

        self.OkCancelFrame.hide()
        self.frameError.hide()
        self.eyeHide_SI.hide()
        self.eyeHide.hide()
        self.stacked_widget.setCurrentIndex(0)
        self.Note_Name.hide()
        self.Note_Pass.hide()
        self.Note_User.hide()
        self.Note_Name.clicked.connect(lambda: self.Note_Name.QToolTip.show())
        self.setGeometry(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
            self.width(),
            self.height()
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.btn_maximize.setToolTip("Phóng to")
        self.btn_minimize.setToolTip("Thu nhỏ")
        self.btn_quit.setToolTip("Đóng")
        cls.connect_btn(self)
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
        self.Deny.clicked.connect(lambda: self.OkCancelFrame.hide())
        self.eyeHide_SI.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeHide.clicked.connect(
            lambda: self.PassBox.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeShow_SI.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.eyeShow.clicked.connect(
            lambda: self.PassBox.setEchoMode(QtWidgets.QLineEdit.Normal)
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
            self.PassBox.clear()
            self.NameBox.clear()
            self.UserBox.clear()
            self.Note_Name.hide()
            self.Note_Pass.hide()
            self.Note_User.hide()
            self.student.setChecked(True)

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
            self.showMaximized()
            cls.GLOBAL_STATE = True
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.btn_maximize.setToolTip("Khôi phục")
            self.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/images/icons/Bg.jpg);
                    border-radius: 0px;
                    }"""
            )
        else:
            self.showNormal()
            cls.GLOBAL_STATE = False
            self.resize(self.width() + 1, self.height() + 1)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.btn_maximize.setToolTip("Phóng to")
            self.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/images/icons/Bg.jpg);
                    border-radius: 9px;
                    }"""
            )

    @classmethod
    def load_users(cls):
        cls.users.clear()
        decrypt(cls.USER_PATH_ENCRYPTED, cls.USER_PATH, cls.KEY_PATH)
        time.sleep(1)
        if os.path.getsize(cls.USER_PATH) > 0:
            with open(cls.USER_PATH, "rb") as f:
                unpickler = pickle.Unpickler(f)
                cls.users = unpickler.load()
        encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)

    @classmethod
    def check_SI(cls, self):
        name = self.NameBox_SI.text()[:31]
        password = self.PassBox_SI.text()[:22]
        if len(password)*len(name) == 0:
            self.frameError.show()
            self.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        elif not [True for user in cls.users if user.name == name]:
            self.frameError.show()
            self.Error_Content.setText(
                "Tên tài khoản không tồn tại. Hãy nhập lại.")
        elif not [True for user in cls.users if user.name == name and user.password == password]:
            self.frameError.show()
            self.Error_Content.setText(
                "Mật khẩu không chính xác. Hãy nhập lại.")
        else:
            for user in cls.users:
                if user.name == name:
                    with open(cls.OPENED_USER, 'w', encoding = 'utf-8') as pro:
                        pro.write(user.name_user)
                        pro.write('\n')
                        pro.write(user.id)
                        pro.write('\n')
                        pro.write(user.password)
                        pro.write('\n')
                    for i in range(len(cls.users)):
                        cls.users[i].auto_saved = False
                    if self.SavePass.isChecked():
                        cls.users[cls.users.index(user)].auto_saved = True

                    decrypt(cls.USER_PATH_ENCRYPTED,
                            cls.USER_PATH, cls.KEY_PATH)
                    time.sleep(1)
                    with open(cls.USER_PATH, "wb") as f:
                        pickle.dump(cls.users, f)
                    encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)

                    self.close()
                    main_ui.main(user.role, self.pg)
                    break
        QtCore.QTimer.singleShot(3000, lambda: self.frameError.hide())
    @classmethod
    def check_SU(cls, self):
        check = True
        name = self.NameBox.text()[:31]
        password = self.PassBox.text()[:22]
        name_account = self.UserBox.text()[:30]
        if len(name) < 8 or list(
            set(False for i in name.lower() if i not in cls.enabled)
        ) == [False]:
            self.Note_Name.show()
            check = False
        else:
            for user in cls.users:
                if name == user.name:
                    self.Note_Name.show()
                    check = False
                    break
            else:
                self.Note_Name.hide()

        if len(password) < 8 or list(
            set(False for i in password.lower() if i not in cls.enabled)
        ) == [False]:
            self.Note_Pass.show()
            check = False
        else:
            self.Note_Pass.hide()
        if not "".join([i for i in name_account.lower() if i not in cls.enabled]).isalnum():
            if (not "".join([i for i in name_account.lower() if i not in cls.enabled]) == ""):
                self.Note_User.show()
                check = False
            else:
                self.Note_User.hide()
        else:
            self.Note_User.hide()
        if len(name_account) < 6:
            self.Note_User.show()
            check = False
        if check:
            decrypt(cls.USER_PATH_ENCRYPTED, cls.USER_PATH, cls.KEY_PATH)
            with open(cls.USER_PATH, "wb") as f:
                name = self.NameBox.text()
                password = self.PassBox.text()
                role = "teacher" if self.teacher.isChecked() else "student"
                code = ''
                for i in range(0,8):
                    code+=str(randrange(0,10))
                cls.users.append(
                    User(name, password, role, name_account, code, False))
                pickle.dump(cls.users, f)

            encrypt(cls.USER_PATH, cls.USER_PATH_ENCRYPTED, cls.KEY_PATH)
            self.stacked_widget.setCurrentIndex(2)


class Loading_Screen(QMainWindow):
    counter = 0

    def __init__(self, pg):
        self.pg = pg if pg else None

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_files/Loading_Screen.ui", self)
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
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
            self.main = LoginWindow(self.pg)
            self.main.setGeometry(
                round((SCREEN_WIDTH - self.main.width()) / 2),
                round((SCREEN_HEIGHT - self.main.height()) / 5),
                self.main.width(),
                self.main.height(),
            )
            self.main.show()
            self.close()
        if self.counter == 20:
            self.timer.singleShot(
                1500, lambda: self.Loading_label.setText(
                    "Kiểm tra cài đặt ...")
            )
        if self.counter == 45:
            self.timer.singleShot(
                2905, lambda: self.Loading_label.setText(
                    "Thiết lập giao diện ...")
            )
        if self.counter == 73:
            self.timer.singleShot(
                1500, lambda: self.Loading_label.setText(
                    "Kết nối dữ liệu  ...")
            )
        self.delay(randrange(5, 10), 0.1)
        self.delay(randrange(20, 30), 0.23)
        self.delay(randrange(40, 50), 0.43)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(80, 90), 0.17)
        self.delay(randrange(90, 99), 0.6)
        self.delay(99, 1)
        self.counter += 1


def main(pg, file=''):
    FILE = file
    app = QApplication(sys.argv)
    splash_window = Loading_Screen(pg)
    splash_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(None)
