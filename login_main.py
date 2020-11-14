from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic

GLOBAL_STATE = False
counter = 0
#</>-------------------
class Loading_Screen(QMainWindow):
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
        global counter
        self.progressBar.setValue(counter)
        if counter>100:
            self.timer.stop()
            self.main = LoginWindow()
            self.main.show()
            self.close()
        counter += 1
#</>------------------

class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_Files/Login_gui.ui", self)
        screen = app.primaryScreen()
        size = screen.size()    
        self.OkCancelFrame.hide()
        self.Accept.clicked.connect(lambda: self.close())
        self.move(round(size.width()/10), round(size.height()/50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        #<> Set Toolbar Button
        GLOBAL_STATE = False
        def State_change_size():
            global GLOBAL_STATE
            if GLOBAL_STATE == False:
                GLOBAL_STATE = True
                self.showFullScreen()
            else:
                GLOBAL_STATE = False
                self.showNormal()
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())        
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet("QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}")
        self.sizegrip.setToolTip("This was locked")
        #</>
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
        if name == '' or password == '':
            self.frameError.show()
            self.Error_NamePass.show()    
     
    def check_SU(self):
        check = True
        self.Default_Check()
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        if len(name)<6:
            self.frameError.show()
            self.Error_NameRan.show()
            check = False
        elif len(password)<3:
            self.Error_PassRan.show()
            self.frameError.show()
            check = False
        else:
            for word in name:
                if word not in 'qwertyuiopasdfghjklzxcvbnm1234567890 ':
                    self.frameError.show()
                    self.Error_SpecialCr.show()
                    check = False     
                else:
                    for word in password:
                        if word not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                            self.Error_SpecialCr.show()
                            self.frameError.show()
                            check = False
        if check == True:
            self.SignUp_Frame.hide()
            self.Complete_Frame.show()

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    splash_window = Loading_Screen()
    splash_window.show()
    screen = app.primaryScreen()
    size = screen.size()
    splash_window.move(round(size.width()/4), round(size.height()/4))
    sys.exit(app.exec_())
