# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Programming\Python\Pylearn\UI_Files\edit_widget2.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditFrame2(object):
    def setupUi(self, EditFrame2):
        EditFrame2.setObjectName("EditFrame2")
        EditFrame2.resize(705, 423)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditFrame2)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(0, 9, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lesson_title = QtWidgets.QLabel(EditFrame2)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lesson_title.setFont(font)
        self.lesson_title.setObjectName("lesson_title")
        self.verticalLayout.addWidget(self.lesson_title)
        self.list_widget = QtWidgets.QListWidget(EditFrame2)
        self.list_widget.setStyleSheet("background-color: transparent;")
        self.list_widget.setObjectName("list_widget")
        self.verticalLayout.addWidget(self.list_widget)

        self.retranslateUi(EditFrame2)
        QtCore.QMetaObject.connectSlotsByName(EditFrame2)

    def retranslateUi(self, EditFrame2):
        _translate = QtCore.QCoreApplication.translate
        EditFrame2.setWindowTitle(_translate("EditFrame2", "Form"))
        self.lesson_title.setText(_translate("EditFrame2", "TextLabel"))