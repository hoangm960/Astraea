import os
import pickle
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                             QMessageBox, QSizeGrip, QVBoxLayout, QWidget)

from UI_Files import Resources

KEY_PATH = "./data/Lesson/assignments.key"
EDIT_FORM_PATH = "./UI_Files/edit_form.ui"
EDIT_FRAME_PATH = "./UI_Files/edit_frame.ui"
OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
HTML_CONVERT_PATH = "./data/html_convert"


class Assignment:
    def __init__(self, name, details, mark, tests, infos):
        self.name = name
        self.details = details
        self.mark = mark
        self.tests = tests
        self.infos = infos


class EditWindow(QMainWindow):
    def __init__(self, pg, connection):
        self.pg = pg
        self.connection = connection
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(EDIT_FORM_PATH, self)
        self.setGeometry(
            round((QApplication.primaryScreen().size().width() - self.width()) / 2),
            round((QApplication.primaryScreen().size().height() - self.height()) / 2),
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


class UIFunctions(EditWindow):
    GLOBAL_STATE = False
    ASSIGNMENTS = []
    doc_files = []

    def __init__(self, ui):
        # Delete title bar
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Button function
        self.connect_btn(ui)

        # Window size grip
        ui.sizegrip = QSizeGrip(ui.frame_grip)
        ui.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(90, 90, 90)}"
        )
        ui.sizegrip.setToolTip("Resize Window")

        ui.stacked_widget.setCurrentIndex(0)
        if os.path.exists(OPENED_ASSIGNMENT_PATH):
            self.check_empty(ui, open(OPENED_ASSIGNMENT_PATH,
                                  encoding='utf-8').readline().rstrip())
    def connect_btn(self, ui):
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.reopen_main(ui))
        ui.confirm_btn.clicked.connect(
            lambda: self.check_empty_entry(ui))
        def check():
            if "'" in ui.name_entry.text():
                ui.name_entry.setStyleSheet("""border-radius: 10px;
                                                color: rgb(255, 0, 0);
                                                border: 2px solid rgb(255,0,0);
                                                background-color: rgb(255, 255, 255);""")
                ui.name_entry.setText("Vui lòng không chứa kí tự '. Có thể thay bằng \"")
                ui.name_entry.setDisabled(True)
                ui.timer = QtCore.QTimer()
                def setDefault():
                    ui.name_entry.clear()
                    ui.name_entry.setStyleSheet("""border-radius: 10px;
                                                color: rgb(0, 0, 0);
                                                background-color: rgb(255, 255, 255);""")
                    ui.name_entry.setDisabled(False)
                ui.timer.singleShot(2500, lambda: setDefault())
            else:
                self.go_to_second(ui)

        ui.confirm_button.clicked.connect(lambda: check())
        ui.return_btn.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.return_btn.clicked.connect(
            lambda: open(OPENED_ASSIGNMENT_PATH, 'w', encoding='utf8').write(''))
        ui.add_btn.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.add_btn.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.return_add_btn.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.confirm_add_btn.clicked.connect(
            lambda: self.add_frame(ui, int(ui.num_entry_3.text()))
        )
        ui.confirm_add_btn.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(1))

    def check_empty_entry(self, ui):
        self.CheckValue = True
        children = ui.content_widget.children()
        del children[0]
        for child in children:
            if not child.title_entry.text() or "'" in child.title_entry.text():
                child.title_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;""")
                self.CheckValue = False
            else:
                child.title_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;""")

            if not os.path.exists(child.test_file_entry.text()) or child.test_file_entry.text()[-4:] != '.txt' or "'" in child.test_file_entry.text():
                child.test_file_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;""")
                self.CheckValue = False
            else:
                child.test_file_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;""")

            if not os.path.exists(child.info_file_entry.text()) or child.info_file_entry.text()[-4:] != '.txt' or "'" in child.info_file_entry.text():
                child.info_file_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;""")
                self.CheckValue = False
            else:
                child.info_file_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;""")

            if child.Score_edit.value() < 0:
                child.Score_edit.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(225, 0 , 0); 
                    border-radius: 12px;""")
                self.CheckValue = False
            else:
                child.Score_edit.setStyleSheet(
                    """background-color: rgb(255, 255, 255); 
                    border: 0px solid black; 
                    border-radius: 12px;""")
            if "'" in child.details_entry.toPlainText():
                text = child.details_entry.toPlainText()
                child.details_entry.setText("Dấu nháy ' không hợp lệ, có thể thay bằng dấu nháy \"")
                child.details_entry.setStyleSheet("""background-color: rgb(255, 255, 255); 
                    border: 2px solid rgb(255,0,0); 
                    border-radius: 12px;""")
                child.details_entry.setDisabled(True)
                ui.timer = QtCore.QTimer()
                def setDefault():
                    child.details_entry.setStyleSheet("""background-color: rgb(255, 255, 255);
                                    border-radius: 12px;""")
                    child.details_entry.setText(text)
                    child.details_entry.setDisabled(False)
                ui.timer.singleShot(2500, lambda: setDefault())


        if self.CheckValue:
            self.show_file_dialog(ui, OPENED_ASSIGNMENT_PATH)

    def check_empty(self, ui, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                ui.stacked_widget.setCurrentIndex(1)
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    title = data[0]
                    assignments = data[1]

                    self.put_frame_in_list(ui, len(assignments))
                    self.setup_frame(ui, title, assignments)

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
        file_path = open(filename, encoding='utf-8').readline().rstrip()
        if not file_path:
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getSaveFileName(
                ui, "Open file", HOME_PATH, "*.list"
            )[0]
            with open(filename, "w", encoding='utf8') as f:
                f.write(f"{file_path}\n0")
        if file_path:
            self.load_assignments(ui, file_path)
            self.reopen_main(ui)

    @staticmethod
    def reopen_main(ui):
        import main_ui
        main_ui.main(1, ui.pg, ui.connection)
        ui.close()

    class EditFrame(QWidget):
        deleted = False

        def __init__(self, ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(EDIT_FRAME_PATH, self)
            self.test_file_btn.clicked.connect(
                lambda: self.get_file(self.test_file_entry, "*.txt")
            )
            self.info_file_btn.clicked.connect(
                lambda: self.get_file(self.info_file_entry, "*.txt")
            )
            self.close_btn.clicked.connect(lambda: self.closeFrame(ui))

        def get_file(self, entry, filter):
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(
                self, "Open file", HOME_PATH, filter)

            if file_name[0]:
                entry.setText(file_name[0])

        def closeFrame(self, ui):
            self.warn_close_frame(ui)
            if self.deleted:
                self.setParent(None)
                ui.scrollArea.verticalScrollBar().setValue(1)
                self.deleted = False

        def warn_close_frame(self, ui):
            msg = QMessageBox(ui)
            msg.setWindowTitle("Xóa bài tập")
            msg.setText(f"'{self.title_entry.text()}' sẽ được xóa")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.popup_button)
            msg.exec_()

        def popup_button(self, i):
            self.deleted = True if i.text().lower() == "ok" else False

    @staticmethod
    def change_lesson_title(ui, title):
        ui.lesson_title.setText(title if title else "Bài học không tên")

    def setup_frame(self, ui, title, assignments):
        children = ui.content_widget.children()
        i = 1
        self.change_lesson_title(ui, title)
        for assignment in assignments:
            children[i].title_entry.setText(assignment.name)
            children[i].details_entry.setText(assignment.details)
            children[i].Score_edit.setValue(assignment.mark)
            i += 1

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

    def add_frame(self, ui, num):
        for _ in range(num):
            ui.frame = self.EditFrame(ui)
            ui.content_widget.layout().addWidget(ui.frame)

    @staticmethod
    def load_io(test_file):
        with open(test_file, encoding = 'utf-8') as f:
            lines = f.readlines()
            sep = lines[0].rstrip()
            del lines[0]
            tests = []
            for line in lines:
                inputs, outputs = line.strip("\n\r").split(sep)
                inputs, outputs = inputs.split('&'), outputs.split('&')
                tests.append([inputs, outputs])
            return tests

    @staticmethod
    def load_info(info_file):
        with open(info_file, encoding = 'utf-8') as f:
            lines = f.readlines()
            sep = lines[0].rstrip()
            del lines[0]
            infos = []
            for line in lines:
                key, message, nums = line.strip("\n\r").split(sep)
                infos.append([key, message, nums])
            return infos

    def load_assignments(self, ui, filename):
        children = ui.content_widget.children()
        del children[0]
        assignments = []
        for i in range(ui.content_widget.layout().count()):
            if not children[i].title_entry.text() in [
                assignment.name for assignment in assignments
            ]:
                tests = self.load_io(children[i].test_file_entry.text())
                infos = self.load_info(children[i].info_file_entry.text())
                assignments.append(
                    Assignment(
                        children[i].title_entry.text(),
                        children[i].details_entry.toPlainText(),
                        children[i].Score_edit.value(),
                        tests,
                        infos
                    )
                )

        with open(filename, "wb") as f:
            pickle.dump([ui.lesson_title.text(), assignments], f, -1)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow(None, None)
    window.show()
    sys.exit(app.exec_())
