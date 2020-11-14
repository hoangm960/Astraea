from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from win32api import GetSystemMetrics
import main_ui


class LoginWindow(QMainWindow):
    GLOBAL_STATE = False

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_Files/Login_gui.ui", self)
        self.OkCancelFrame.hide()
        self.Accept.clicked.connect(lambda: self.close())
        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # <> Set Toolbar Button

        def State_change_size():
            self.GLOBAL_STATE
            if self.GLOBAL_STATE == False:
                self.GLOBAL_STATE = True
                self.showFullScreen()
            else:
                self.GLOBAL_STATE = False
                self.showNormal()

        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())

        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}"
        )
        self.sizegrip.setToolTip("This was locked")

        self.SignIn_Bt.clicked.connect(lambda: self.check_SI())
        self.SignUp_Bt.clicked.connect(lambda: self.check_SU())

        self.Complete_Frame.hide()
        self.SignUp_Frame.hide()
        self.Default_Check()

    def Default_Check(self):
        self.frameError.hide()
        self.Error_PassRan.hide()
        self.Error_NameRan.hide()
        self.Error_SpecialCr.hide()
        self.Error_NamePass.hide()

    def check_SI(self):
        self.Default_Check()
        name = self.NameBox_SI.text().lower()
        password = self.PassBox_SI.text().lower()
        if name == "" or password == "":
            self.frameError.show()
            self.Error_NamePass.show()
        else:
            self.close()
            main_ui.main()

    def check_SU(self):
        check = True
        self.Default_Check()
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        if len(name) < 6:
            self.frameError.show()
            self.Error_NameRan.show()
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
        if check == True:
            self.SignUp_Frame.hide()
            self.Complete_Frame.show()


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
        self.timer.start(20)
        self.show()

    def progress(self):
        self.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            self.main = LoginWindow()
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
