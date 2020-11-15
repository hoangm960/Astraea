from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip, QWidget
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from win32api import GetSystemMetrics
import main_ui

state_echoPass = True
class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI_Files/Login_gui.ui", self)
        self.OkCancelFrame.hide()
        self.Accept.clicked.connect(lambda: self.close())
        self.move(round(GetSystemMetrics(0) / 10), round(GetSystemMetrics(1) / 50))
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        #<> Set Toolbar Button
        # def State_change_size():
        #     global GLOBAL_STATE
        #     if GLOBAL_STATE == False:
        #         GLOBAL_STATE = True
        #         self.showFullScreen()
        #     else:
        #         GLOBAL_STATE = False
        #         self.showNormal()
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.OkCancelFrame.show())
        self.eyeButton_SU.hide()
        self.eyeButton_SI.hide()
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { background-color: none; width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(66, 0, 99);}"
        )
        self.sizegrip.setToolTip("This was locked")
        self.eyeButton_SI.clicked.connect(lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password))
        self.eyeButton_SU.clicked.connect(lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Password))
        self.eyeButton_SI_2.clicked.connect(lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal))
        self.eyeButton_SU_2.clicked.connect(lambda: self.PassBox_SU.setEchoMode(QtWidgets.QLineEdit.Normal))
        self.SignIn_Bt.clicked.connect(lambda: self.check_SI())
        self.SignUp_Bt.clicked.connect(lambda: self.check_SU())
        def default():
            global state_echoPass
            state_echoPass = True
        self.ConvertButton.clicked.connect(lambda: default())
        self.ConvertButton_SU.clicked.connect(lambda: default())
        self.check_data()
        with open("New_Data/AutoSave.txt",'a+') as file:
            file.close()
        with open("New_Data/AutoSave.txt", 'r') as file:
            data_name = file.readline().replace('\n','')
            if data_name != '':
                self.NameBox_SI.setText(data_name)
                self.PassBox_SI.setText(self.account_data[data_name])
                self.SavePass.setChecked(True)
            file.close()

        self.Complete_Frame.hide()
        self.SignUp_Frame.hide()
        self.Default_Check()
    #Check information from: User.txt
    def check_data(self):   
        self.account_data = dict()
        with open("New_Data/User.txt", "a+") as file:
            file.close()
        with open("New_Data/User.txt", 'r', encoding = 'utf8') as file:
            while True:
                data_name = file.readline().replace('\n','')
                if data_name == '':
                    break
                data_password = file.readline().replace('\n','')
                self.account_data[data_name] = data_password
            file.close()
    #complete
        
    def Default_Check(self): 
        self.frameError.hide()
        self.Error_PassRan.hide()
        self.Error_NameRan.hide()
        self.Error_SpecialCr.hide()
        self.Error_NamePass.hide()
        self.Error_NameExist.hide()
        self.Error_NamenotExist.hide()
        self.Error_MissPass.hide()
    #Check your signing in >>
    def check_SI(self):
        self.check_data()
        self.Default_Check()
        name = self.NameBox_SI.text()
        password = self.PassBox_SI.text()
        if name == '' or password == '':
            self.frameError.show()
            self.Error_NamePass.show()
        elif name not in self.account_data.keys():
            self.frameError.show()
            self.Error_NamenotExist.show()
        elif password != self.account_data[name]:
            self.frameError.show()
            self.Error_MissPass.show()
        else:
            if self.SavePass.isChecked():
                with open("New_Data/AutoSave.txt","w") as file_write:
                    file_write.write(name)
                    file_write.close()
            self.close() 
            main_ui.main()

    #Check your signing up"
    def check_SU(self):
        check = True
        self.check_data()
        self.Default_Check()
        name = self.NameBox_SU.text().lower()
        password = self.PassBox_SU.text().lower()
        if len(name) < 6:
            self.frameError.show()
            self.Error_NameRan.show()
            check = False
        elif name in self.account_data.keys():
            self.frameError.show()
            self.Error_NameExist.show()
            check = False
        elif len(password)<3:
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
            with open('New_Data/User.txt','a+') as file_write:
                name = self.NameBox_SU.text() + '\n'
                password = self.PassBox_SU.text() + '\n'
                file_write.write(name)
                file_write.write(password)
                file_write.close()
            self.SignUp_Frame.hide()
            self.Complete_Frame.show()
            with open('New_Data/Teacher_User.txt','a+') as file_write:
                if self.Teacher_SU.isChecked():
                    file_write.write(name)
                file_write.close()
                
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