import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow

DOC_PATH = "./UI_Files/Doc.ui"


class DocWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(DOC_PATH, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
def main():
    app = QApplication(sys.argv)
    window = DocWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


