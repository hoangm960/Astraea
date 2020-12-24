import os
import pickle
import sys
from datetime import datetime

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QFileDialog,
                             QMainWindow, QSizeGrip,
                             QVBoxLayout, QWidget)
from win32api import GetMonitorInfo, MonitorFromPoint

import check_algorithm
import main_ui

RESULT_FORM_PATH = "./UI_Files/result_form.ui"
RESULT_FRAME_PATH = "./UI_Files/result_frame.ui"
TEST_FRAME_PATH = "./UI_Files/Test_frame.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
OPENED_RESULT_PATH = "./data/results/"

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]


class ResultWindow(QMainWindow):
    def __init__(self, pg=None):
        self.pg = pg
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(RESULT_FORM_PATH, self)
        self.setGeometry(
            round((SCREEN_WIDTH - self.width()) / 3),
            round((SCREEN_HEIGHT - self.height()) / 2),
            self.width(),
            self.height(),
        )

        def moveWindow(event):
            if UIFunctions.GLOBAL_STATE == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

        UIFunctions(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(ResultWindow):
    GLOBAL_STATE = False
    assignments = {}
    lesson = {}
    users = []
    count = 0
    mark = int()
    Total = int()
    TotalTest = int()
    TotalScore = int()
    USER_PATH = "./data/Users/User.txt"
    USER_PATH_ENCRYPTED = "./data/Users/User.encrypted"
    KEY_PATH = "./data/encryption/users.key"
    OPENED_USER = "./data/Users/opened_user.ou"
    FILE_ERROR = "./data/ERROR.txt"
    def __init__(self, ui):
        # Delete title bar
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        ui.stacked_widget.setCurrentIndex(1)
        ui.return_btn.clicked.connect(lambda: self.reopen_main(ui))
        ui.inform.hide()
        ui.Frame_close.hide()
        ui.ERROR_WINDOW.hide()
        # Button function
        ui.OkCancelFrame.move(0, 0)
        ui.OkCancelFrame.move(280, 148)
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())

        def quit():
            ui.Accept1.clicked.connect(lambda: ui.close())
            ui.Accept1.clicked.connect(
                lambda: main_ui.main("student", ui.pg))
            ui.Deny1.clicked.connect(lambda: ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30); border-radius: 10px; color: rgb(255, 255, 255);"""))
            ui.bg_frame.setStyleSheet(
                """background-color: rgba(255, 255, 255, 200); border-radius: 10px; color: rgb(255, 255, 255);""")
        ui.btn_quit.clicked.connect(lambda: quit())

        # Window size grip
        ui.sizegrip = QSizeGrip(ui.frame_grip)
        ui.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        ui.sizegrip.setToolTip("Resize Window")
        self.load_assignments(open(OPENED_LESSON_PATH, encoding = 'utf-8').read().rstrip())
        self.check_empty(ui, len(self.assignments))

    def load_assignments(self, ui, filename):
        ui.textBrowser.clear()
        self.lesson.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    assignments = data[1]
                    for assignment in assignments:
                        self.lesson[assignment.name] = assignment.details
                        ui.textBrowser.addItem(assignment.name)
    
    @classmethod
    def returnStatus(self):
        return self.GLOBAL_STATE

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True
            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """
                background-color: rgb(30, 30, 30);\n border-radius: 0px;"""
            )
            ui.inform.move(
                round((ui.ScrollAreaT.width() - 280) / 2),
                round((ui.ScrollAreaT.height() - 70) / 2),
            )
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30); \nborder-radius: 10px;"""
            )
            ui.inform.move(
                round((ui.ScrollAreaT.width() - 280) / 2),
                round((ui.ScrollAreaT.height() - 70) / 2),
            )
            ui.btn_maximize.setToolTip("Phóng to")

    class ResultFrame(QWidget):
        def __init__(ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(RESULT_FRAME_PATH, ui)

    class TestFrame(QWidget):
        def __init__(ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(TEST_FRAME_PATH, ui)

            ui.ans_file_btn.clicked.connect(
                lambda: ui.showDialog(ui.ans_file_entry, "Python (*.py);;Free Pascal (*.pas)")
            )

        def showDialog(ui, entry, filter):
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(
                ui, "Open file", HOME_PATH, filter
            )

            if file_name[0]:
                entry.setText(file_name[0])

    def load_assignments(self, filename):
        self.assignments.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    self.assignments = data[1]

    def check_empty(self, ui, num):
        if num == 0:
            ui.Out_btn.clicked.connect(lambda: ui.close())
            ui.Out_btn.clicked.connect(lambda: self.reopen_main(ui))
            ui.Out_btn.setText("Thoát")
            ui.inform.show()
            ui.inform.move(340, 220)
        else:
            ui.Out_btn.clicked.connect(lambda: ui.OkCancelFrame.show())
            ui.Accept.clicked.connect(
                lambda: ui.stacked_widget.setCurrentIndex(0))
            ui.Accept.clicked.connect(
                lambda: self.check_true(ui, len(self.assignments)))
            self.put_frame_in_list(ui, len(self.assignments))

    def put_frame_in_list(self, ui, num):
        current_layout = ui.content_widgetT.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widgetT.setLayout(current_layout)
        ui.scrollArea.verticalScrollBar().setValue(1)
        ui.results = self.ResultFrame()

        for i in range(num):
            ui.TestFrame = self.TestFrame()
            ui.content_widgetT.layout().addWidget(ui.TestFrame)
            ui.TestFrame.details_label.setText(self.assignments[i].name)
            ui.TestFrame.details_entry.setText(self.assignments[i].details)

    def check_result(self, frame, num):
        assignment = self.assignments[num]
        return check_algorithm.main(
            filename=frame.ans_file_entry.text(),
            inputs= assignment.inputs,
            outputs= assignment.outputs
        )

    def check_true(self, ui, num):
        children = ui.content_widgetT.children()
        del children[0:2]
        with open(self.FILE_ERROR, 'w', encoding = 'utf-8', errors = 'ignore') as file_error:
            file_error.write('\nPython {}'.format(str(sys.version_info[0])+'.'+str(sys.version_info[1])))
        for i in range(num):
            with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                file_error.write('\nBài {}'.format(str(i+1)))
            correct = 0
            results = []
            ui.TestFrame = children[i]
            if os.path.exists(ui.TestFrame.ans_file_entry.text()):
                try:
                    results = self.check_result(ui.TestFrame, i)
                except:
                    with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                        file_error.write('\n>>> FileERROR: File bài làm không đúng yêu cầu của đề')

                for result in results:
                    if result[1]:
                        correct += 1
            elif ui.TestFrame.ans_file_entry.text():
                with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                    file_error.write('\n>>> FileExistsERROR: Lỗi không tìm thấy file bài làm.')

            current_layout = ui.content_widget.layout()
            if not current_layout:
                current_layout = QVBoxLayout()
                current_layout.setContentsMargins(9, 9, 9, 9)
                ui.content_widget.setLayout(current_layout)

            ui.ResultFrame = self.ResultFrame()
            ui.content_widget.layout().addWidget(ui.ResultFrame)
            ui.ResultFrame.correct_num.setText(
                f'{str(correct)}/{str(len(self.assignments[i].outputs))}')
            ui.ResultFrame.test_file_label.setText(self.assignments[i].name)
            self.TotalTest += len(self.assignments[i].outputs)
            if len(results) != 0:
                try:
                    ui.ResultFrame.Score_box.setText(
                        str(round(float(str(correct / len(self.assignments[i].outputs) * self.assignments[i].mark)),2))
                    )
                    if results[-1]:
                        ui.ResultFrame.detail_entry.setText(
                            "Bài làm đã tối ưu hóa.")
                        self.Total += correct
                    else:
                        ui.ResultFrame.detail_entry.setText(
                            "Bài làm chưa tối ưu hóa.")
                        self.Total += correct
                        self.Total -= 0.25
                    self.TotalScore += (correct /len(self.assignments[i].outputs) * self.assignments[i].mark)
                    
                    if correct < (len(results[:-1])/2):
                        ui.ResultFrame.detail_entry.setText(
                            "Bài làm chưa hoàn thiện tốt.")
                    if results[0][0] == True:
                        with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                            file_error.write('\n>>> TimeoutExpired: Thuật toán vượt quá thời gian yêu cầu.')    
                    elif results[0][0] == True:    
                        with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                            file_error.write('\n>>> OutputMISSING: Không xuất được output. Có lẽ chưa print()?')
                except ZeroDivisionError:
                    with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                        file_error.write('\n>>> ZeroDivisonError: Tồn tại phép tính chia cho 0')
                    ui.ResultFrame.detail_entry.setText(
                        "Câu này đã xảy ra sự cố.")
            elif not ui.TestFrame.ans_file_entry.text():
                ui.ResultFrame.detail_entry.setText("Chưa làm câu này")
                with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error:
                    file_error.write('\n>>> Chưa làm bài')
            with open(self.FILE_ERROR, 'r', encoding = 'utf-8', errors = 'ignore') as file_error:    
                list_file = file_error.readlines()
                if '>>>' not in list_file[-1]:
                    with open(self.FILE_ERROR, 'a+', encoding = 'utf-8', errors = 'ignore') as file_error_w:
                        file_error_w.write('\n>>> Không xảy ra lỗi')
            with open(self.FILE_ERROR, 'r', encoding = 'utf-8', errors = 'ignore') as file_error:    
                ui.Error_text.setText(str(file_error.read()))

        totalScore = int()
        for assignment in self.assignments:
            totalScore += assignment.mark
        if self.TotalScore != 0:
            ui.progressBar.setValue(int((self.TotalScore / totalScore)*100))
            ui.Score.setText(str(round(self.TotalScore, 2)))
        else:
            ui.progressBar.setValue(0)
        if float(ui.Score.text()) < 0.7:
            ui.Judge.setText("Bài làm vẫn chưa đạt chuẩn.")
        else:
            ui.Judge.setText("Bài làm đạt chuẩn")

        with open(f"{OPENED_RESULT_PATH}{open(self.OPENED_USER, encoding = 'utf-8').readline().rstrip()}.rf", 'a+', encoding='utf-8') as f:
            name_account = open(
                self.OPENED_USER, encoding='utf-8').readline().rstrip()
            current_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            text = f'{name_account} :  {ui.Score.text()} ({current_time})\n'
            f.write(text)
    @staticmethod
    def reopen_main(ui):
        main_ui.main("student", ui.pg)
        ui.close()


def main(pg):
    app = QApplication(sys.argv)
    window = ResultWindow(pg)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(None)
