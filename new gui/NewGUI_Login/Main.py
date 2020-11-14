from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QWidget
import sys
from Login_gui import Ui_MainWindow
from Loading_Screen import Ui_Loading_Screen
from PyQt5.QtCore import Qt

GLOBAL_STATE = False
counter = 0
#</>-------------------
class Loading_Screen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_Loading_Screen()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)
        self.show()
    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        screen = app.primaryScreen()
        size = screen.size()    
        self.ui.OkCancelFrame.hide()
        self.ui.Accept.clicked.connect(lambda: self.close())
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
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_quit.clicked.connect(lambda: self.ui.OkCancelFrame.show())        
        self.sizegrip = QSizeGrip(self.ui.frame_grip)
        self.sizegrip.setStyleSheet("QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}")
        self.sizegrip.setToolTip("This was locked")
        #</>
        self.ui.SignIn_Bt.clicked.connect(lambda: self.check_SI())
        self.ui.SignUp_Bt.clicked.connect(lambda: self.check_SU())
        self.ui.Complete_Frame.hide()    
        self.ui.SignUp_Frame.hide()
        self.Default_Check()
    def Default_Check(self): 
        self.ui.frameError.hide()
        self.ui.Error_PassRan.hide()
        self.ui.Error_NameRan.hide() 
        self.ui.Error_SpecialCr.hide()    
        self.ui.Error_NamePass.hide()

    def check_SI(self):
        self.Default_Check()
        name = self.ui.NameBox_SI.text().lower()
        password = self.ui.PassBox_SI.text().lower()
        if name == '' or password == '':
            self.ui.frameError.show()
            self.ui.Error_NamePass.show()    
     
    def check_SU(self):
        check = True
        self.Default_Check()
        name = self.ui.NameBox_SU.text().lower()
        password = self.ui.PassBox_SU.text().lower()
        if len(name)<6:
            self.ui.frameError.show()
            self.ui.Error_NameRan.show()
            check = False
        elif len(password)<3:
            self.ui.Error_PassRan.show()
            self.ui.frameError.show()
            check = False
        else:
            for word in name:
                if word not in 'qwertyuiopasdfghjklzxcvbnm1234567890 ':
                    self.ui.frameError.show()
                    self.ui.Error_SpecialCr.show()
                    check = False     
                else:
                    for word in password:
                        if word not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                            self.ui.Error_SpecialCr.show()
                            self.ui.frameError.show()
                            check = False
        if check == True:
            self.ui.SignUp_Frame.hide()
            self.ui.Complete_Frame.show()

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    splash_window = Loading_Screen()
    splash_window.show()
    screen = app.primaryScreen()
    size = screen.size()
    splash_window.move(round(size.width()/4), round(size.height()/4))
    sys.exit(app.exec_())
