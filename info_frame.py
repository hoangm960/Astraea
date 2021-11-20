from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)
INFO_CASE_PATH = "./UI_Files/Info_Case.ui"

class Frame_Info(QMainWindow):
    def __init__(self, ui_main, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(INFO_CASE_PATH, self)
        UIFunction(ui=self, parent=ui_main, info=info)


class UIFunction(Frame_Info):
    def __init__(self, ui, parent, info):
        if info:
            self.keyword = info.keyword
            self.message = info.message
            self.min_num = info.min_num
        else:
            self.keyword = self.message = self.min_num = ''
        self.connect(ui, parent)
        self.setup(ui)

    def connect(self, ui, parent):
        ui.close_btn.clicked.connect(lambda: self.closeFrame(ui, parent))

    def closeFrame(self, ui, parent):
        if self.warn_close_frame(parent):
            ui.setParent(None)
            ui.close()

    def warn_close_frame(self, ui):
        msg = QMessageBox.question(
            ui,
            "Xóa chú thích",
            "Bạn chắc chắn muốn xóa chú thích?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        return msg == QMessageBox.Yes

    def setup(self, ui):
        ui_dict = {ui.keyword: self.keyword, ui.message: self.message, ui.count: self.min_num}
        for x, y in ui_dict.items():
            if y:
                if x == ui.count:
                    x.setValue(y)
                else:
                    x.setText(y)