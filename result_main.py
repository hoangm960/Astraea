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

RESULT_FORM_PATH = "UI_Files/result_form.ui"
RESULT_FRAME_PATH = "UI_Files/result_frame.ui"

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
        cls.put_frame_in_list(self, 6)
        
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

    class ResultFrame(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(RESULT_FRAME_PATH, self)

    @classmethod
    def put_frame_in_list(cls, self, num):
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)
        self.scrollArea.verticalScrollBar().setValue(1)
        self.percent = 0
        self.SumTest = 0
        Average = 0
        test = [1,2,3,4,5,6,7,8,9,10]        
        correct = [1,2,3,4,5,6,7,8,9,9]
        for i in correct:
            self.percent += i
        for i in test:
            self.SumTest+=i
        for i in range(0,num):
            self.frame = cls.ResultFrame()
            self.content_layout.addWidget(self.frame)
            self.frame.test_file_label.setText('Câu '+str(i+1))
            self.frame.Score_box.setText(str(round((correct[i]/test[i])*10,2)))
            self.frame.Test_box.setText(str(correct[i])+'/'+str(test[i]))
            Average += round((correct[i]/test[i])*10,2)
        self.progressBar.setValue(round((self.percent/self.SumTest)*100))
        self.Score.setText(str(round(Average / len(test),2)))
        if float(self.Score.text()) <8.5:
            self.Judge.setText('Mua điểm không em')
        if float(self.Score.text()) == 10:
            self.Judge.setText('Amazing Gút chóp iem')
        if float(self.Score.text()) < 10 and float(self.Score.text()) >= 8.5:
            self.Judge.setText('Muốn 10 phẩy không khó, đêm đến nhà thầy')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec_())
