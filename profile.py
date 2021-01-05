from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import mysql.connector

UI_PATH = './UI_Files/profile_form.ui'
USER_PATH = './data/Users/opened_user.ou'
class ProfileWindow(QMainWindow):
    def __init__(self, ui, pg, connection):
        self.ui = ui
        self.pg = pg
        self.connection = connection
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
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

    @staticmethod 
    def Update(ui):
        with open(USER_PATH, 'r', encoding = 'utf-8') as f:
            username, name, password = (line.rstrip() for line in f.readlines())
            ui.username_box.setText(username)
            ui.NameBox.setText(name)
            ui.PassBox.setText(password)
            


if __name__ == '__main__':
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    window = ProfileWindow(None, None, connection)
    window.show()
    sys.exit(app.exec_())

