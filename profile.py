from encryption import decrypt, encrypt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys

class ProfileWindow(QMainWindow):
    UI_PATH = './UI_Files/profile_form.ui'

    def __init__(self, window, pg):
        self.win = window
        self.pg = pg
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        UIFunctions(self, self.win)

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.TitleBar.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(ProfileWindow):
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    KEY_PATH = "data/encryption/users.key"

    def __init__(self, ui, win):
        self.connect_btn(ui)
        if win:
            win.profile_btn.setDisabled(True)
        ui.btn_quit.clicked.connect(lambda: win.profile_btn.setDisabled(False))
    def connect_btn(self, ui):
        def SignOut(ui):
            if ui.win:
                ui.win.close()
            ui.close()
            if ui.pg:
                ui.pg.minimize()
            import login_main

            ui.main = login_main.LoginWindow(ui.pg)
            ui.main.show()
        ui.OutAccount.clicked.connect(lambda: SignOut(ui))
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        self.Update(ui)

    
    def Update(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            username, name, password = (line.rstrip() for line in f.readlines()[:-1])
            ui.username_box.setText(username)
            ui.NameBox.setText(name)
            ui.PassBox.setText(password)
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileWindow(None, None, None)
    window.show()
    sys.exit(app.exec_())
