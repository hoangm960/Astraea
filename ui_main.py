# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Programming\Python\Pylearn\ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 728)
        MainWindow.setMinimumSize(QtCore.QSize(300, 728))
        MainWindow.setMaximumSize(QtCore.QSize(300, 728))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bg_frame = QtWidgets.QFrame(self.centralwidget)
        self.bg_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.497, y1:0, x2:0.496, y2:1, stop:0 rgba(0, 176, 255, 255), stop:0.539773 rgba(0, 71, 121, 255), stop:1 rgba(0, 31, 104, 255));")
        self.bg_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bg_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bg_frame.setObjectName("bg_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.bg_frame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.title_bar = QtWidgets.QFrame(self.bg_frame)
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.title_bar.setFont(font)
        self.title_bar.setStyleSheet("background-color: none")
        self.title_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.title_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title_bar.setObjectName("title_bar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.title_bar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_title = QtWidgets.QFrame(self.title_bar)
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_title)
        self.verticalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtWidgets.QLabel(self.frame_title)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.title.setFont(font)
        self.title.setScaledContents(False)
        self.title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.horizontalLayout_2.addWidget(self.frame_title)
        self.frame_btn = QtWidgets.QFrame(self.title_bar)
        self.frame_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_btn.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btn.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btn.setObjectName("frame_btn")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_btn)
        self.horizontalLayout_5.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_minimize = QtWidgets.QPushButton(self.frame_btn)
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
        self.horizontalLayout_5.addWidget(self.btn_minimize)
        self.btn_quit = QtWidgets.QPushButton(self.frame_btn)
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
        self.horizontalLayout_5.addWidget(self.btn_quit)
        self.horizontalLayout_2.addWidget(self.frame_btn)
        self.verticalLayout_6.addWidget(self.title_bar)
        self.frame_content = QtWidgets.QFrame(self.bg_frame)
        self.frame_content.setStyleSheet("background-color: none")
        self.frame_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName("frame_content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_content)
        self.verticalLayout_3.setContentsMargins(15, 15, 15, 5)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_content_assignment = QtWidgets.QFrame(self.frame_content)
        self.frame_content_assignment.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content_assignment.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_assignment.setObjectName("frame_content_assignment")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_content_assignment)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.list_assignments = QtWidgets.QListWidget(self.frame_content_assignment)
        font = QtGui.QFont()
        font.setFamily("iCiel Effra")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.list_assignments.setFont(font)
        self.list_assignments.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_assignments.setAutoScroll(False)
        self.list_assignments.setAutoScrollMargin(5)
        self.list_assignments.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_assignments.setTabKeyNavigation(True)
        self.list_assignments.setProperty("showDropIndicator", False)
        self.list_assignments.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.list_assignments.setIconSize(QtCore.QSize(3, 3))
        self.list_assignments.setMovement(QtWidgets.QListView.Free)
        self.list_assignments.setProperty("isWrapping", False)
        self.list_assignments.setViewMode(QtWidgets.QListView.ListMode)
        self.list_assignments.setUniformItemSizes(False)
        self.list_assignments.setWordWrap(True)
        self.list_assignments.setSelectionRectVisible(True)
        self.list_assignments.setItemAlignment(QtCore.Qt.AlignLeading)
        self.list_assignments.setObjectName("list_assignments")
        self.verticalLayout_5.addWidget(self.list_assignments)
        self.verticalLayout_3.addWidget(self.frame_content_assignment)
        self.frame_content_hint = QtWidgets.QFrame(self.frame_content)
        self.frame_content_hint.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content_hint.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_hint.setObjectName("frame_content_hint")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_content_hint)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.assignment_details = QtWidgets.QTextEdit(self.frame_content_hint)
        font = QtGui.QFont()
        font.setFamily("iCiel Effra")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.assignment_details.setFont(font)
        self.assignment_details.setTabChangesFocus(True)
        self.assignment_details.setUndoRedoEnabled(False)
        self.assignment_details.setReadOnly(True)
        self.assignment_details.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.assignment_details.setObjectName("assignment_details")
        self.verticalLayout_4.addWidget(self.assignment_details)
        self.verticalLayout_3.addWidget(self.frame_content_hint)
        self.verticalLayout_6.addWidget(self.frame_content)
        self.frame_main_btn = QtWidgets.QFrame(self.bg_frame)
        self.frame_main_btn.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_main_btn.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_main_btn.setFont(font)
        self.frame_main_btn.setStyleSheet("background-color: none;\n"
"")
        self.frame_main_btn.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main_btn.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main_btn.setObjectName("frame_main_btn")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_main_btn)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.main_btn = QtWidgets.QPushButton(self.frame_main_btn)
        self.main_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.main_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        self.main_btn.setFont(font)
        self.main_btn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 255, 255, 150)\n"
"}")
        self.main_btn.setCheckable(False)
        self.main_btn.setChecked(False)
        self.main_btn.setFlat(False)
        self.main_btn.setObjectName("main_btn")
        self.horizontalLayout_6.addWidget(self.main_btn)
        self.verticalLayout_6.addWidget(self.frame_main_btn)
        self.verticalLayout.addWidget(self.bg_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.list_assignments.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "PYLEARN"))
        self.btn_minimize.setToolTip(_translate("MainWindow", "Minimize"))
        self.btn_quit.setToolTip(_translate("MainWindow", "Close"))
        self.list_assignments.setSortingEnabled(False)
        self.main_btn.setText(_translate("MainWindow", "Main Button"))
