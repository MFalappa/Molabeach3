# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_path_dlg.ui'
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
        Dialog.resize(485, 258)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 12, 463, 226))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox_select = QtWidgets.QGroupBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_select.setFont(font)
        self.groupBox_select.setObjectName(_fromUtf8("groupBox_select"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_select)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_select)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 124, 177))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkBox_select_all = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_select_all.setFont(font)
        self.checkBox_select_all.setChecked(True)
        self.checkBox_select_all.setObjectName(_fromUtf8("checkBox_select_all"))
        self.verticalLayout_4.addWidget(self.checkBox_select_all)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_4.addWidget(self.groupBox_select)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_search = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_search.setObjectName(_fromUtf8("pushButton_search"))
        self.horizontalLayout_2.addWidget(self.pushButton_search)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lineEdit_search = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_search.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit_search.setObjectName(_fromUtf8("lineEdit_search"))
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_done = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_done.setObjectName(_fromUtf8("pushButton_done"))
        self.horizontalLayout.addWidget(self.pushButton_done)
        self.pushButton_apply = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_apply.setObjectName(_fromUtf8("pushButton_apply"))
        self.horizontalLayout.addWidget(self.pushButton_apply)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox_select.setTitle(_translate("Dialog", "Connected Box", None))
        self.checkBox_select_all.setText(_translate("Dialog", "Select All", None))
        self.label_2.setText(_translate("Dialog", "Change directory to save", None))
        self.pushButton_search.setText(_translate("Dialog", "Search", None))
        self.pushButton_done.setText(_translate("Dialog", "Done", None))
        self.pushButton_apply.setText(_translate("Dialog", "Apply", None))

