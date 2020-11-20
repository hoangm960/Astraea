import os
from pathlib import Path
import pickle
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QLayout,
    QListWidgetItem,
    QMainWindow,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)
from PyQt5 import uic
from UI_Files import Resources
from win32api import GetSystemMetrics
import main_ui
from encryption import *

EDIT_FORM_PATH = "UI_Files/edit_form.ui"
EDIT_FRAME_PATH = "UI_Files/edit_frame.ui"
ASSIGNMENTS_PATH = "data/Lesson/assignments.list"


class Assignment:
    def __init__(self, name, test_file, input_file, ans_file, tests, vars, details):
        self.name = name
        self.test_file = test_file
        self.input_file = input_file
        self.ans_file = ans_file
        self.tests = tests
        self.vars = vars
        self.details = details


class EditWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(EDIT_FORM_PATH, self)
        self.setGeometry(
            round((GetSystemMetrics(0) - self.width()) / 2),
            round((GetSystemMetrics(1) - self.height()) / 2),
            self.width(),
            self.height(),
        )

        def moveWindow(event):
            if UIFunctions.returnStatus() == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(EditWindow):
    GLOBAL_STATE = False
    ASSIGNMENTS = []
    list = []

    @classmethod
    def uiDefinitions(cls, ui):
        # Delete title bar
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Make drop shadow
        ui.shadow = QGraphicsDropShadowEffect(ui)
        ui.shadow.setBlurRadius(20)
        ui.shadow.setXOffset(0)
        ui.shadow.setYOffset(0)
        ui.shadow.setColor(QColor(0, 0, 0, 100))
        ui.bg_frame.setGraphicsEffect(ui.shadow)

        # Button function
        ui.btn_maximize.clicked.connect(lambda: cls.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.confirm_btn.clicked.connect(
            lambda: cls.load_assignments(ui, ASSIGNMENTS_PATH)
        )

        # Window size grip
        ui.sizegrip = QSizeGrip(ui.frame_grip)
        ui.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        ui.sizegrip.setToolTip("Resize Window")

        # Change scene
        ui.confirm_button.clicked.connect(lambda: cls.go_to_second(ui))
        ui.return_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.return_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.confirm_add_btn.clicked.connect(lambda: cls.add_frame(ui, int(ui.num_entry_3.text())))
        ui.confirm_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.stacked_widget.setCurrentIndex(0)
        cls.check_empty(ui, ASSIGNMENTS_PATH)

    @classmethod
    def check_empty(cls, ui, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                ui.stacked_widget.setCurrentIndex(1)
                with open(filename, 'rb') as f:
                    unpickler = pickle.Unpickler(f)
                    assignments = unpickler.load()
                    cls.put_frame_in_list(ui, len(assignments))
                    cls.setup_frame(ui, assignments)
                
    @classmethod
    def go_to_second(cls, ui):
        cls.change_lesson_title(ui, ui.name_entry.text())
        cls.put_frame_in_list(ui, ui.num_entry.value())
        ui.stacked_widget.setCurrentIndex(1)

    @classmethod
    def returnStatus(cls):
        return cls.GLOBAL_STATE

    @classmethod
    def maximize_restore(cls, ui):
        status = cls.GLOBAL_STATE

        if status == False:
            ui.showMaximized()

            cls.GLOBAL_STATE = True

            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 0px;"
            )
            ui.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.bg_layout.setContentsMargins(10, 10, 10, 10)
            ui.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 20px;"
            )
            ui.btn_maximize.setToolTip("Maximize")

    class EditFrame(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(EDIT_FRAME_PATH, self)

            self.test_file_btn.clicked.connect(
                lambda: self.showDialog(self.test_file_entry)
            )
            self.input_file_btn.clicked.connect(
                lambda: self.showDialog(self.input_file_entry)
            )
            self.ans_file_btn.clicked.connect(
                lambda: self.showDialog(self.ans_file_entry)
            )

        def showDialog(self, entry):
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(self, "Open file", HOME_PATH)

            if file_name[0]:
                entry.setText(file_name[0])

    @classmethod
    def change_lesson_title(cls, ui, title):
        ui.lesson_title.setText(title if title else "Bài học không tên")

    @classmethod
    def setup_frame(cls, ui, assignments):
        children = ui.content_widget.children()
        i = 1
        for assignment in assignments:
            children[i].title_entry.setText(assignment.name)
            children[i].test_file_entry.setText(assignment.test_file)
            children[i].input_file_entry.setText(assignment.input_file)
            children[i].ans_file_entry.setText(assignment.ans_file)
            children[i].test_num_entry.setValue(assignment.tests)
            children[i].test_var_entry.setValue(assignment.vars)
            children[i].details_entry.setText(assignment.details)
            i += 1

    @classmethod
    def put_frame_in_list(cls, ui, num):
        current_layout = ui.content_widget.layout()
        ui.content_layout = (
            QVBoxLayout(ui.content_widget) if not current_layout else current_layout
        )
        ui.content_layout.setContentsMargins(9, 9, 9, 9)
        for i in reversed(range(ui.content_layout.count())):
            ui.content_layout.itemAt(i).widget().setParent(None)

        ui.scrollArea.verticalScrollBar().setValue(1)

        cls.add_frame(ui, num)

    @classmethod
    def add_frame(cls, ui, num):
        for _ in range(num):
            ui.frame = cls.EditFrame()
            ui.frame.setGeometry(ui.content_layout.geometry())
            ui.content_layout.addWidget(ui.frame)

    @classmethod
    def load_assignments(cls, ui, filename):
        children = ui.content_widget.children()
        assignments = [
            Assignment(
                children[i].title_entry.text(),
                children[i].test_file_entry.text(),
                children[i].input_file_entry.text(),
                children[i].ans_file_entry.text(),
                children[i].test_num_entry.value(),
                children[i].test_var_entry.value(),
                children[i].details_entry.toPlainText()
            )
            for i in range(1, ui.content_layout.count() + 1)
        ]

        with open(filename, "wb") as f:
            pickle.dump(assignments, f)

        main_ui.main("teacher")
        ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow()
    window.show()
    sys.exit(app.exec_())
