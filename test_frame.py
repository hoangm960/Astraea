import os
import pickle

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

TEST_CASE_PATH = "./UI_Files/Test_Case.ui"


class Frame_Test(QMainWindow):
    def __init__(self, ui_main, test=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(TEST_CASE_PATH, self)
        UIFunction(ui=self, parent=ui_main, test=test)


class UIFunction(Frame_Test):
    def __init__(self, ui, parent, test):
        if test:
            self.inputs = test.inputs
            self.outputs = test.outputs
        else:
            self.inputs = self.outputs = ""
        self.connect(ui, parent)
        self.setup(ui)

    def connect(self, ui, parent):
        ui.add_input.clicked.connect(lambda: self.add_frame(ui, 1, ""))
        ui.add_output.clicked.connect(lambda: self.add_frame(ui, 0, ""))
        ui.close_btn.clicked.connect(lambda: self.closeFrame(ui, parent))

    def closeFrame(self, ui, parent):
        if self.warn_close_frame(parent):
            ui.setParent(None)
            ui.close()


    def warn_close_frame(self, ui):
        msg = QMessageBox.question(
            ui,
            "Xóa test",
            "Bạn chắc chắn muốn xóa test?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        return msg == QMessageBox.Yes

    def setup(self, ui):
        current_layout = ui.input.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.input.setLayout(current_layout)
        for i in reversed(range(current_layout.count())):
            current_layout.itemAt(i).widget().setParent(None)

        ui.area_in.verticalScrollBar().setValue(1)

        current_layout = ui.output.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.output.setLayout(current_layout)
        for i in reversed(range(current_layout.count())):
            current_layout.itemAt(i).widget().setParent(None)

        ui.area_out.verticalScrollBar().setValue(1)

        if self.inputs and self.outputs:
            for i in self.inputs:
                self.add_frame(ui, 1, i)
            for i in self.outputs:
                self.add_frame(ui, 0, i)

    def add_frame(self, ui, num, text):
        ui.frame = QLineEdit(ui)
        ui.frame.setText(text)
        ui.frame.setStyleSheet(
            """background-color: rgb(255, 255, 255);
                                border-radius: 10px;
                                font: 13px;
                                color: black;"""
        )
        ui.frame.setMinimumSize(400, 30)
        ui.frame.setAlignment(Qt.AlignCenter)
        if num:
            ui.input.layout().addWidget(ui.frame)
        else:
            ui.output.layout().addWidget(ui.frame)
