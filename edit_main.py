import os
import pickle
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                             QMessageBox, QSizeGrip, QVBoxLayout, QWidget)

from models.assignment import Assignment
from path import OPENED_ASSIGNMENT_PATH, OPENED_INFO_DATA, OPENED_TEST_DATA
from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH

EDIT_FORM_PATH = "./UI_Files/edit_form.ui"
EDIT_FRAME_PATH = "./UI_Files/edit_frame.ui"


class EditWindow(QMainWindow):
    switch_window_main = QtCore.pyqtSignal()
    switch_window_test = QtCore.pyqtSignal(int)

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(EDIT_FORM_PATH, self)
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
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(90, 90, 90)}"
        )
        self.sizegrip.setToolTip("Resize Window")
        self.stacked_widget.setCurrentIndex(0)

        def moveWindow(event):
            if UIFunctions.GLOBAL_STATE == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(EditWindow):
    GLOBAL_STATE = False
    ASSIGNMENTS = []
    doc_files = []

    def __init__(self, ui):
        self.connect_btn(ui)
        if os.path.exists(OPENED_ASSIGNMENT_PATH):
            self.check_empty(
                ui, open(OPENED_ASSIGNMENT_PATH, encoding="utf-8").readline().rstrip()
            )

    def connect_btn(self, ui):
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))
        ui.confirm_btn.clicked.connect(lambda: self.check_empty_entry(ui))

        def check():
            open(OPENED_TEST_DATA, 'w').write('')
            open(OPENED_INFO_DATA, 'w').write('')
            if "'" in ui.name_entry.text():
                ui.name_entry.setStyleSheet(
                    """border-radius: 10px;
                                                color: rgb(255, 0, 0);
                                                border: 2px solid rgb(255,0,0);
                                                background-color: rgb(255, 255, 255);"""
                )
                ui.name_entry.setText(
                    "Vui lòng không chứa kí tự '. Có thể thay bằng \""
                )
                ui.name_entry.setDisabled(True)
                ui.timer = QtCore.QTimer()

                def setDefault():
                    ui.name_entry.clear()
                    ui.name_entry.setStyleSheet(
                        """border-radius: 10px;
                                                color: rgb(0, 0, 0);
                                                background-color: rgb(255, 255, 255);"""
                    )
                    ui.name_entry.setDisabled(False)

                ui.timer.singleShot(2500, lambda: setDefault())
            else:
                self.go_to_second(ui)

        ui.confirm_button.clicked.connect(lambda: check())
        ui.return_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.return_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.confirm_add_btn.clicked.connect(
            lambda: self.initTestInfo(OPENED_TEST_DATA, int(ui.num_entry_3.text()))
        )
        ui.confirm_add_btn.clicked.connect(
            lambda: self.initTestInfo(OPENED_INFO_DATA, int(ui.num_entry_3.text()))
        )
        ui.confirm_add_btn.clicked.connect(
            lambda: self.add_frame(ui, int(ui.num_entry_3.text()))
        )
        ui.confirm_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))

    def return_main(self, ui):
        ui.switch_window_main.emit()

    def check_empty_entry(self, ui):
        self.CheckValue = True
        children = ui.content_widget.children()
        del children[0]
        for child in children:
            if not child.title_entry.text() or "'" in child.title_entry.text():
                child.title_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;"""
                )
                self.CheckValue = False
            else:
                child.title_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;"""
                )

            if child.Score_edit.value() < 0:
                child.Score_edit.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;"""
                )
                self.CheckValue = False
            else:
                child.Score_edit.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;"""
                )
            if "'" in child.details_entry.toPlainText():
                text = child.details_entry.toPlainText()
                child.details_entry.setText(
                    "Dấu nháy ' không hợp lệ, có thể thay bằng dấu nháy \""
                )
                child.details_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(255,0,0); 
                    border-radius: 12px;"""
                )
                child.details_entry.setDisabled(True)
                ui.timer = QtCore.QTimer()

                def setDefault():
                    child.details_entry.setStyleSheet(
                        """background-color: rgb(255, 255, 255);
                                    border-radius: 12px;"""
                    )
                    child.details_entry.setText(text)
                    child.details_entry.setDisabled(False)

                ui.timer.singleShot(2500, lambda: setDefault())
            with open(OPENED_TEST_DATA, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
            check = []
            for i in data:
                for j in i:
                    check.append(list(set(j.inputs)))
                    check.append(list(set(j.outputs)))
            if not len(data[children.index(child)]) or [i for i in check if '' in i or i == None]:
                child.edit_btn.setStyleSheet("""QPushButton {
                                                background-color: rgb(255, 255, 255);
                                                border-radius: 5px;
                                                border: 2px solid rgb(255, 0, 0);
                                            }

                                            QPushButton:hover {
                                                background-color: rgba(255, 255, 255, 150)
                                            }""")
                self.CheckValue = False
            else:
                child.edit_btn.setStyleSheet("""QPushButton {
                                            background-color: rgb(255, 255, 255);
                                            border-radius: 5px;
                                        }

                                        QPushButton:hover {
                                            background-color: rgba(255, 255, 255, 150)
                                        }""")
                self.CheckValue = True
            
        if self.CheckValue:
            self.show_file_dialog(ui, OPENED_ASSIGNMENT_PATH)

    def check_empty(self, ui, filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            ui.stacked_widget.setCurrentIndex(1)
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
                title = data[0]
                assignments = data[1]

                self.put_frame_in_list(ui, len(assignments))
                self.setup_frame(ui, title, assignments)
                self.setupTestInfo(assignments)

    @staticmethod
    def setupTestInfo(assignments):
        with open(OPENED_TEST_DATA, 'wb') as f:
            pickle.dump([assignment.tests for assignment in assignments], f, -1)
        with open(OPENED_INFO_DATA, 'wb') as f:
            pickle.dump([assignment.infos for assignment in assignments], f, -1)

    def go_to_second(self, ui):
        self.change_lesson_title(ui, ui.name_entry.text())
        self.put_frame_in_list(ui, ui.num_entry.value())
        ui.stacked_widget.setCurrentIndex(1)

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
                """background-color: rgb(30, 30, 30);
                border-radius: 0px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30);
                border-radius: 10px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("Phóng to")

    def show_file_dialog(self, ui, filename):
        file_path = open(filename, encoding="utf-8").readline().rstrip()
        if not file_path:
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getSaveFileName(
                ui, "Open file", HOME_PATH, "*.list"
            )[0]
            with open(filename, "w", encoding="utf8") as f:
                f.write(f"{file_path}\n0")
        if file_path:
            self.load_assignments(ui, file_path)
            self.return_main(ui)

    class EditFrame(QWidget):
        def __init__(self, ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(EDIT_FRAME_PATH, self)
            self.edit_btn.clicked.connect(lambda: self.getData(ui))
            self.close_btn.clicked.connect(lambda: self.closeFrame(ui))

        def getData(self, ui):
            ui.switch_window_test.emit(ui.content_widget.layout().indexOf(self))

        def closeFrame(self, ui):
            if self.warn_close_frame(ui):
                self.setParent(None)
                ui.scrollArea.verticalScrollBar().setValue(1)

        def warn_close_frame(self, ui):
            msg = QMessageBox.question(
                ui,
                "Xóa bài tập",
                f'"{self.title_entry.text() if self.title_entry.text() else "Bai tap khong ten"}" sẽ được xóa',
                QMessageBox.Yes | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            return msg == QMessageBox.Yes

    @staticmethod
    def change_lesson_title(ui, title):
        ui.lesson_title.setText(title or "Bài học không tên")

    def setup_frame(self, ui, title, assignments):
        children = ui.content_widget.children()
        self.change_lesson_title(ui, title)
        for i, assignment in enumerate(assignments, start=1):
            children[i].title_entry.setText(assignment.name)
            children[i].details_entry.setText(assignment.details)
            children[i].Score_edit.setValue(assignment.mark)

    def put_frame_in_list(self, ui, num):
        current_layout = ui.content_widget.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widget.setLayout(current_layout)
        for i in reversed(range(current_layout.count())):
            current_layout.itemAt(i).widget().setParent(None)

        ui.scrollArea.verticalScrollBar().setValue(1)

        self.add_frame(ui, num)

    @staticmethod
    def initTestInfo(filename, num):
        with open(filename, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            data = unpickler.load()
        with open(filename, 'wb') as f:
            data.extend([[]]*num)
            pickle.dump(data, f, -1)

    def add_frame(self, ui, num):
        for _ in range(num):
            ui.frame = self.EditFrame(ui)
            ui.content_widget.layout().addWidget(ui.frame)

    @staticmethod
    def get_data(filename):
        if os.path.getsize(filename) > 0:
            with open(filename, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
            with open(filename, 'w') as f:
                f.write('')
            return data

    def load_assignments(self, ui, filename):
        children = ui.content_widget.children()
        del children[0]
        assignments = []
        tests_data, infos_data = self.get_data(OPENED_TEST_DATA), self.get_data(OPENED_INFO_DATA)
        for i in range(ui.content_widget.layout().count()):
            if children[i].title_entry.text() not in [
                assignment.name for assignment in assignments
            ]:
                tests = tests_data[i]
                infos = infos_data[i]
                assignments.append(
                    Assignment(
                        children[i].title_entry.text(),
                        children[i].details_entry.toPlainText(),
                        children[i].Score_edit.value(),
                        tests,
                        infos,
                    )
                )

        with open(filename, "wb") as f:
            pickle.dump([ui.lesson_title.text(), assignments], f, -1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow()
    window.show()
    sys.exit(app.exec_())
