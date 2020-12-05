import shutil
import win32com.client
import win32com.client.dynamic


class WordSaveFormat:
    wdFormatNone = None
    wdFormatHTML = 8


class WordOle:
    def __init__(self, filename):
        self.wordApp = win32com.client.dynamic.Dispatch('Word.Application')
        self.filename = filename
        self.wordDoc = self.wordApp.Documents.Open(filename)

    def save(self, newFilename = None, wordSaveFormat = WordSaveFormat.wdFormatNone):
        if newFilename:
            self.filename = newFilename
            self.wordDoc.SaveAs(newFilename, wordSaveFormat)
        else:
            self.wordDoc.Save()

    def close(self):
        self.wordDoc.Close( SaveChanges = 0 )
        self.wordApp.Quit()

    def show(self):
        self.wordApp.Visible = 1

    def hide(self):
        self.wordApp.Visible = 0

if __name__ == "__main__":
    wordOle = WordOle( "D:\\Programming\\Python\\Astraea\\test.docx" )
    wordOle.hide()
    wordOle.save( "D:\\Programming\\Python\\Astraea\\test.html", WordSaveFormat.wdFormatHTML )
    wordOle.close()