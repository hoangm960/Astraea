from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QMainWindow,
    QSizeGrip,
    QWidget,
)
from PyQt5 import uic

EDIT_FORM_PATH = "UI_Files/edit_form.ui"
EDIT_WIDGET1_PATH = "UI_Files/edit_widget1.ui"
EDIT_WIDGET2_PATH = "UI_Files/edit_widget2.ui"


class EditFrame1(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(EDIT_WIDGET1_PATH, self)


class EditFrame2(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(EDIT_WIDGET2_PATH, self)

    def change_lesson_title(self, title):
        self.lesson_title.setText(title if title else "Bài học không tên")


class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(EDIT_FORM_PATH, self)

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

        self.btn_maximize.clicked.connect(lambda: UIFunctions.maximize_restore(self))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_quit.clicked.connect(lambda: self.close())

        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")

        self.first = EditFrame1()
        self.stackedWidget.insertWidget(0, self.first)
        self.first.confirm_button.clicked.connect(lambda: cls.go_to_second(self))
        self.second = EditFrame2()
        self.stackedWidget.insertWidget(1, self.second)
        self.stackedWidget.setCurrentIndex(0)

    @classmethod
    def go_to_second(cls, self):
        self.second.change_lesson_title(self.first.name_entry.text())
        self.stackedWidget.setCurrentIndex(1)

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
