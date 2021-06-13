import os
import sys
from PIL import ImageGrab
import io
import codecs

import mysql.connector
from PyQt5 import QtCore, uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QApplication, QColorDialog, QFileDialog,
                             QMainWindow, QMessageBox, QShortcut)

PAD_UI = './UI_Files/Pad.ui'
OPENED_DOC = "./data/Users/opened_doc.od"
OPENED_DOC_CONTENT = "./data/Users/opened_doc_content.html"

HTML_EXTENSIONS = ['.htm', '.html']

class MainPad(QMainWindow):
    def __init__(self, pg):
        super(QMainWindow, self).__init__()
        uic.loadUi(PAD_UI, self)    
        self.pg = pg
        def moveWindow(event):
            if UIFunction.GLOBAL_STATE == True:
                UIFunction.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow
        UIFunction(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    
class UIFunction(MainPad):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    GLOBAL_STATE = False
    path = None
    Format = [False, False, False]

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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

        ui.Font.currentFontChanged.connect(lambda: ui.editor.setCurrentFont(ui.Font.currentFont()))
        ui.Size.valueChanged.connect(lambda: ui.editor.setFontPointSize(ui.Size.value()))
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

            img.save(img_bytes, format='PNG')

            base64_data = codecs.encode(img_bytes.getvalue(), 'base64')

            base64_text = codecs.decode(base64_data, 'ascii')

            html_img_tag = '<img src="data:image/png;base64, %s" />' % base64_text
            document.setHtml(html_img_tag)

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="K63yMSwITl",
            password="zRtA9VtyHq",
            database="K63yMSwITl"
        )

        return connection

    @staticmethod
    def check_empty(ui):
        content = open(OPENED_DOC_CONTENT, encoding='utf8').read()
        if content:
            ui.editor.setText(content)

    def Save(self, ui):
        content = ui.editor.toHtml()
        open(OPENED_DOC_CONTENT, 'w', encoding='utf8').write(content)
        lesson_id = open(self.OPENED_LESSON_PATH, encoding='utf8').readlines()[1]
        id = open(OPENED_DOC, encoding='utf8').readlines()[1]
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE doc SET DocContent = %s WHERE DocId = %s AND LessonId = %s", (content, id, lesson_id))
        connection.commit()
        connection.close()

    def Quit(self, ui):
        with open(OPENED_DOC_CONTENT, encoding='utf8') as f:
            text = f.read() 
        if text != ui.editor.toHtml():
            msg = QMessageBox(ui)
            msg.setWindowTitle('Chú ý')
            msg.setText("Chưa lưu file. Đồng ý lưu file?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
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

    @staticmethod
    def reopen_doc(ui):
        import doc
        window = doc.DocWindow(1, ui.pg)
        window.show()   
            
    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE
        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True
            ui.centralwidget.setStyleSheet("""background-color: rgb(74, 74, 74);
    border-radius: 0px;""")
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.centralwidget.setStyleSheet("""background-color: rgb(74, 74, 74);
    border-radius: 20px;""")
            ui.btn_maximize.setToolTip("Phóng to")

    def textColor(self, ui):
        col = QColorDialog.getColor(ui.editor.textColor(), ui)
        if not col.isValid():
            return
        ui.editor.setTextColor(col)
        ui.ColorText.setStyleSheet("""image: url(:/images/icons/edit-color.png);background: {};""".format(col.name()))
    
    def textBackgroundColor(self, ui):
        col = QColorDialog.getColor(ui.editor.textBackgroundColor(), ui)
        if not col.isValid():
            return
        ui.editor.setTextBackgroundColor(col)
        ui.Color.setStyleSheet("""background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.227273 rgba(255, 255, 255, 255), stop:0.232955 {}, stop:0.727273 {}, stop:0.732955 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255))""".format(col.name(),col.name()))


    def setBold(self, ui):
        if self.Format[0]:
            self.Format[0] = False
            ui.editor.setFontWeight(700)
            ui.Bold.setStyleSheet("""QPushButton {
                                    image: url(:/images/icons/edit-bold.png);
                                    }""")
        else:
            self.Format[0] = True
            ui.editor.setFontWeight(500)
            ui.Bold.setStyleSheet("""QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-bold.png);
                                    }""")
    
    def setItalic(self, ui):
        if self.Format[1]:
            self.Format[1] = False
            ui.editor.setFontItalic(False)
            ui.Italic.setStyleSheet("""QPushButton {
                                    image: url(:/images/icons/edit-italic.png);
                                    }""")
        else:
            self.Format[1] = True
            ui.editor.setFontItalic(True)
            ui.Italic.setStyleSheet("""QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-italic.png);
                                    }""")
    
    def setUnderline(self, ui):
        if self.Format[2]:
            self.Format[2] = False
            ui.editor.setFontUnderline(False)
            ui.Underline.setStyleSheet("""QPushButton {
                                    image: url(:/images/icons/edit-underline.png);
                                    }""")
        else:
            self.Format[2] = True
            ui.editor.setFontUnderline(True)
            ui.Underline.setStyleSheet("""QPushButton {
                                    background: rgb(193,193,193);
                                    image: url(:/images/icons/edit-underline.png);
                                    }""")
    
    def Function_Open(self, ui):
        path = QFileDialog.getOpenFileName(ui, "Mở file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")
        try:
            self.path = str(path[0])
            with open(self.path, 'r', encoding = 'utf8') as f:
                text = f.read()
            ui.Title.setText("%s - ASTRAEA Document" % (os.path.basename(self.path) if self.path else "Untitled"))
            ui.editor.setText(text)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPad(None)
    window.show()
    sys.exit(app.exec_())
