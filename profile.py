from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys

UI_PATH = './UI_Files/profile_form.ui'
USER_PATH = './data/Users/opened_user.ou'
class ProfileWindow(QMainWindow):
    def __init__(self, ui, pg):
        self.ui = ui
        self.pg = pg
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
    def uiDefinitions(cls, Ui):
        cls.connect_btn(Ui)        
    @classmethod    
    def connect_btn(cls, Ui): 
        def SignOut(Ui):
            if Ui.ui:
                Ui.ui.close()
            Ui.close()
            if Ui.pg:
                Ui.pg.minimize()
            import login_main
            
            Ui.main = login_main.LoginWindow(Ui.pg)
            Ui.main.show()           
        Ui.OutAccount.clicked.connect(lambda: SignOut(Ui))
        
        Ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        Ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Ui.btn_quit.clicked.connect(lambda: Ui.close())
        Ui.btn_minimize.clicked.connect(lambda: Ui.showMinimized())
        Ui.btn_maximize.clicked.connect(lambda: cls.maximize_restore(Ui))
        cls.Update(Ui)
        Ui.Save_btn.setDisabled(True)
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
    @classmethod 
    def Update(cls, Ui):
        with open(USER_PATH, 'r', encoding = 'utf-8') as f:
            name = f.readline().rstrip()
            Ui.NameBox.setText(name)
            id = f.readline().rstrip()
            Ui.IDBox.setText(id)
            password = f.readline().rstrip()
            Ui.PassBox.setText(password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileWindow(None, None)
    window.show()
    sys.exit(app.exec_())

