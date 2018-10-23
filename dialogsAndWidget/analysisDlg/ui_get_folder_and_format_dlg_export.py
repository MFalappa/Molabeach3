# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_folder_and_format_dlg_export.ui'
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

class Ui_Dialog_export(object):
    def setupUi(self, Dialog_export):
        Dialog_export.setObjectName(_fromUtf8("Dialog_export"))
        Dialog_export.resize(454, 219)
        self.horizontalLayout_6 = QtGui.QHBoxLayout(Dialog_export)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Dialog_export)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_delimiter = QtGui.QLabel(Dialog_export)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_delimiter.setFont(font)
        self.label_delimiter.setObjectName(_fromUtf8("label_delimiter"))
        self.horizontalLayout.addWidget(self.label_delimiter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboBox = QtGui.QComboBox(Dialog_export)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.comboBox_2 = QtGui.QComboBox(Dialog_export)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(Dialog_export)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lineEdit = QtGui.QLineEdit(Dialog_export)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.pushButton_browse = QtGui.QPushButton(Dialog_export)
        self.pushButton_browse.setObjectName(_fromUtf8("pushButton_browse"))
        self.horizontalLayout_4.addWidget(self.pushButton_browse)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.pushButton_Cancel = QtGui.QPushButton(Dialog_export)
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.horizontalLayout_5.addWidget(self.pushButton_Cancel)
        self.pushButton_ok = QtGui.QPushButton(Dialog_export)
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout_5.addWidget(self.pushButton_ok)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog_export)
        QtCore.QMetaObject.connectSlotsByName(Dialog_export)

    def retranslateUi(self, Dialog_export):
        Dialog_export.setWindowTitle(_translate("Dialog_export", "Export data...", None))
        self.label_2.setText(_translate("Dialog_export", "Select a file format:", None))
        self.label_delimiter.setText(_translate("Dialog_export", "Select a delimiter:", None))
        self.comboBox.setItemText(0, _translate("Dialog_export", ".csv", None))
        self.comboBox.setItemText(1, _translate("Dialog_export", ".txt", None))
        self.comboBox.setItemText(2, _translate("Dialog_export", ".xls", None))
        self.comboBox.setItemText(3, _translate("Dialog_export", ".phz", None))
        self.comboBox_2.setItemText(0, _translate("Dialog_export", "\\t", None))
        self.comboBox_2.setItemText(1, _translate("Dialog_export", " ", None))
        self.comboBox_2.setItemText(2, _translate("Dialog_export", ";", None))
        self.comboBox_2.setItemText(3, _translate("Dialog_export", ",", None))
        self.comboBox_2.setItemText(4, _translate("Dialog_export", ":", None))
        self.label.setText(_translate("Dialog_export", "Choose a folder:", None))
        self.pushButton_browse.setText(_translate("Dialog_export", "Browse...", None))
        self.pushButton_Cancel.setText(_translate("Dialog_export", "Cancel", None))
        self.pushButton_ok.setText(_translate("Dialog_export", "Ok", None))

