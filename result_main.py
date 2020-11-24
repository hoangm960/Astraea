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
import check_algorithm

RESULT_FORM_PATH = "UI_Files/result_form.ui"
RESULT_FRAME_PATH = "UI_Files/result_frame.ui"
TEST_FRAME_PATH = "UI_Files/Test_frame.ui"


class ResultWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(RESULT_FORM_PATH, self)
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


class UIFunctions(ResultWindow):
    GLOBAL_STATE = False

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
        self.stacked_widget.setCurrentIndex(1)
        self.Out_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.Out_btn.clicked.connect(lambda: cls.put_frame_in_list(self, 20))
        self.return_btn.clicked.connect(lambda: self.close())
        # Button function
        self.btn_maximize.clicked.connect(lambda: cls.maximize_restore(self))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.close())

        # Window size grip
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")
        cls.put_frame_in_test(self, 20)

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
                """
                background-color: rgb(30, 30, 30);\n border-radius: 0px;"""
            )
            self.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.bg_layout.setContentsMargins(10, 10, 10, 10)
            self.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30); \nborder-radius: 10px;"""
            )
            self.btn_maximize.setToolTip("Maximize")

    class ResultFrame(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(RESULT_FRAME_PATH, self)

    class TestFrame(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(TEST_FRAME_PATH, self)

            self.ans_file_btn.clicked.connect(
                lambda: self.showDialog(self.ans_file_entry)
            )

        def showDialog(self, entry):
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(self, "Open file", HOME_PATH)

            if file_name[0]:
                entry.setText(file_name[0])

    @classmethod
    def put_frame_in_test(cls, self, num):
        current_layoutT = self.content_widgetT.layout()
        if not current_layoutT:
            current_layoutT = QVBoxLayout()
            current_layoutT.setContentsMargins(9, 9, 9, 9)
            self.content_widgetT.setLayout(current_layoutT)
        self.ScrollAreaT.verticalScrollBar().setValue(1)

        for i in range(0, num):
            self.frameT = cls.TestFrame()
            self.content_widgetT.layout().addWidget(self.frameT)
            self.frameT.details_label.setText("Câu " + str(i + 1))

    @classmethod
    def put_frame_in_list(cls, self, num):
        current_layout = self.content_widget.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            self.content_widget.setLayout(current_layout)
        self.scrollArea.verticalScrollBar().setValue(1)

        for i in range(0, num):
            self.frame = cls.ResultFrame()
            self.content_widget.layout().addWidget(self.frame)
            self.frame.test_file_label.setText("Câu " + str(i + 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec_())
