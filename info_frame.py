import os
import pickle

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QMessageBox

INFO_CASE_PATH = "./UI_Files/Info_Case.ui"

class Frame_Info(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(INFO_CASE_PATH, self)