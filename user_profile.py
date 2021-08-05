from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from encryption import decrypt, encrypt

UI_PATH = './UI_Files/profile_form.ui'

class ProfileWindow(QMainWindow):
    switch_window_main = QtCore.pyqtSignal()
    switch_window_login = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        self.init_UI()
        UIFunctions(self)

    def init_UI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.TitleBar.mouseMoveEvent = self.moveWindow

    def moveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(ProfileWindow):
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    KEY_PATH = "data/encryption/users.key"

    def __init__(self, ui):
        self.connect_btn(ui)
        self.Update(ui)

    def connect_btn(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))
        ui.OutAccount.clicked.connect(lambda: self.SignOut(ui))
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())

    def return_main(self, ui):
        ui.switch_window_main.emit()

    def SignOut(self, ui):
        ui.switch_window_login.emit()
    
    def Update(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            username, name, password = (line.rstrip() for line in f.readlines()[:-1])
            ui.username_box.setText(username)
            ui.NameBox.setText(name)
            ui.PassBox.setText(password)
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
