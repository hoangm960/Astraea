import os
import pickle
import sys
import time
from random import randrange

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, 
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
        self.pg = pg

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        LoginFunctions(self)
        
        
        self.OkCancelFrame.move(440, 247)

        def moveWindow(event):
            if LoginFunctions.GLOBAL_STATE == True:
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

    def __init__(self, ui):
        ui.OkCancelFrame.hide()
        ui.frameError.hide()
        ui.eyeHide_SI.hide()
        ui.eyeHide.hide()
        ui.stacked_widget.setCurrentIndex(0)
        ui.Note_Name.hide()
        ui.Note_Pass.hide()
        ui.Note_User.hide()
        ui.setGeometry(
            round((SCREEN_WIDTH - ui.width()) / 2),
            round((SCREEN_HEIGHT - ui.height()) / 2),
            ui.width(),
            ui.height()
        )
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_maximize.setToolTip("Phóng to")
        ui.btn_minimize.setToolTip("Thu nhỏ")
        ui.btn_quit.setToolTip("Đóng")
        self.connect_btn(ui)
        self.load_users()
        self.check_autosave(ui)
        self.move_TaskClose(ui)

    @staticmethod
    def move_TaskClose(ui):
        ui.OkCancelFrame.move(
            round((ui.frame.width() - 400) / 2),
            round((ui.frame.height() - 180) / 2),
        )

    def connect_btn(self, ui):
        
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_maximize.clicked.connect(lambda: self.move_TaskClose(ui))
        ui.btn_quit.clicked.connect(lambda: ui.OkCancelFrame.show())
        ui.Accept.clicked.connect(lambda: ui.close())
        if ui.pg:
            ui.Accept.clicked.connect(lambda: ui.pg.close())
        ui.Deny.clicked.connect(lambda: ui.OkCancelFrame.hide())
        ui.eyeHide_SI.clicked.connect(
            lambda: ui.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        ui.eyeHide.clicked.connect(
            lambda: ui.PassBox.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        ui.eyeShow_SI.clicked.connect(
            lambda: ui.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        ui.eyeShow.clicked.connect(
            lambda: ui.PassBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        ui.SignIn_Bt.clicked.connect(lambda: self.check_SI(ui))
        ui.SignUp_Bt.clicked.connect(lambda: self.check_SU(ui))
        ui.ConvertButton.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(1)
        )
        
        ui.ConvertButton_SU.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(0)
        )
        ui.ConvertButton_4.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(0)
        )
        ui.ConvertButton.clicked.connect(lambda: default())
    
        def default():
            ui.STATE_ECHOPASS = True
            ui.PassBox.clear()
            ui.NameBox.clear()
            ui.UserBox.clear()
            ui.Note_Name.hide()
            ui.Note_Pass.hide()
            ui.Note_User.hide()
            ui.student.setChecked(True)

    def check_autosave(self, ui):
        for user in self.users:
            if user.auto_saved:
                ui.NameBox_SI.setText(user.name)
                ui.PassBox_SI.setText(user.password)
                ui.SavePass.setChecked(True)
                break

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()
            self.GLOBAL_STATE = True
            ui.verticalLayout.setContentsMargins(0, 0, 0, 0)
            ui.btn_maximize.setToolTip("Khôi phục")
            ui.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/images/icons/Bg.jpg);
                    border-radius: 0px;
                    }"""
            )
        else:
            ui.showNormal()
            self.GLOBAL_STATE = False
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.verticalLayout.setContentsMargins(10, 10, 10, 10)
            ui.btn_maximize.setToolTip("Phóng to")
            ui.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/images/icons/Bg.jpg);
                    border-radius: 9px;
                    }"""
            )

    def load_users(self):
        self.users.clear()
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        time.sleep(1)
        if os.path.getsize(self.USER_PATH) > 0:
            with open(self.USER_PATH, "rb") as f:
                unpickler = pickle.Unpickler(f)
                self.users = unpickler.load()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

    def check_SI(self, ui):
        name = ui.NameBox_SI.text()[:31]
        password = ui.PassBox_SI.text()[:22]
        if len(password)*len(name) == 0:
            ui.frameError.show()
            ui.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        elif not [True for user in self.users if user.name == name]:
            ui.frameError.show()
            ui.Error_Content.setText(
                "Tên tài khoản không tồn tại. Hãy nhập lại.")
        elif not [True for user in self.users if user.name == name and user.password == password]:
            ui.frameError.show()
            ui.Error_Content.setText(
                "Mật khẩu không chính xác. Hãy nhập lại.")
        else:
            for user in self.users:
                if user.name == name:
                    with open(self.OPENED_USER, 'w', encoding='utf-8') as f:
                        f.write(user.name_user)
                        f.write('\n')
                        f.write(user.id)
                        f.write('\n')
                        f.write(user.password)
                        f.write('\n')
                    for i in range(len(self.users)):
                        self.users[i].auto_saved = False
                    if ui.SavePass.isChecked():
                        self.users[self.users.index(user)].auto_saved = True
                    else:
                        self.users[self.users.index(user)].auto_saved = False    
                    decrypt(self.USER_PATH_ENCRYPTED,
                            self.USER_PATH, self.KEY_PATH)
                    time.sleep(1)
                    with open(self.USER_PATH, "wb") as f:
                        pickle.dump(self.users, f)
                    encrypt(self.USER_PATH,
                            self.USER_PATH_ENCRYPTED, self.KEY_PATH)

                    ui.close()
                    main_ui.main(user.role, ui.pg)
                    break
        QtCore.QTimer.singleShot(3000, lambda: ui.frameError.hide())

    def check_SU(self, ui):
        check = True
        name = ui.NameBox.text()[:31]
        password = ui.PassBox.text()[:22]
        name_account = ui.UserBox.text()[:30]
        
        if len(name) < 8 or list(
            set(False for i in name.lower() if i not in self.enabled)
        ) == [False]:
            ui.Note_Name.show()
            check = False
        else:
            for user in self.users:
                if name == user.name:
                    ui.Note_Name.show()
                    check = False
                    break
            else:
                ui.Note_Name.hide()

        if len(password) < 8 or list(
            set(False for i in password.lower() if i not in self.enabled)
        ) == [False]:
            ui.Note_Pass.show()
            check = False
        else:
            ui.Note_Pass.hide()
        if not "".join([i for i in name_account.lower() if i not in self.enabled]).isalnum():
            if (not "".join([i for i in name_account.lower() if i not in self.enabled]) == ""):
                ui.Note_User.show()
                check = False
            else:
                ui.Note_User.hide()
        else:
            ui.Note_User.hide()
        if len(name_account) < 6:
            ui.Note_User.show()
            check = False
        if check:
            decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
            with open(self.USER_PATH, "wb") as f:
                name = ui.NameBox.text()
                password = ui.PassBox.text()
                role = "teacher" if ui.teacher.isChecked() else "student"
                code = ''
                for i in range(0, 8):
                    code += str(randrange(0, 10))
                self.users.append(
                    User(name, password, role, name_account, code, False))
                pickle.dump(self.users, f)

            encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
            for user in self.users:
                if user.auto_saved:
                    user.auto_saved = False
            ui.NameBox_SI.clear()
            ui.PassBox_SI.clear()
            ui.SavePass.setChecked(False)
            ui.stacked_widget.setCurrentIndex(2)

class Loading_Screen(QMainWindow):
    counter = 0

    def __init__(self, pg, version):
        self.pg = pg
        self.version = version

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("./UI_files/Loading_Screen.ui", self)
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        UILoadingFunctions(self, version)

class UILoadingFunctions(Loading_Screen):
    def __init__(self, ui, version):
        self.update_version(ui, str(version))

        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.timer = QtCore.QTimer()
        ui.timer.timeout.connect(lambda: self.progress(ui))
        ui.timer.start(20)
        ui.show()

    @staticmethod
    def update_version(ui, version):
        ui.version.setText(f'<html><head/><body><p align="right"><span style=" font-size:14pt; color:#ffffff;">v{version}</span></p></body></html>')

    @classmethod
    def delay(self, point, wait):
        if self.counter == point:
            time.sleep(wait)

    @classmethod
    def progress(self, ui):
        ui.progressBar.setValue(self.counter)
        if self.counter > 100:
            ui.timer.stop()
            ui.main = LoginWindow(ui.pg)
            ui.main.setGeometry(
                round((SCREEN_WIDTH - ui.main.width()) / 2),
                round((SCREEN_HEIGHT - ui.main.height()) / 5),
                ui.main.width(),
                ui.main.height(),
            )
            ui.main.show()
            ui.close()
        if self.counter == 20:
            ui.timer.singleShot(
                1500, lambda: ui.Loading_label.setText(
                    "Kiểm tra cài đặt ...")
            )
        if self.counter == 45:
            ui.timer.singleShot(
                2905, lambda: ui.Loading_label.setText(
                    "Thiết lập giao diện ...")
            )
        if self.counter == 73:
            ui.timer.singleShot(
                1500, lambda: ui.Loading_label.setText(
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


def main(pg, version, file=''):
    FILE = file
    app = QApplication(sys.argv)
    splash_window = Loading_Screen(pg, version)
    splash_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(None, 2.5)
