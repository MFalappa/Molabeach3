# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogEdit(object):
    def setupUi(self, DialogEdit):
        DialogEdit.setObjectName("DialogEdit")
        DialogEdit.resize(351, 292)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(DialogEdit)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(DialogEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.comboBox = QtWidgets.QComboBox(DialogEdit)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(DialogEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textBrowser_descr = QtWidgets.QTextBrowser(DialogEdit)
        self.textBrowser_descr.setObjectName("textBrowser_descr")
        self.verticalLayout.addWidget(self.textBrowser_descr)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_cancel = QtWidgets.QPushButton(DialogEdit)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_Edit = QtWidgets.QPushButton(DialogEdit)
        self.pushButton_Edit.setObjectName("pushButton_Edit")
        self.horizontalLayout.addWidget(self.pushButton_Edit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(DialogEdit)
        QtCore.QMetaObject.connectSlotsByName(DialogEdit)

    def retranslateUi(self, DialogEdit):
        _translate = QtCore.QCoreApplication.translate
        DialogEdit.setWindowTitle(_translate("DialogEdit", "Dialog"))
        self.label.setText(_translate("DialogEdit", "Choose importing function:"))
        self.label_2.setText(_translate("DialogEdit", "Importing function description:"))
        self.pushButton_cancel.setText(_translate("DialogEdit", "Cancel"))
        self.pushButton_Edit.setText(_translate("DialogEdit", "Edit..."))

