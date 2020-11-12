import os
import subprocess
import sys

import win32con
import win32gui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QDialogButtonBox,
                             QGraphicsDropShadowEffect, QMainWindow, QMessageBox,
                             QPushButton, QSizeGrip, QWidget)

from main import *
from ui_main import Ui_MainWindow
import pickle
from edit_form import Ui_EditWindow


class MainWindow(QMainWindow):
    def __init__(self, role):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.role = role
        UIFunctions.uiDefinitions(self)


class UIFunctions(MainWindow):
    pg = None

    def uiDefinitions(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.ui.bg_frame.setGraphicsEffect(self.shadow)

        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_quit.clicked.connect(lambda: UIFunctions.close_pg(self))

        # UIFunctions.open_vscode()
        UIFunctions.load_assignments(self, "assignments.txt")
        self.ui.list_assignments.itemActivated.connect(lambda: UIFunctions.load_details(self, 'assignment_details.list'))

        UIFunctions.define_role(self)
        

    @classmethod
    def open_vscode(cls):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        cls.pg = win32gui.FindWindow(None, 'Visual Studio Code')
        x0, y0, x1, y1 = win32gui.GetWindowRect(cls.pg)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(cls.pg, 0, 0, w + 50, h, True)

    @classmethod
    def close_pg(cls, self):
        if cls.pg:
            win32gui.PostMessage(cls.pg, win32con.WM_CLOSE,0,0)
        self.close()

    @classmethod
    def load_assignments(cls, self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.ui.list_assignments.addItem(line.rstrip("\n"))
    
    @classmethod
    def load_details(cls, self, filename):
        with open(filename, 'rb') as f:
            details = pickle.load(f)
            self.ui.assignment_details.setText(details[self.ui.list_assignments.currentRow()].rstrip('\n'))

    @classmethod
    def define_role(cls, self):
        if self.role.lower() == 'teacher':
            cls.teacher_gui_config(self)
        if self.role.lower() == 'student':
            cls.student_gui_config(self)
    
    @classmethod
    def teacher_gui_config(cls, self):
        self.ui.main_btn.setText('Sửa đổi')
        self.ui.main_btn.setStyleSheet('''QPushButton {background-color: rgb(59, 143, 14);}
        QPushButton:hover {background-color: rgba(59, 143, 14, 150);}''')
        self.ui.main_btn.clicked.connect(lambda: open_edit_form())

        self.ui.assignment_details.setReadOnly(False)
        self.ui.confirmButton = QDialogButtonBox(self.ui.frame_content_hint)
        self.ui.confirmButton.setStandardButtons(QDialogButtonBox.Ok)
        self.ui.confirmButton.setObjectName("confirmButton")
        self.ui.verticalLayout_4.addWidget(self.ui.confirmButton)
        self.ui.confirmButton.accepted.connect(lambda: save_text('assignment_details.list'))
        
        def save_text(filename):
            save_text.changed = True
            with open(filename, 'rb') as f:
                save_text.details = pickle.load(f)
            if save_text.details[self.ui.list_assignments.currentRow()] != self.ui.assignment_details.toPlainText():
                show_confirm_mess(filename)
            save_text.details[self.ui.list_assignments.currentRow()] = self.ui.assignment_details.toPlainText()
            if save_text.changed:
                with open(filename, 'wb') as f:    
                    pickle.dump(save_text.details, f)
            else:
                cls.load_details(self, filename)


        def show_confirm_mess(filename):
            msg = QMessageBox()
            msg.setWindowTitle("Thành công sửa đổi bài tập")
            msg.setText("Chi tiết câu đã được chỉnh sửa")
            with open(filename) as f:
                msg.setDetailedText(f'Chi tiết gốc:\n{save_text.details[self.ui.list_assignments.currentRow()]}\n\nChi tiết sau khi sửa đổi:\n{self.ui.assignment_details.toPlainText()}')
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
            msg.buttonClicked.connect(popup_button)
            msg.exec_()

        def popup_button(i):
            save_text.changed = False if i.text().lower() == "cancel" else True

        class UIFunctions(MainWindow):
            GLOBAL_STATE = False

            @classmethod
            def maximize_restore(cls, self):
                status = cls.GLOBAL_STATE

                if status == False:
                    self.showMaximized()

                    cls.GLOBAL_STATE = True
                    
                    self.ui.bg_layout.setContentsMargins(0, 0, 0, 0)
                    self.ui.bg_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 0px;")
                    self.ui.btn_maximize.setToolTip("Restore")
                else:
                    cls.GLOBAL_STATE = False
                    self.showNormal()
                    self.resize(self.width() + 1, self.height() + 1)
                    self.ui.bg_layout.setContentsMargins(10, 10, 10, 10)
                    self.ui.bg_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 20px;")
                    self.ui.btn_maximize.setToolTip("Maximize")

            @classmethod
            def uiDefinitions(cls, self):
                self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

                self.shadow = QGraphicsDropShadowEffect(self)
                self.shadow.setBlurRadius(20)
                self.shadow.setXOffset(0)
                self.shadow.setYOffset(0)
                self.shadow.setColor(QColor(0, 0, 0, 100))
                self.ui.bg_frame.setGraphicsEffect(self.shadow)

                self.ui.btn_maximize.clicked.connect(lambda: UIFunctions.maximize_restore(self))
                self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
                self.ui.btn_quit.clicked.connect(lambda: self.close())

                self.sizegrip = QSizeGrip(self.ui.frame_grip)
                self.sizegrip.setStyleSheet("QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }")
                self.sizegrip.setToolTip("Resize Window")

            @classmethod
            def returnStatus(cls):
                return cls.GLOBAL_STATE

        class EditWindow(QMainWindow):
            def __init__(self):
                QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
                self.ui = Ui_EditWindow()
                self.ui.setupUi(self)

                def moveWindow(event):
                    if UIFunctions.returnStatus() == True:
                        UIFunctions.maximize_restore(self)
                    if event.buttons() == Qt.LeftButton:
                        self.move(self.pos() + event.globalPos() - self.dragPos)
                        self.dragPos = event.globalPos()
                        event.accept()

                self.ui.title_bar.mouseMoveEvent = moveWindow

                UIFunctions.uiDefinitions(self)


            def mousePressEvent(self, event):
                self.dragPos = event.globalPos()

        def open_edit_form():
            window = EditWindow()
            window.show()

    @classmethod
    def student_gui_config(cls, self):
        self.ui.main_btn.setText('Kiểm tra')
        self.ui.main_btn.setStyleSheet('''QPushButton {background-color: rgb(224, 150, 0);}
        QPushButton:hover {background-color: rgba(224, 150, 0, 150);}''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # role = 'student'
    role = 'teacher'
    window = MainWindow(role)
    window.move(1070, 0)
    window.show()
    sys.exit(app.exec_())

