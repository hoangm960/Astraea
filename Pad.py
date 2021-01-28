import os
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCharFormat, QTextCursor 
from PyQt5.QtWidgets import QAction, QFileDialog, QFontDialog, QMainWindow, QApplication, QColorDialog, QMessageBox
from PyQt5.QtCore import Qt
from UI_Files import Resources
import sys 

PAD_UI = './UI_Files/Pad.ui'

HTML_EXTENSIONS = ['.htm', '.html']

class MainPad(QMainWindow):
    def __init__(self, doc):
        super(QMainWindow, self).__init__()
        uic.loadUi(PAD_UI, self)    
        self.doc = doc
        UIFunction(self)

class UIFunction(MainPad):
    GLOBAL_STATE = False
    path = None
    Format = [False, False, False]
    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.connect(ui)
        
    def connect(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.Quit(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.Color.clicked.connect(lambda: self.textColor(ui))
        ui.Center_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignCenter))
        ui.Left_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignLeft))
        ui.Right_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignRight))
        ui.J_Align.clicked.connect(lambda: ui.editor.setAlignment(Qt.AlignJustify))

        ui.Font.currentFontChanged.connect(lambda: ui.editor.setCurrentFont(ui.Font.currentFont()))
        ui.Size.valueChanged.connect(lambda: ui.editor.setFontPointSize(ui.Size.value()))
        ui.Bold.clicked.connect(lambda: self.setBold(ui))
        ui.Italic.clicked.connect(lambda: self.setItalic(ui))
        ui.Underline.clicked.connect(lambda: self.setUnderline(ui))

        ui.Save_As.clicked.connect(lambda: self.Function_Save_As(ui))
        ui.Save.clicked.connect(lambda: self.Function_Save(ui))
        ui.Open.clicked.connect(lambda: self.Function_Open(ui))
        ui.New.clicked.connect(lambda: self.Function_New(ui))
        ui.editor.setCurrentFont(ui.Font.currentFont())

    def Quit(self, ui):
        text = ''
        try:
            with open(self.path,'r', encoding = 'utf8') as f:
                text = f.read() 
        except:
            pass
        if not self.path or text != ui.editor.toHtml():
            msg = QMessageBox(ui)
            msg.setWindowTitle('Chú ý')
            msg.setText("Chưa lưu file. Đồng ý lưu file?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
            clicked = msg.exec_()
            if clicked == QMessageBox.Save:
                msg.close()
                self.Function_Save(ui)
            elif clicked == QMessageBox.No:
                ui.close()
                msg.close()
            else:
                msg.close()
        else:
            ui.close()
                
            
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
        ui.Color.setStyleSheet("""background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.227273 rgba(255, 255, 255, 255), stop:0.232955 {}, stop:0.727273 {}, stop:0.732955 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255))""".format(ui.editor.textColor().name(),ui.editor.textColor().name()))

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

    def Function_Save_As(self, ui):
        path = QFileDialog.getSaveFileName(ui, "Save file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")
        if not path:
            return  
        try:
            self.path = str(path[0])
            ui.Title.setText("%s - ASTRAEA Document" % (os.path.basename(self.path) if self.path else "Untitled"))
            with open(self.path, 'w') as f:
                f.write(ui.editor.toHtml())
        except:
            pass

    def Function_Save(self, ui):
        if not self.path:
            self.Function_Save_As(ui)  
        else:
            ui.Title.setText("%s - ASTRAEA Document" % (os.path.basename(self.path) if self.path else "Untitled"))
            with open(self.path, 'w', encoding = 'utf8') as f:
                f.write(ui.editor.toHtml())
    
    def Function_Open(self, ui):
        path = QFileDialog.getOpenFileName(ui, "Open file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")
        try:
            self.path = str(path[0])
            with open(self.path, 'r', encoding = 'utf8') as f:
                text = f.read()
            ui.Title.setText("%s - ASTRAEA Document" % (os.path.basename(self.path) if self.path else "Untitled"))
            ui.editor.setText(text)
        except:
            pass
        
    def Function_New(self, ui):
        self.path = None
        ui.editor.clear()
        ui.Title.setText('Untitled - ASTRAEA Document')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPad(None)
    window.show()
    sys.exit(app.exec_())
