import Main
import os
import pickle
import sys
from pathlib import Path

import pyautogui
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QFileDialog,
                             QGraphicsDropShadowEffect, QLayout,
                             QListWidgetItem, QMainWindow, QSizeGrip,
                             QVBoxLayout, QWidget)

import check_algorithm
import main_ui

RESULT_FORM_PATH = "./UI_Files/result_form.ui"
RESULT_FRAME_PATH = "./UI_Files/result_frame.ui"
TEST_FRAME_PATH = "./UI_Files/Test_frame.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
OPENED_RESULT_PATH = "./data/Users/Kết quả.txt"
if not os.path.exists(OPENED_RESULT_PATH):
    open(OPENED_RESULT_PATH, "w").close()

class ResultWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(RESULT_FORM_PATH, self)
        self.setGeometry(
            round((Main.SCREEN_WIDTH - self.width()) / 3),
            round((Main.SCREEN_HEIGHT - self.height()) / 2),
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
    assignments = {}
    lesson = {}
    mark = int()
    Total = int()
    TotalTest = int()
    TotalScore = int()

    @classmethod
    def load_assignments(cls, ui, filename):
        ui.textBrowser.clear()
        cls.lesson.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    title = data[0]
                    assignments = data[1]
                    for assignment in assignments:
                        cls.lesson[assignment.name] = assignment.details
                        ui.textBrowser.addItem(assignment.name)

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
        self.return_btn.clicked.connect(lambda: self.close())
        self.inform.hide()
        self.OkCancelFrameQuit.hide()
        # Button function
        self.OkCancelFrame.hide()
        self.OkCancelFrame.move(0,0)
        self.OkCancelFrame.move(280,148)
        self.btn_maximize.clicked.connect(lambda: cls.maximize_restore(self))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        def quit():
            self.OkCancelFrameQuit.show()
            self.Accept1.clicked.connect(lambda: self.close())
            self.Accept1.clicked.connect(lambda: main_ui.main("student"))
            self.Deny1.clicked.connect(lambda: self.OkCancelFrameQuit.hide())
            self.Deny1.clicked.connect(lambda: self.Out_btn.setDisabled(False))
            self.Deny1.clicked.connect(lambda: self.bg_frame.setStyleSheet("""background-color: rgb(30, 30, 30); border-radius: 10px; color: rgb(255, 255, 255);"""))
            self.Out_btn.setDisabled(True)
            self.bg_frame.setStyleSheet("""background-color: rgba(255, 255, 255, 200); border-radius: 10px; color: rgb(255, 255, 255);""")
        self.btn_quit.clicked.connect(lambda: quit())

        # Window size grip
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")
        cls.load_assignments(open(OPENED_LESSON_PATH).read().rstrip())
        cls.check_empty(self, len(cls.assignments))
    @classmethod
    def move_TaskClose(cls, self):
        self.OkCancelFrame.move(
            round((self.ScrollAreaT.width() - 400) / 2),
            round((self.ScrollAreaT.height() - 180) / 2),
        )
    @classmethod
    def returnStatus(cls):
        return cls.GLOBAL_STATE

    @classmethod
    def maximize_restore(cls, self):
        status = cls.GLOBAL_STATE

        if status == False:
            self.showMaximized()

            cls.GLOBAL_STATE = True
            cls.move_TaskClose(self)
            self.bg_layout.setContentsMargins(0, 0, 0, 0)
            self.bg_frame.setStyleSheet(
                """
                background-color: rgb(30, 30, 30);\n border-radius: 0px;"""
            )
            self.inform.move(
                round((self.ScrollAreaT.width() - 280) / 2),
                round((self.ScrollAreaT.height() - 70) / 2),
            )
            self.btn_maximize.setToolTip("khôi phục")
        else:
            cls.GLOBAL_STATE = False
            self.showNormal()
            cls.move_TaskClose(self)
            self.resize(self.width() + 1, self.height() + 1)
            self.bg_layout.setContentsMargins(0, 0, 0, 0)
            self.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30); \nborder-radius: 10px;"""
            )
            self.inform.move(
                round((self.ScrollAreaT.width() - 280) / 2),
                round((self.ScrollAreaT.height() - 70) / 2),
            )
            self.btn_maximize.setToolTip("Phóng to")

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
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(
                self, "Open file", HOME_PATH, "*.py"
            )

            if file_name[0]:
                entry.setText(file_name[0])

    @classmethod
    def load_assignments(cls, filename):
        cls.assignments.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    cls.assignments = data[1]
    @classmethod
    def reopen_main(cls, ui):
        import main_ui
        main_ui.main("student")
        ui.close()

    @classmethod
    def check_empty(cls, self, num):
        if num != 0:
            self.Out_btn.clicked.connect(lambda: self.close())
            self.Out_btn.clicked.connect(lambda: cls.reopen_main(self))
            self.Out_btn.setText("Thoát")
            self.inform.show()
            self.inform.move(340, 220)
        else:
            self.Out_btn.clicked.connect(lambda: self.OkCancelFrame.show())
            self.Accept.clicked.connect(lambda: self.btn_quit.hide())
            self.Accept.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
            self.Accept.clicked.connect(
            lambda: cls.check_true(self, len(cls.assignments)))
            self.Deny.clicked.connect(lambda: self.OkCancelFrame.hide())
            cls.put_frame_in_list(self, len(cls.assignments))

    @classmethod
    def put_frame_in_list(cls, self, num):
        current_layout = self.content_widgetT.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            self.content_widgetT.setLayout(current_layout)
        self.scrollArea.verticalScrollBar().setValue(1)
        self.results = cls.ResultFrame()

        for i in range(num):
            self.frame = cls.TestFrame()
            self.content_widgetT.layout().addWidget(self.frame)
            self.frame.details_label.setText(cls.assignments[i].name)
            self.frame.details_entry.setText(cls.assignments[i].details)

    # @classmethod
    # def count_total_mark(cls):
    #     for assignment in assignments: 
    #         cls.assignment.mark

    @classmethod
    def check_result(cls, frame, num):
        assignments = cls.assignments[num]
        return check_algorithm.main(
            filename=frame.ans_file_entry.text(),
            ex_file=assignments.ex_file,
            tests=assignments.tests,
        )

    @classmethod
    def check_true(cls, self, num):
        children = self.content_widgetT.children()
        del children[0:2]
        for i in range(num):
            correct = 0
            results = []
            self.frame = children[i]

            if self.frame.ans_file_entry.text() != "":
                results = cls.check_result(self.frame, i)
                for result in results[:-1]:
                    if result[1]:
                        correct += 1

            current_layout = self.content_widget.layout()
            if not current_layout:
                current_layout = QVBoxLayout()
                current_layout.setContentsMargins(9, 9, 9, 9)
                self.content_widget.setLayout(current_layout)
    
            self.frame = cls.ResultFrame()
            self.content_widget.layout().addWidget(self.frame)
            self.frame.correct_num.setText(
                str(correct)+'/'+str(len(cls.assignments[i].tests)))
            self.frame.test_file_label.setText(cls.assignments[i].name)
        
            cls.TotalTest += len(cls.assignments[i].tests)
            
            if results[-1]:
                self.frame.Score_box.setText(
                    str(correct / len(results[:-1]) * cls.assignments[i].mark)
                )
                if results[-1]:
                    self.frame.detail_entry.setText("Bài làm đã tối ưu hóa.")
                else:
                    self.frame.detail_entry.setText("Bài làm chưa tối ưu hóa.")
                cls.Total += correct
                cls.TotalScore += (correct / len(cls.assignments[i].tests) * cls.assignments[i].mark)
            else:
                self.frame.detail_entry.setText("Chưa làm câu này")

        totalScore = int()
        for assignment in cls.assignments:
            totalScore += assignment.mark
        if cls.TotalScore != 0:
            self.progressBar.setValue(int((cls.TotalScore / totalScore)*100))
            self.Score.setText(str(round(cls.TotalScore, 2)))
        else:
            self.progressBar.setValue(0)
        if float(self.Score.text()) < 0.7:
            self.Judge.setText("Bài làm vẫn chưa đạt chuẩn.")
        else:
            self.Judge.setText("Bài làm đạt chuẩn")
        with open(OPENED_RESULT_PATH, 'r+', encoding = 'utf-8') as f:
            if f.read() == '':
                text = 'Em nào đó: '+ self.Score.text()
                f.write(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec_())
