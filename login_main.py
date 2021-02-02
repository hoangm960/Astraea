import os
import pickle
import subprocess
import sys
import time
from random import randrange
import mysql.connector

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
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
    def __init__(self, id, name, name_user, password, role):
        self.id = id
        self.name = name
        self.name_user = name_user
        self.password = password
        self.role = role


class LoginWindow(QMainWindow):
    UI_PATH = "UI_Files/Login_gui.ui"

    def __init__(self, pg, connection):
        self.pg = pg
        self.connection = connection
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        LoginFunctions(self)
        

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
    enabled = "qwertyuiopasdfghjklzxcvbnm1234567890 @/._"
    GLOBAL_STATE = False
    STATE_ECHOPASS = True
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    KEY_PATH = "data/encryption/users.key"

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
        ui.HorizontalSpacer_L.hide()
        self.connect_btn(ui)
        self.check_autosave(ui)

    def connect_btn(self, ui):
        
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_quit.clicked.connect(lambda: ui.OkCancelFrame.show())
        ui.Accept.clicked.connect(lambda: ui.close())
        def close_pg():
            try:
                ui.pg.close()
            except:
                pass
        ui.Accept.clicked.connect(close_pg)
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
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        time.sleep(1)
        with open(self.USER_PATH) as f:
            lines = f.readlines()
        if lines:
            if bool(lines[-1]):
                ui.NameBox_SI.setText(lines[0].rstrip())
                ui.PassBox_SI.setText(lines[2].rstrip())
                ui.SavePass.setChecked(True)
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

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

    def check_SI(self, ui):
        cursor = ui.connection.cursor()
        username = ui.NameBox_SI.text()[:31]
        password = ui.PassBox_SI.text()[:22]

        if len(password)*len(username) == 0:
            ui.frameError.show()
            ui.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        else:
            cursor.execute("SELECT Username FROM user WHERE Username = %s", (username, ))
            if username not in [row[0] for row in cursor]:
                ui.frameError.show()
                ui.Error_Content.setText(
                    "Tên tài khoản không tồn tại. Hãy nhập lại.")
            else:
                cursor.execute("SELECT Username, Password FROM user WHERE Username = %s AND Password = %s", (username, password))
                if not [row[0] for row in cursor]:
                    ui.frameError.show()
                    ui.Error_Content.setText(
                        "Mật khẩu không chính xác. Hãy nhập lại.")
                else:
                    cursor.execute(f"SELECT ShowName, Password, Type FROM user WHERE Username = '{username}'")
                    name, password, role = (row[i] for row in cursor for i in range(len(row)))

                    decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
                    with open(self.USER_PATH, 'w', encoding='utf-8') as f:
                        f.write(f'{username}\n')
                        f.write(f'{name}\n')
                        f.write(f'{password}\n')
                        f.write('True' if ui.SavePass.isChecked() else 'False')
                    encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

                    ui.close()
                    main_ui.main(role, ui.pg, ui.connection)
                QtCore.QTimer.singleShot(3000, lambda: ui.frameError.hide())

    def check_SU(self, ui):
        cursor = ui.connection.cursor()
        check = True
        username = ui.NameBox.text()[:31]
        password = ui.PassBox.text()[:22]
        name = ui.UserBox.text()[:30]
        
        if len(username) < 8 or list(
            set(False for i in username.lower() if i not in self.enabled)
        ) == [False]:
            ui.Note_Name.show()
            check = False
        else:
            cursor.execute("SELECT Username FROM user WHERE Username = %s", (username, ))
            if [row for row in cursor]:
                ui.Note_Name.show()
                check = False
            else:
                ui.Note_Name.hide()

        if len(password) < 8 or list(
            set(False for i in password.lower() if i not in self.enabled)
        ) == [False]:
            ui.Note_Pass.show()
            check = False
        else:
            ui.Note_Pass.hide()

        if not "".join([i for i in name.lower() if i not in self.enabled]).isalnum():
            if (not "".join([i for i in name.lower() if i not in self.enabled]) == ""):
                ui.Note_User.show()
                check = False
            else:
                ui.Note_User.hide()
        else:
            ui.Note_User.hide()

        if len(name) < 6:
            ui.Note_User.show()
            check = False

        if check:
            role = 1 if ui.teacher.isChecked() else 0
            cursor.execute("INSERT INTO user(Username, ShowName, Password, Type) VALUES(%s, %s, %s, %s)", (username, name, password, role))
            ui.connection.commit()

            ui.NameBox_SI.clear()
            ui.PassBox_SI.clear()
            ui.SavePass.setChecked(False)
            ui.stacked_widget.setCurrentIndex(2)

class Loading_Screen(QMainWindow):
    counter = 0

    def __init__(self, version):
        self.version = version

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("./UI_files/Loading_Screen.ui", self)
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        UILoadingFunctions(self, version)

class UILoadingFunctions(Loading_Screen):
    PG = None
    connection = None
    def __init__(self, ui, version):
        self.update_version(ui, str(version))

        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.frame.hide()
        ui.Out.clicked.connect(lambda: ui.close())
        ui.pushButton.clicked.connect(lambda: self.tryAgain(ui, version))
        ui.timer = QtCore.QTimer()
        ui.timer.timeout.connect(lambda: self.progress(ui))
        ui.timer.start(20)
        ui.show()

    @staticmethod
    def update_version(ui, version):
        ui.version.setText(f'<html><head/><body><p align="right"><span style=" font-size:14pt; color:#ffffff;">v{version}</span></p></body></html>')

    def delay(self, point, wait):
        if self.counter == point:
            time.sleep(wait)

    def tryAgain(self, ui, version):
        ui.close()
        window = Loading_Screen(version)
        window.show()

    def progress(self, ui):
        ui.progressBar.setValue(self.counter)
        if self.counter > 100:
            ui.timer.stop()
            ui.main = LoginWindow(self.PG, self.connection)
            ui.main.setGeometry(
                round((SCREEN_WIDTH - ui.main.width()) / 2),
                round((SCREEN_HEIGHT - ui.main.height()) / 5),
                ui.main.width(),
                ui.main.height(),
            )
            ui.main.show()
            ui.close()
            
        if self.counter == 6:
            ui.timer.singleShot(
                1500, lambda: ui.Loading_label.setText(
                    "kiểm tra cài đặt ...")
            )  
            try:
                import thonny
            except ImportError:
                ui.timer.singleShot(500, lambda: ui.Loading_label.setText("đang tải Thonny...")) 
                subprocess.call('pip3 install thonny')
                time.sleep(6)      
        if self.counter == 14:
            ui.timer.singleShot(
                2905, lambda: ui.Loading_label.setText(
                    "khởi động ...")
            )
            import pygetwindow as gw        
            subprocess.Popen(['thonny'], shell=True)
            time.sleep(2)
            ide_title = ''
            while not ide_title:
                titles = gw.getAllTitles()
                for title in titles:
                    if "thonny" in title.lower():
                        ide_title = title
                        break
            if gw.getWindowsWithTitle(ide_title):
                self.PG = gw.getWindowsWithTitle(ide_title)[0]
                self.PG.minimize()
        if self.counter == 50:
            ui.Loading_label.setText("đang kết nối...")
        if self.counter == 73:
            time.sleep(3)
            try:
                    self.connection = mysql.connector.connect(
                            host="remotemysql.com",
                            user="K63yMSwITl",
                            password="zRtA9VtyHq",
                            database="K63yMSwITl"
                    )
            except:
                ui.Loading_label.setText("kết nối thất bại. Đường truyền không ổn định.")
                ui.frame.show()
                ui.timer.stop()
                ui.progressBar.hide()
                self.PG.close()
        self.delay(randrange(5, 10), 0.1)
        self.delay(randrange(20, 30), 0.23)
        self.delay(randrange(40, 50), 0.43)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(80, 90), 0.17)
        self.delay(randrange(90, 99), 0.6)
        self.delay(99, 1)
        self.counter += 1
        


def main(version):
    app = QApplication(sys.argv)
    splash_window = Loading_Screen(version)
    splash_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main('2.6')
