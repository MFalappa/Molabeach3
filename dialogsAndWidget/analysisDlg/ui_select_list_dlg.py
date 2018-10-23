# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_list_dlg.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(352, 423)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_select = QtGui.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_select.setFont(font)
        self.groupBox_select.setObjectName(_fromUtf8("groupBox_select"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_select)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.groupBox_select)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 302, 315))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkBox_select_all = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_select_all.setFont(font)
        self.checkBox_select_all.setChecked(True)
        self.checkBox_select_all.setObjectName(_fromUtf8("checkBox_select_all"))
        self.verticalLayout_4.addWidget(self.checkBox_select_all)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_close = QtGui.QPushButton(self.groupBox_select)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.pushButton_apply = QtGui.QPushButton(self.groupBox_select)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_apply.setFont(font)
        self.pushButton_apply.setObjectName(_fromUtf8("pushButton_apply"))
        self.horizontalLayout.addWidget(self.pushButton_apply)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addWidget(self.groupBox_select)
        self.groupBox_select.raise_()
        self.groupBox_select.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox_select.setTitle(_translate("Dialog", "Select Box", None))
        self.checkBox_select_all.setText(_translate("Dialog", "Select All", None))
        self.pushButton_close.setText(_translate("Dialog", "Close", None))
        self.pushButton_apply.setText(_translate("Dialog", "Apply", None))

