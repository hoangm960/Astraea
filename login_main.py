import time

import mysql.connector
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from encryption import *
import Main

FILE = ""
QuitFrameUI = "./UI_Files/QuitFrame.ui"


class User:
    def __init__(self, id, name, name_user, password, role):
        self.id = id
        self.name = name
        self.name_user = name_user
        self.password = password
        self.role = role


class LoginWindow(QMainWindow):
    UI_PATH = "UI_Files/Login_gui.ui"
    switch_window_main = QtCore.pyqtSignal(int)
    switch_window_quit = QtCore.pyqtSignal()

    def __init__(self, pg):
        self.pg = pg
        QMainWindow.__init__(self)
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
        ui.frameError.hide()
        ui.eyeHide_SI.hide()
        ui.eyeHide.hide()
        ui.stacked_widget.setCurrentIndex(0)
        ui.Note_Name.hide()
        ui.Note_Pass.hide()
        ui.Note_User.hide()
        ui.setGeometry(
            round((Main.SCREEN_WIDTH - ui.width()) / 2),
            round((Main.SCREEN_HEIGHT - ui.height()) / 2),
            ui.width(),
            ui.height(),
        )
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_maximize.setToolTip("Phóng to")
        ui.btn_minimize.setToolTip("Thu nhỏ")
        ui.btn_quit.setToolTip("Đóng")
        self.connect_btn(ui)
        self.check_autosave(ui)

    def connect_btn(self, ui):

        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_quit.clicked.connect(lambda: self.openQuitFrame(ui))

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
        ui.ConvertButton.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))

        ui.ConvertButton_SU.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(0)
        )
        ui.ConvertButton_4.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.ConvertButton.clicked.connect(lambda: self.default(ui))

    def default(self, ui):
        ui.STATE_ECHOPASS = True
        ui.PassBox.clear()
        ui.NameBox.clear()
        ui.UserBox.clear()
        ui.Note_Name.hide()
        ui.Note_Pass.hide()
        ui.Note_User.hide()
        ui.student.setChecked(True)

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="53K73q3Z6I",
            password="DpXgsUvOuu",
            database="53K73q3Z6I",
        )

        return connection

    def openQuitFrame(self, ui):
        ui.switch_window_quit.emit()

    def check_autosave(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        time.sleep(1)
        with open(self.USER_PATH, encoding="utf-8") as f:
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
        connection = self.get_connection()
        cursor = connection.cursor()
        username = ui.NameBox_SI.text()[:31]
        password = ui.PassBox_SI.text()[:22]

        if len(password) * len(username) == 0:
            ui.frameError.show()
            ui.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        else:
            cursor.execute("SELECT Username FROM user WHERE Username = %s", (username,))
            if username not in [row[0] for row in cursor]:
                ui.frameError.show()
                ui.Error_Content.setText("Tên tài khoản không tồn tại. Hãy nhập lại.")
            else:
                cursor.execute(
                    "SELECT Username, Password FROM user WHERE Username = %s AND Password = %s",
                    (username, password),
                )
                if not [row[0] for row in cursor]:
                    ui.frameError.show()
                    ui.Error_Content.setText("Mật khẩu không chính xác. Hãy nhập lại.")
                else:
                    cursor.execute(
                        f"SELECT ShowName, Password, Type FROM user WHERE Username = '{username}'"
                    )
                    name, password, role = (
                        row[i] for row in cursor for i in range(len(row))
                    )

                    decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
                    with open(self.USER_PATH, "w", encoding="utf-8") as f:
                        f.write(f"{username}\n")
                        f.write(f"{name}\n")
                        f.write(f"{password}\n")
                        f.write("True" if ui.SavePass.isChecked() else "False")
                    encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
                    connection.close()
                    self.open_main(ui, role)

                QtCore.QTimer.singleShot(3000, lambda: ui.frameError.hide())

    def open_main(self, ui, role):
        ui.switch_window_main.emit(role)

    def check_SU(self, ui):
        connection = self.get_connection()
        cursor = connection.cursor()
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
            cursor.execute("SELECT Username FROM user WHERE Username = %s", (username,))
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
            if not "".join([i for i in name.lower() if i not in self.enabled]) == "":
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
            cursor.execute(
                "INSERT INTO user(Username, ShowName, Password, Type) VALUES(%s, %s, %s, %s)",
                (username, name, password, role),
            )
            connection.commit()
            connection.close()

            ui.NameBox_SI.clear()
            ui.PassBox_SI.clear()
            ui.SavePass.setChecked(False)
            ui.stacked_widget.setCurrentIndex(2)
