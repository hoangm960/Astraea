from encryption import decrypt, encrypt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys

class ProfileWindow(QMainWindow):
    UI_PATH = './UI_Files/profile_form.ui'

    def __init__(self, ui, pg):
        self.ui = ui
        self.pg = pg
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_PATH, self)
        UIFunctions.uiDefinitions(self)

        def moveWindow(event):
            if UIFunctions.GLOBAL_STATE == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.TitleBar.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(ProfileWindow):
    GLOBAL_STATE = False
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"

    @classmethod
    def uiDefinitions(cls, ui):
        cls.connect_btn(ui)

    @classmethod
    def connect_btn(cls, ui):
        def SignOut(ui):
            if ui.ui:
                ui.ui.close()
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
        ui.btn_maximize.clicked.connect(lambda: cls.maximize_restore(ui))
        cls.Update(ui)
        ui.Save_btn.setDisabled(True)

    @classmethod
    def maximize_restore(cls, self):
        status = cls.GLOBAL_STATE
        if status == False:
            self.showMaximized()

            cls.GLOBAL_STATE = True
            self.centralwidget.setStyleSheet("""background-color: rgb(74, 74, 74);
border-radius: 0px;""")
            self.btn_maximize.setToolTip("khôi phục")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.centralwidget.setStyleSheet("""background-color: rgb(74, 74, 74);
border-radius: 20px;""")
            self.btn_maximize.setToolTip("Phóng to")

    def Update(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        with open(self.USER_PATH, 'r', encoding='utf-8') as f:
            username, name, password = (line.rstrip()
                                        for line in f.readlines())
            ui.username_box.setText(username)
            ui.NameBox.setText(name)
            ui.PassBox.setText(password)
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileWindow(None, None)
    window.show()
    sys.exit(app.exec_())
