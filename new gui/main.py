import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_main import Ui_MainWindo    w
from ui_functions import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
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

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

