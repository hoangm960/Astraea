import os
import pickle
from datetime import datetime

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QSizeGrip, QVBoxLayout, QWidget

import check_algorithm
from connect_db import DBConnection
from encryption import decrypt, encrypt
from Main import screen_resolution

RESULT_FORM_PATH = "./UI_Files/result_form.ui"
RESULT_FRAME_PATH = "./UI_Files/result_frame.ui"
TEST_FRAME_PATH = "./UI_Files/Test_frame.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
OPENED_RESULT_PATH = "./data/results/"
SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()


class ResultWindow(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(RESULT_FORM_PATH, self)
        self.init_UI()
        UIFunctions(self)

    def init_UI(self):
        self.setGeometry(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
            self.width(),
            self.height(),
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.stacked_widget.setCurrentIndex(1)
        self.inform.hide()
        self.Frame_close.hide()
        self.ERROR_WINDOW.hide()
        self.OkCancelFrame.move(0, 0)
        self.OkCancelFrame.move(280, 148)
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")
        self.title_bar.mouseMoveEvent = self.moveWindow

    def moveWindow(self, event):
        if UIFunctions.GLOBAL_STATE == True:
            UIFunctions.maximize_restore(self)
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(ResultWindow):
    GLOBAL_STATE = False
    assignments = {}
    TotalScore = int()
    USER_PATH = "./data/Users/User.txt"
    USER_PATH_ENCRYPTED = "./data/Users/User.encrypted"
    KEY_PATH = "./data/encryption/users.key"
    FILE_COMMENT = "./data/results/comment.txt"

    def __init__(self, ui):
        self.load_assignments(
            open(OPENED_LESSON_PATH, encoding="utf-8").readline().rstrip()
        )
        self.check_empty(ui, len(self.assignments))

    def connect_btn(self, ui):
        ui.return_btn.clicked.connect(lambda: self.return_main(ui))
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.Accept1.clicked.connect(lambda: ui.close())
        ui.Accept1.clicked.connect(lambda: self.return_main(ui))

    @classmethod
    def returnStatus(self):
        return self.GLOBAL_STATE

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True
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
                lambda: ui.showDialog(
                    ui.ans_file_entry, "Python (*.py);;Free Pascal (*.pas)"
                )
            )

        def showDialog(ui, entry, filter):
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, filter)

            if file_name[0]:
                entry.setText(file_name[0])

    def load_assignments(self, filename):
        self.assignments.clear()
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
                self.assignments = data[1]

    def check_empty(self, ui, num):
        if num == 0:
            ui.Out_btn.clicked.connect(lambda: ui.close())
            ui.Out_btn.clicked.connect(lambda: self.return_main(ui))
            ui.Out_btn.setText("Thoát")
            ui.inform.show()
            ui.inform.move(340, 220)
        else:
            ui.Out_btn.clicked.connect(lambda: ui.OkCancelFrame.show())
            ui.Accept.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
            ui.Accept.clicked.connect(lambda: self.check_true(ui))
            self.put_frame_in_list(ui, len(self.assignments))

    def put_frame_in_list(self, ui, num):
        current_layout = ui.content_widgetT.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widgetT.setLayout(current_layout)
        ui.scrollArea.verticalScrollBar().setValue(1)

        for i in range(num):
            ui.TestFrame = self.TestFrame()
            ui.content_widgetT.layout().addWidget(ui.TestFrame)
            ui.TestFrame.details_label.setText(self.assignments[i].name)
            ui.TestFrame.details_entry.setText(self.assignments[i].details)

    def check_result(self, frame, num):
        assignment = self.assignments[num]
        return check_algorithm.main(
            filename=frame.ans_file_entry.text(),
            tests=assignment.tests,
            infos=assignment.infos,
        )

    def get_results(self, ui, child, num):
        with open(
            self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
        ) as file_error:
            file_error.write(f"\n{self.assignments[num].name}")
        correct = 0
        results = []
        errors = []
        ui.TestFrame = child
        if os.path.exists(ui.TestFrame.ans_file_entry.text()):
            results, errors = self.check_result(ui.TestFrame, num)
            for result in results:
                if result[1]:
                    correct += 1
            return correct, results, errors

        elif ui.TestFrame.ans_file_entry.text():
            with open(
                self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
            ) as file_error:
                file_error.write(
                    "\n>>> FileExistsERROR: Lỗi không tìm thấy file bài làm."
                )
        else:
            return 0, [], []

    def check_true(self, ui): 
        open(self.FILE_COMMENT, "w", encoding="utf8").close()
        ui.btn_quit.close()
        children = ui.content_widgetT.children()
        del children[0:2]

        current_layout = ui.content_widget.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widget.setLayout(current_layout)

        for i in range(len(self.assignments)):
            correct, results, errors = self.get_results(ui, children[i], i)

            ui.ResultFrame = self.ResultFrame()
            ui.content_widget.layout().addWidget(ui.ResultFrame)
            ui.ResultFrame.test_file_label.setText(self.assignments[i].name)
            ui.ResultFrame.correct_num.setText(
                f'{correct}/{len(self.assignments[i].tests)}'
            )


            if len(results) != 0:
                ui.ResultFrame.Score_box.setText(
                    str(
                        round(
                            correct
                            / len(self.assignments[i].tests)
                            * self.assignments[i].mark,
                            2,
                        )
                    )
                )
                for result in results:
                    try:
                        if result[0]:
                            with open(
                                self.FILE_COMMENT,
                                "a+",
                                encoding="utf-8",
                                errors="ignore",
                            ) as f:
                                f.write(
                                    "\n>>> TimeoutExpired: Thuật toán vượt quá thời gian yêu cầu."
                                )
                    except ZeroDivisionError:
                        with open(
                            self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
                        ) as f:
                            f.write(
                                "\n>>> ZeroDivisionError: Tồn tại phép tính chia cho 0."
                            )

                if errors:
                    for message in errors:
                        with open(
                            self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
                        ) as f:
                            f.write(f"\n>>> {message}")

            elif not ui.TestFrame.ans_file_entry.text():
                with open(
                    self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
                ) as f:
                    f.write("\n>>> Chưa làm bài")

            with open(self.FILE_COMMENT, "r", encoding="utf-8", errors="ignore") as f:
                list_file = f.readlines()
                if ">>>" not in list_file[-1]:
                    with open(
                        self.FILE_COMMENT, "a+", encoding="utf-8", errors="ignore"
                    ) as file_error_w:
                        file_error_w.write("\n>>> Không xảy ra lỗi")

            with open(self.FILE_COMMENT, "r", encoding="utf-8", errors="ignore") as f:
                ui.Error_text.setText(str(f.read()))

        totalScore = int() + sum(assignment.mark for assignment in self.assignments)
        children = ui.content_widget.children()
        del children[0]
        for child in children:
            self.TotalScore += float(child.Score_box.text())
        if self.TotalScore != 0:
            ui.progressBar.setValue(int((self.TotalScore / totalScore) * 100))
            ui.Score.setText(str(round(self.TotalScore, 2)))
        else:
            ui.progressBar.setValue(0)
        with open(self.FILE_COMMENT, "a", encoding="utf-8", errors="ignore") as f:
            if float(self.TotalScore) < 0.7 * totalScore:
                f.write("\nBài làm vẫn chưa đạt chuẩn.")
                ui.Judge.setText("Bài làm vẫn chưa đạt chuẩn.")
            else:
                f.write("\nBài làm vẫn đạt chuẩn.")
                ui.Judge.setText("Bài làm đạt chuẩn")

        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        name_account = open(self.USER_PATH, encoding="utf-8").readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

        connection = DBConnection()
        cursor = connection.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lesson_id = int(open(OPENED_LESSON_PATH, encoding="utf-8").readlines()[1])
        if lesson_id:
            try:
                cursor.execute(
                    "INSERT INTO submission(Username, LessonId, SubmissionDate, Mark, Comment) VALUES(%s, %s, %s, %s, %s)",
                    (
                        name_account,
                        lesson_id,
                        current_time,
                        round(self.TotalScore, 2),
                        open(self.FILE_COMMENT, encoding="utf-8").read(),
                    ),
                )
            except mysql.connector.errors.IntegrityError:
                cursor.execute(
                    "UPDATE submission SET Username = %s, LessonId = %s, SubmissionDate = %s, Mark = %s, Comment = %s",
                    (
                        name_account,
                        lesson_id,
                        current_time,
                        round(self.TotalScore, 2),
                        open(self.FILE_COMMENT, encoding="utf8").read(),
                    ),
                )

            connection.close_connection()

    def return_main(self, ui):
        ui.switch_window.emit()
