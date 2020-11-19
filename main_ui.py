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

import edit_main 
from PyQt5 import uic
from UI_Files import Resources

UI_MAIN_PATH = "UI_Files/ui_main.ui"
ASSIGNMENTS_PATH = "data/Lesson/assignments.list"
DETAILS_PATH = "data/Lesson/assignment_details.list"


class MainWindow(QMainWindow):
    def __init__(self, role):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.role = role
        UIFunctions.uiDefinitions(self)


class UIFunctions(MainWindow):
    @classmethod
    def uiDefinitions(cls, self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 200))
        self.bg_frame.setGraphicsEffect(self.shadow)

        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: cls.close_pg(self))

        # cls.open_vscode()

        cls.load_assignments(self, ASSIGNMENTS_PATH)
        self.list_assignments.itemPressed.connect(
            lambda: cls.load_details(self, DETAILS_PATH)
        )

        cls.define_role(self)

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
        # self.list_assignments.
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    assignments = unpickler.load()
                    for assignment in assignments:
                        self.list_assignments.addItem(assignment)

    @classmethod
    def load_details(cls, self, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    details = unpickler.load()
                    self.assignment_details.setText(
                        details[self.list_assignments.currentRow()]
                    )

    class TeacherUiFunctions:
        @classmethod
        def config(cls, self):
            self.main_btn.setText("Sửa đổi")
            self.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(59, 143, 14);}
            QPushButton:hover {background-color: rgba(59, 143, 14, 150);}"""
            )
            self.main_btn.clicked.connect(lambda: cls.open_edit_form(self))

            self.assignment_details.setReadOnly(False)
            self.confirmButton = QDialogButtonBox(self.frame_content_hint)
            self.confirmButton.setStandardButtons(QDialogButtonBox.Ok)
            self.confirmButton.setObjectName("confirmButton")
            self.verticalLayout_4.addWidget(self.confirmButton)
            self.confirmButton.accepted.connect(
                lambda: cls.save_text(self, DETAILS_PATH)
            )

        @classmethod
        def save_text(cls, self, filename):
            cls.changed = True
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                cls.details = unpickler.load()
            if (
                cls.details[self.list_assignments.currentRow()]
                != self.assignment_details.toPlainText()
            ):
                cls.show_confirm_mess(self, filename)
            cls.details[
                self.list_assignments.currentRow()
            ] = self.assignment_details.toPlainText()
            if cls.changed:
                with open(filename, "wb") as f:
                    pickle.dump(cls.details, f)
            else:
                cls.load_details(self, filename)

        @classmethod
        def show_confirm_mess(cls, self, filename):
            msg = QMessageBox()
            msg.setWindowTitle("Thành công sửa đổi bài tập")
            msg.setText("Chi tiết câu đã được chỉnh sửa")
            with open(filename) as f:
                msg.setDetailedText(
                    f"Chi tiết gốc:\n{cls.details[self.list_assignments.currentRow()]}\n\nChi tiết sau khi sửa đổi:\n{self.assignment_details.toPlainText()}"
                )
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(cls.popup_button)
            msg.exec_()

        @classmethod
        def popup_button(cls, i):
            cls.changed = False if i.text().lower() == "cancel" else True

        @classmethod
        def open_edit_form(cls, self):
            window = edit_main.EditWindow(self)
            window.show()

    class StudentUiFunctions:
        @classmethod
        def student_gui_config(cls, self):
            self.main_btn.setText("Kiểm tra")
            self.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(224, 150, 0);}
            QPushButton:hover {background-color: rgba(224, 150, 0, 150);}"""
            )
            self.main_btn.clicked.connect(lambda: result_main.open_result_form())
    @classmethod
    def define_role(cls, self):
        if self.role.lower() == "teacher":
            cls.TeacherUiFunctions.config(self)
        if self.role.lower() == "student":
            cls.StudentUiFunctions.student_gui_config(self)


def main(role):
    window = MainWindow(role)
    window.move(GetSystemMetrics(0) - window.width(), 0)
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main("teacher")
    sys.exit(app.exec_())
