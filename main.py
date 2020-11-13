import os
import pickle
import subprocess
import sys

import win32con
import win32gui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizeGrip,
    QWidget,
)
from win32api import GetSystemMetrics

from edit_main import EditWindow
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self, role):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("UI Files/ui_main.ui", self)
        self.role = role
        UIFunctions.uiDefinitions(self)


class UIFunctions(MainWindow):
    @classmethod
    def uiDefinitions(cls, self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.bg_frame.setGraphicsEffect(self.shadow)

        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: cls.close_pg(self))

        # UIFunctions.open_vscode()

        UIFunctions.load_assignments(self, "data/assignments.txt")
        self.list_assignments.itemActivated.connect(
            lambda: UIFunctions.load_details(self, "data/assignment_details.list")
        )

        UIFunctions.define_role(self)

    @classmethod
    def open_vscode(cls):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        cls.pg = win32gui.FindWindow(None, "Visual Studio Code")
        x0, y0, x1, y1 = win32gui.GetWindowRect(cls.pg)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(cls.pg, 0, 0, w + 45, h, True)

    @classmethod
    def close_pg(cls, self):
        try:
            win32gui.PostMessage(cls.pg, win32con.WM_CLOSE, 0, 0)
        except:
            pass

        self.close()

    @classmethod
    def load_assignments(cls, self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.list_assignments.addItem(line.rstrip("\n"))

    @classmethod
    def load_details(cls, self, filename):
        with open(filename, "rb") as f:
            details = pickle.load(f)
            self.assignment_details.setText(
                details[self.list_assignments.currentRow()].rstrip("\n")
            )

    @classmethod
    def define_role(cls, self):
        if self.role.lower() == "teacher":
            cls.teacher_gui_config(self)
        if self.role.lower() == "student":
            cls.student_gui_config(self)

    @classmethod
    def teacher_gui_config(cls, self):
        self.main_btn.setText("Sửa đổi")
        self.main_btn.setStyleSheet(
            """QPushButton {background-color: rgb(59, 143, 14);}
        QPushButton:hover {background-color: rgba(59, 143, 14, 150);}"""
        )
        self.main_btn.clicked.connect(lambda: open_edit_form())

        self.assignment_details.setReadOnly(False)
        self.confirmButton = QDialogButtonBox(self.frame_content_hint)
        self.confirmButton.setStandardButtons(QDialogButtonBox.Ok)
        self.confirmButton.setObjectName("confirmButton")
        self.verticalLayout_4.addWidget(self.confirmButton)
        self.confirmButton.accepted.connect(
            lambda: save_text("assignment_details.list")
        )

        def save_text(filename):
            save_text.changed = True
            with open(filename, "rb") as f:
                save_text.details = pickle.load(f)
            if (
                save_text.details[self.list_assignments.currentRow()]
                != self.assignment_details.toPlainText()
            ):
                show_confirm_mess(filename)
            save_text.details[
                self.list_assignments.currentRow()
            ] = self.assignment_details.toPlainText()
            if save_text.changed:
                with open(filename, "wb") as f:
                    pickle.dump(save_text.details, f)
            else:
                cls.load_details(self, filename)

        def show_confirm_mess(filename):
            msg = QMessageBox()
            msg.setWindowTitle("Thành công sửa đổi bài tập")
            msg.setText("Chi tiết câu đã được chỉnh sửa")
            with open(filename) as f:
                msg.setDetailedText(
                    f"Chi tiết gốc:\n{save_text.details[self.list_assignments.currentRow()]}\n\nChi tiết sau khi sửa đổi:\n{self.assignment_details.toPlainText()}"
                )
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(popup_button)
            msg.exec_()

        def popup_button(i):
            save_text.changed = False if i.text().lower() == "cancel" else True

        def open_edit_form():
            window = EditWindow()
            window.show()

    @classmethod
    def student_gui_config(cls, self):
        self.main_btn.setText("Kiểm tra")
        self.main_btn.setStyleSheet(
            """QPushButton {background-color: rgb(224, 150, 0);}
        QPushButton:hover {background-color: rgba(224, 150, 0, 150);}"""
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # role = 'student'
    role = "teacher"
    window = MainWindow(role)
    window.move(GetSystemMetrics(0) - 300, 0)
    window.show()
    sys.exit(app.exec_())

