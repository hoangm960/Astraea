from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from utils.encryption import decrypt, encrypt
from path import KEY_PATH, OPENED_ASSIGNMENT_PATH, USER_PATH, USER_PATH_ENCRYPTED

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
        open(OPENED_ASSIGNMENT_PATH, mode='w',encoding="utf8").write('')
        ui.switch_window_login.emit()
    
    def Update(self, ui):
        decrypt(USER_PATH_ENCRYPTED, USER_PATH, KEY_PATH)
        with open(USER_PATH, 'r', encoding='utf-8') as f:
            username, name, password = (line.rstrip() for line in f.readlines()[:-1])
            ui.username_box.setText(username)
            ui.NameBox.setText(name)
            ui.PassBox.setText(password)
        encrypt(USER_PATH, USER_PATH_ENCRYPTED, KEY_PATH)
