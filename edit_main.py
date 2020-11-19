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
    QSizeGrip, QVBoxLayout,
    QWidget,
)
from PyQt5 import uic
from UI_Files import Resources
from win32api import GetSystemMetrics
import main_ui

EDIT_FORM_PATH = "UI_Files/edit_form.ui"
EDIT_FRAME_PATH = "UI_Files/edit_frame.ui"
ASSIGNMENTS_PATH = "data/Lesson/assignments.list"


class Assignment:
    def __init__(self, name, test_file, input_file, ans_file, tests, vars):
        self.name = name
        self.test_file = test_file
        self.input_file = input_file
        self.ans_file = ans_file
        self.tests = tests
        self.vars = vars


class EditWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(EDIT_FORM_PATH, self)
        self.setGeometry(
            round((GetSystemMetrics(0) - self.width()) / 3),
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
    def uiDefinitions(cls, self):
        # Delete title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Make drop shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.bg_frame.setGraphicsEffect(self.shadow)

        # Button function
        self.btn_maximize.clicked.connect(lambda: cls.maximize_restore(self))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.close())
        self.confirm_btn.clicked.connect(lambda: cls.load_assignments(self, ASSIGNMENTS_PATH))

        # Window size grip
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")

        # Change scene
        self.confirm_button.clicked.connect(lambda: cls.go_to_second(self))
        self.return_btn.clicked.connect(lambda: cls.return_to_first(self))
        self.stacked_widget.setCurrentIndex(0)

    @classmethod
    def go_to_second(cls, self):
        cls.change_lesson_title(self, self.name_entry.text())
        cls.put_frame_in_list(self, self.num_entry.value())
        self.stacked_widget.setCurrentIndex(1)

    @classmethod
    def returnStatus(cls):
        return cls.GLOBAL_STATE

    @classmethod
    def maximize_restore(cls, self):
        status = cls.GLOBAL_STATE

        if status == False:
            self.showMaximized()

            cls.GLOBAL_STATE = True

            self.bg_layout.setContentsMargins(0, 0, 0, 0)
            self.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 0px;"
            )
            self.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.bg_layout.setContentsMargins(10, 10, 10, 10)
            self.bg_frame.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 20px;"
            )
            self.btn_maximize.setToolTip("Maximize")

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
    def change_lesson_title(cls, self, title):
        self.lesson_title.setText(title if title else "Bài học không tên")

    @classmethod
    def put_frame_in_list(cls, self, num):
        current_layout = self.content_widget.layout()
        self.content_layout = QVBoxLayout(self.content_widget) if not current_layout else current_layout
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)
        
        self.scrollArea.verticalScrollBar().setValue(1)
        
        for _ in range(num):
            self.frame = cls.EditFrame()
            self.content_layout.addWidget(self.frame)

    @classmethod
    def return_to_first(cls, self):
        # self.content_widget.layout().delete()
        self.stacked_widget.setCurrentIndex(0)

    @classmethod
    def load_assignments(cls, self, filename):
        assignment_names = [
            self.content_widget.children()[i].title_entry.text()
            for i in range(1, self.content_layout.count() + 1)
        ]
        with open(filename, "wb") as f:
            pickle.dump(assignment_names, f)

        main_ui.UIFunctions.load_assignments(self.parent(), filename)
        self.close()

    # @classmethod
    # def load_check_info(cls, self, filename):
    #     children = self.content_widget.children()
    #     assignments = [Assignment(children[i].test_file_entry.text(), children[i].input_file_entry.text() for i in range(1, self.content_layout.count() + 1)]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow()
    window.show()
    sys.exit(app.exec_())
