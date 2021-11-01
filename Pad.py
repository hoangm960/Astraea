import codecs
import io
import os

from PIL import ImageGrab
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QColorDialog, QFileDialog, QMainWindow,
                             QMessageBox, QShortcut)

from connect_db import get_connection
from path import OPENED_ASSIGNMENT_PATH, OPENED_DOC, OPENED_DOC_CONTENT

PAD_UI = "./UI_Files/Pad.ui"
HTML_EXTENSIONS = [".htm", ".html"]


class PadWindow(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(QMainWindow, self).__init__()
        uic.loadUi(PAD_UI, self)
        self.init_UI()
        UIFunction(self)

    def init_UI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()
        self.title_bar.mouseMoveEvent = self.moveWindow

    def moveWindow(self, event):
        if UIFunction.GLOBAL_STATE == True:
            UIFunction.maximize_restore(self)
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunction(PadWindow):
    GLOBAL_STATE = False
    path = None
    Format = [False, False, False]

    def __init__(self, ui):
        self.connect(ui)
        self.check_empty(ui)

    def connect(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.Quit(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.ColorText.clicked.connect(lambda: self.textColor(ui))
        ui.Color.clicked.connect(lambda: self.textBackgroundColor(ui))

        ui.Center_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignCenter))
        ui.Left_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignLeft))
        ui.Right_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignRight))
        ui.J_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignJustify))

        ui.Font.currentFontChanged.connect(
            lambda: ui.editor.setCurrentFont(ui.Font.currentFont())
        )
        ui.Size.valueChanged.connect(
            lambda: ui.editor.setFontPointSize(ui.Size.value())
        )
        ui.Bold.clicked.connect(lambda: self.setBold(ui))
        ui.Italic.clicked.connect(lambda: self.setItalic(ui))
        ui.Underline.clicked.connect(lambda: self.setUnderline(ui))

        ui.Save.clicked.connect(lambda: self.Save(ui))
        ui.Open.clicked.connect(lambda: self.Function_Open(ui))
        ui.editor.setCurrentFont(ui.Font.currentFont())
        ui.shortcut = QShortcut(QKeySequence("Ctrl+Shift+V"), ui)
        ui.shortcut.activated.connect(lambda: self.check_changed(ui))

    def check_changed(self, ui):
        document = ui.editor.document()
        img = ImageGrab.grabclipboard()
        if img:
            img_bytes = io.BytesIO()

            img.save(img_bytes, format="PNG")

            base64_data = codecs.encode(img_bytes.getvalue(), "base64")

            base64_text = codecs.decode(base64_data, "ascii")

            html_img_tag = '<img src="data:image/png;base64, %s" />' % base64_text
            document.setHtml(html_img_tag)

    @staticmethod
    def check_empty(ui):
        content = open(OPENED_DOC_CONTENT, encoding="utf8").read()
        if content:
            ui.editor.setText(content)

    def Save(self, ui):
        content = ui.editor.toHtml()
        open(OPENED_DOC_CONTENT, "w", encoding="utf8").write(content)
        lesson_id = open(OPENED_ASSIGNMENT_PATH, encoding="utf8").readlines()[1]
        id = open(OPENED_DOC, encoding="utf8").readlines()[1]
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE doc SET DocContent = %s WHERE DocId = %s AND LessonId = %s",
            (content, id, lesson_id),
        )
        connection.commit()
        connection.close()

    def Quit(self, ui):
        with open(OPENED_DOC_CONTENT, encoding="utf8") as f:
            text = f.read()
        if text != ui.editor.toHtml():
            msg = QMessageBox(ui)
            msg.setWindowTitle("Chú ý")
            msg.setText("Chưa lưu file. Đồng ý lưu file?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(
                QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel
            )
            clicked = msg.exec_()
            if clicked == QMessageBox.Save:
                self.Save(ui)
                msg.close()
                ui.close()
                self.reopen_doc(ui)
            elif clicked == QMessageBox.No:
                ui.close()
                self.reopen_doc(ui)
                msg.close()
            else:
                msg.close()
        else:
            ui.close()
            self.reopen_doc(ui)

    def reopen_doc(self, ui):
        ui.switch_window.emit()

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE
        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True
            ui.centralwidget.setStyleSheet(
                """background-color: rgb(74, 74, 74);
    border-radius: 0px;"""
            )
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.centralwidget.setStyleSheet(
                """background-color: rgb(74, 74, 74);
    border-radius: 20px;"""
            )
            ui.btn_maximize.setToolTip("Phóng to")

    def textColor(self, ui):
        col = QColorDialog.getColor(ui.editor.textColor(), ui)
        if not col.isValid():
            return
        ui.editor.setTextColor(col)
        ui.ColorText.setStyleSheet(
            """image: url(:/images/icons/edit-color.png);background: {};""".format(
                col.name()
            )
        )

    def textBackgroundColor(self, ui):
        col = QColorDialog.getColor(ui.editor.textBackgroundColor(), ui)
        if not col.isValid():
            return
        ui.editor.setTextBackgroundColor(col)
        ui.Color.setStyleSheet(
            """background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.227273 rgba(255, 255, 255, 255), stop:0.232955 {}, stop:0.727273 {}, stop:0.732955 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255))""".format(
                col.name(), col.name()
            )
        )

    def setBold(self, ui):
        if self.Format[0]:
            self.Format[0] = False
            ui.editor.setFontWeight(700)
            ui.Bold.setStyleSheet(
                """QPushButton {
                                    image: url(:/images/icons/edit-bold.png);
                                    }"""
            )
        else:
            self.Format[0] = True
            ui.editor.setFontWeight(500)
            ui.Bold.setStyleSheet(
                """QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-bold.png);
                                    }"""
            )

    def setItalic(self, ui):
        if self.Format[1]:
            self.Format[1] = False
            ui.editor.setFontItalic(False)
            ui.Italic.setStyleSheet(
                """QPushButton {
                                    image: url(:/images/icons/edit-italic.png);
                                    }"""
            )
        else:
            self.Format[1] = True
            ui.editor.setFontItalic(True)
            ui.Italic.setStyleSheet(
                """QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-italic.png);
                                    }"""
            )

    def setUnderline(self, ui):
        if self.Format[2]:
            self.Format[2] = False
            ui.editor.setFontUnderline(False)
            ui.Underline.setStyleSheet(
                """QPushButton {
                                    image: url(:/images/icons/edit-underline.png);
                                    }"""
            )
        else:
            self.Format[2] = True
            ui.editor.setFontUnderline(True)
            ui.Underline.setStyleSheet(
                """QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-underline.png);
                                    }"""
            )

    def Function_Open(self, ui):
        path = QFileDialog.getOpenFileName(
            ui,
            "Mở file",
            "",
            "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)",
        )
        try:
            self.path = str(path[0])
            with open(self.path, "r", encoding="utf8") as f:
                text = f.read()
            ui.Title.setText(
                "%s - ASTRAEA Document"
                % (os.path.basename(self.path) if self.path else "Untitled")
            )
            ui.editor.setText(text)
        except:
            pass
