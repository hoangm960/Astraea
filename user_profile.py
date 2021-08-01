from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from encryption import decrypt, encrypt


class ProfileWindow(QMainWindow):
    UI_PATH = './UI_Files/profile_form.ui'
    switch_window_main = QtCore.pyqtSignal()
    switch_window_login = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        UIFunctions(self)

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

    def __init__(self, ui):
        self.connect_btn(ui)
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))

    def connect_btn(self, ui):
        ui.OutAccount.clicked.connect(lambda: self.SignOut(ui))
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        self.Update(ui)

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
