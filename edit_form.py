# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Programming\Python\Pylearn\edit_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditWindow(object):
    def setupUi(self, EditWindow):
        EditWindow.setObjectName("EditWindow")
        EditWindow.resize(736, 418)
        self.centralwidget = QtWidgets.QWidget(EditWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(736, 418))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bg_frame = QtWidgets.QFrame(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.bg_frame.setFont(font)
        self.bg_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255));\n"
"border-radius: 10px;")
        self.bg_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bg_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bg_frame.setObjectName("bg_frame")
        self.bg_layout = QtWidgets.QVBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_layout.setSpacing(0)
        self.bg_layout.setObjectName("bg_layout")
        self.title_bar = QtWidgets.QFrame(self.bg_frame)
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.title_bar.setStyleSheet("background-color: none")
        self.title_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.title_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title_bar.setObjectName("title_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title = QtWidgets.QFrame(self.title_bar)
        self.title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title.setObjectName("title")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.title)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title_label = QtWidgets.QLabel(self.title)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_3.addWidget(self.title_label)
        self.horizontalLayout.addWidget(self.title)
        self.btn_frame = QtWidgets.QFrame(self.title_bar)
        self.btn_frame.setMaximumSize(QtCore.QSize(100, 50))
        self.btn_frame.setStyleSheet("background-color: none;")
        self.btn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btn_frame.setObjectName("btn_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.btn_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_maximize = QtWidgets.QPushButton(self.btn_frame)
        self.btn_maximize.setMinimumSize(QtCore.QSize(15, 15))
        self.btn_maximize.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_maximize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(85, 255, 127, 150);\n"
"}")
        self.btn_maximize.setText("")
        self.btn_maximize.setObjectName("btn_maximize")
        self.horizontalLayout_2.addWidget(self.btn_maximize)
        self.btn_minimize = QtWidgets.QPushButton(self.btn_frame)
        self.btn_minimize.setMinimumSize(QtCore.QSize(15, 15))
        self.btn_minimize.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_minimize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    background-color: rgb(255, 170, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 170, 0, 150);\n"
"}")
        self.btn_minimize.setText("")
        self.btn_minimize.setObjectName("btn_minimize")
        self.horizontalLayout_2.addWidget(self.btn_minimize)
        self.btn_quit = QtWidgets.QPushButton(self.btn_frame)
        self.btn_quit.setMinimumSize(QtCore.QSize(15, 15))
        self.btn_quit.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_quit.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    background-color: rgb(255, 0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 0, 0, 150);\n"
"}")
        self.btn_quit.setText("")
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout_2.addWidget(self.btn_quit)
        self.horizontalLayout.addWidget(self.btn_frame)
        self.bg_layout.addWidget(self.title_bar)
        self.content_frame = QtWidgets.QFrame(self.bg_frame)
        self.content_frame.setStyleSheet("background-color: none")
        self.content_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_frame.setObjectName("content_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.content_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.name_frame = QtWidgets.QFrame(self.content_frame)
        self.name_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.name_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.name_frame.setObjectName("name_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.name_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.name_label = QtWidgets.QLabel(self.name_frame)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(22)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.horizontalLayout_3.addWidget(self.name_label)
        self.name_entry = QtWidgets.QLineEdit(self.name_frame)
        self.name_entry.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(22)
        self.name_entry.setFont(font)
        self.name_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.name_entry.setObjectName("name_entry")
        self.horizontalLayout_3.addWidget(self.name_entry)
        self.verticalLayout_4.addWidget(self.name_frame)
        self.num_frame = QtWidgets.QFrame(self.content_frame)
        self.num_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.num_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.num_frame.setObjectName("num_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.num_frame)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.num_label = QtWidgets.QLabel(self.num_frame)
        self.num_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(22)
        self.num_label.setFont(font)
        self.num_label.setObjectName("num_label")
        self.horizontalLayout_4.addWidget(self.num_label)
        self.num_entry = QtWidgets.QSpinBox(self.num_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.num_entry.sizePolicy().hasHeightForWidth())
        self.num_entry.setSizePolicy(sizePolicy)
        self.num_entry.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(22)
        self.num_entry.setFont(font)
        self.num_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.num_entry.setMinimum(1)
        self.num_entry.setMaximum(100000)
        self.num_entry.setObjectName("num_entry")
        self.horizontalLayout_4.addWidget(self.num_entry)
        self.verticalLayout_4.addWidget(self.num_frame)
        self.confirm_frame = QtWidgets.QFrame(self.content_frame)
        self.confirm_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.confirm_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.confirm_frame.setObjectName("confirm_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.confirm_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.confirm_button = QtWidgets.QPushButton(self.confirm_frame)
        self.confirm_button.setMinimumSize(QtCore.QSize(50, 50))
        self.confirm_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.confirm_button.setStyleSheet("QPushButton {\n"
"    background-color: rgb(102, 146, 251);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(102, 146, 251, 200);\n"
"}")
        self.confirm_button.setObjectName("confirm_button")
        self.verticalLayout_5.addWidget(self.confirm_button, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_4.addWidget(self.confirm_frame, 0, QtCore.Qt.AlignHCenter)
        self.bg_layout.addWidget(self.content_frame)
        self.frame_grip = QtWidgets.QFrame(self.bg_frame)
        self.frame_grip.setMinimumSize(QtCore.QSize(30, 0))
        self.frame_grip.setMaximumSize(QtCore.QSize(30, 30))
        self.frame_grip.setStyleSheet("background-color: none;")
        self.frame_grip.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_grip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_grip.setObjectName("frame_grip")
        self.bg_layout.addWidget(self.frame_grip, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.bg_frame)
        EditWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EditWindow)
        QtCore.QMetaObject.connectSlotsByName(EditWindow)

    def retranslateUi(self, EditWindow):
        _translate = QtCore.QCoreApplication.translate
        EditWindow.setWindowTitle(_translate("EditWindow", "MainWindow"))
        self.title_label.setText(_translate("EditWindow", "Pylearn"))
        self.btn_maximize.setToolTip(_translate("EditWindow", "Maximize"))
        self.btn_minimize.setToolTip(_translate("EditWindow", "Minimize"))
        self.btn_quit.setToolTip(_translate("EditWindow", "Close"))
        self.name_label.setText(_translate("EditWindow", "Tên bài tập:"))
        self.num_label.setText(_translate("EditWindow", "Số bài tập:"))
        self.confirm_button.setText(_translate("EditWindow", "OK"))
