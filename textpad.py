from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os
import sys
import uuid

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']

def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()

class TextEdit(QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, QUrl(u), image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return


        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, QUrl(uuid), image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)


class UIFunctions:
    def __init__(self, ui):
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        # Initialize.
        self.update_format(ui)
        self.update_title(ui)

    def block_signals(ui, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(ui):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        ui.block_signals(ui._format_actions, True)

        ui.fonts.setCurrentFont(ui.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        ui.fontsize.setCurrentText(str(int(ui.editor.fontPointSize())))

        ui.italic_action.setChecked(ui.editor.fontItalic())
        ui.underline_action.setChecked(ui.editor.fontUnderline())
        ui.bold_action.setChecked(ui.editor.fontWeight() == QFont.Bold)

        ui.alignl_action.setChecked(ui.editor.alignment() == Qt.AlignLeft)
        ui.alignc_action.setChecked(ui.editor.alignment() == Qt.AlignCenter)
        ui.alignr_action.setChecked(ui.editor.alignment() == Qt.AlignRight)
        ui.alignj_action.setChecked(ui.editor.alignment() == Qt.AlignJustify)

        ui.block_signals(ui._format_actions, False)

    def dialog_critical(ui, s):
        dlg = QMessageBox(ui)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(ui):
        path, _ = QFileDialog.getSaveFileName(ui, "Save file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")


        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            ui.dialog_critical(str(e))

        else:
            ui.path = path
            # Qt will automatically try and guess the format as txt/html
            ui.editor.setText(text)
            ui.update_title()

    def file_save(ui):
        if ui.path is None:
            # If we do not have a path, we need to use Save As.
            return ui.file_save_as()

        text = ui.editor.toHtml() if splitext(ui.path) in HTML_EXTENSIONS else ui.editor.toPlainText()

        try:
            with open(ui.path, 'w') as f:
                f.write(text)

        except Exception as e:
            ui.dialog_critical(str(e))

    def file_save_as(ui):
        path, _ = QFileDialog.getSaveFileName(ui, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = ui.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else ui.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            ui.dialog_critical(str(e))

        else:
            ui.path = path
            ui.update_title()

    def file_print(ui):
        dlg = QPrintDialog()
        if dlg.exec_():
            ui.editor.print_(dlg.printer())

    def update_title(ui):
        ui.setWindowTitle("%s - Megasolid Idiom" % (os.path.basename(ui.path) if ui.path else "Untitled"))

    def edit_toggle_wrap(ui):
        ui.editor.setLineWrapMode( 1 if ui.editor.lineWrapMode() == 0 else 0 )
