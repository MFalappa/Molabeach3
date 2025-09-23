# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'read_prog_gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui,QtWidgets


def _fromUtf8(s):
    return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1011, 627)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox_select = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_select.setFont(font)
        self.groupBox_select.setObjectName(_fromUtf8("groupBox_select"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_select)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_select)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 139, 556))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.checkBox_select_all = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_select_all.setFont(font)
        self.checkBox_select_all.setObjectName(_fromUtf8("checkBox_select_all"))
        self.verticalLayout_5.addWidget(self.checkBox_select_all)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.horizontalLayout_3.addWidget(self.groupBox_select)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.textBrowser_row = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_row.setMinimumSize(QtCore.QSize(400, 0))
        self.textBrowser_row.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textBrowser_row.setObjectName(_fromUtf8("textBrowser_row"))
        self.verticalLayout_2.addWidget(self.textBrowser_row)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.textBrowser__transl = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser__transl.setMinimumSize(QtCore.QSize(400, 0))
        self.textBrowser__transl.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textBrowser__transl.setObjectName(_fromUtf8("textBrowser__transl"))
        self.verticalLayout.addWidget(self.textBrowser__transl)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_readprog = QtWidgets.QPushButton(Dialog)
        self.pushButton_readprog.setObjectName(_fromUtf8("pushButton_readprog"))
        self.horizontalLayout.addWidget(self.pushButton_readprog)
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox_select.setTitle(_translate("Dialog", "Select Box", None))
        self.checkBox_select_all.setText(_translate("Dialog", "Select all", None))
        self.label.setText(_translate("Dialog", "Row Messages:", None))
        self.label_2.setText(_translate("Dialog", "Translated Program:", None))
        self.pushButton_save.setText(_translate("Dialog", "Save", None))
        self.pushButton_readprog.setText(_translate("Dialog", "Read Prog", None))
        self.pushButton_close.setText(_translate("Dialog", "Close", None))

