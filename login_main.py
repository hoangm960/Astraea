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


class User:
    def __init__(self, name, password, role, auto_saved):
        self.name = name
        self.password = password
        self.role = role
        self.auto_saved = auto_saved


class LoginWindow(QMainWindow):
    STATE_ECHOPASS = True
    USER_PATH = "data/Users/User.txt"
    UI_PATH = "UI_Files/Login_gui.ui"
    users = []

    def __init__(self):
        QMainWindow.__init__(self)
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

    @classmethod
    def uiDefinitions(cls, self):
        self.OkCancelFrame.hide()
        self.Complete_Frame.hide()
        self.SignUp_Frame.hide()
        self.eyeButton_SU.hide()
        self.eyeButton_SI.hide()
        cls.Default_Check(self)

        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        cls.create_dropshadow(self)
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
        self.ConvertButton.clicked.connect(lambda: default())
        self.ConvertButton_SU.clicked.connect(lambda: default())

        def default():
            self.STATE_ECHOPASS = True

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
            self.showMaximized()

            cls.GLOBAL_STATE = True

            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 0px;"
            )
            self.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 20px;"
            )
            self.btn_maximize.setToolTip("Maximize")

    @classmethod
    def Default_Check(cls, self):
        self.frameError.hide()
        self.Error_PassRan.hide()
        self.Error_NameRan.hide()
        self.Error_SpecialCr.hide()
        self.Error_NamePass.hide()
        self.Error_NameExist.hide()
        self.Error_NamenotExist.hide()
        self.Error_MissPass.hide()

    @classmethod
    def load_users(cls, self):
        cls.users.clear()
        if os.path.getsize(self.USER_PATH) > 0:
            with open(self.USER_PATH, "rb") as f:
                unpickler = pickle.Unpickler(f)
                cls.users = unpickler.load()

    @classmethod
    def check_SI(cls, self):
        cls.Default_Check(self)
        cls.load_users(self)
        name = self.NameBox_SI.text()
        password = self.PassBox_SI.text()
        for user in cls.users:
            if name == "" or password == "":
                self.frameError.show()
                self.Error_NamePass.show()
            elif name not in user.name:
                self.frameError.show()
                self.Error_NamenotExist.show()

            elif password != user.password:
                self.frameError.show()
                self.Error_MissPass.show()

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

    @classmethod
    def check_SU(cls, self):
        check = True
        cls.Default_Check(self)
        cls.load_users(self)
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        for user in cls.users:
            if len(name) < 6:
                self.frameError.show()
                self.Error_NameRan.show()
                check = False

            elif name in user.name:
                self.frameError.show()
                self.Error_NameExist.show()
                check = False

            elif len(password) < 8:
                self.Error_PassRan.show()
                self.frameError.show()
                check = False

            else:
                for word in name:
                    if word not in "qwertyuiopasdfghjklzxcvbnm1234567890 ":
                        self.frameError.show()
                        self.Error_SpecialCr.show()
                        check = False
                    else:
                        for word in password:
                            if word not in "qwertyuiopasdfghjklzxcvbnm1234567890 ":
                                self.Error_SpecialCr.show()
                                self.frameError.show()
                                check = False

        if check:
            with open(self.USER_PATH, "wb") as f:
                name = self.NameBox_SU.text()
                password = self.PassBox_SU.text()
                role = "teacher" if self.Teacher_SU.isChecked() else "student"
                cls.users.append(User(name, password, role, False))
                pickle.dump(cls.users, f)

            self.SignUp_Frame.hide()
            self.Complete_Frame.show()
            self.close


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
        self.counter += 1


def main():
    app = QApplication(sys.argv)
    splash_window = Loading_Screen()
    splash_window.move(round(GetSystemMetrics(0) / 4), round(GetSystemMetrics(1) / 4))
    splash_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
