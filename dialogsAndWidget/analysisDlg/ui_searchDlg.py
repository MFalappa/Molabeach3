# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchDlg(object):
    def setupUi(self, SearchDlg):
        SearchDlg.setObjectName("SearchDlg")
        SearchDlg.resize(456, 386)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(SearchDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SearchDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.searchAnalisisLineEdit = QtWidgets.QLineEdit(SearchDlg)
        self.searchAnalisisLineEdit.setObjectName("searchAnalisisLineEdit")
        self.horizontalLayout.addWidget(self.searchAnalisisLineEdit)
        self.searchPushButton = QtWidgets.QPushButton(SearchDlg)
        self.searchPushButton.setObjectName("searchPushButton")
        self.horizontalLayout.addWidget(self.searchPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.analysisList = QtWidgets.QListWidget(SearchDlg)
        self.analysisList.setObjectName("analysisList")
        self.verticalLayout.addWidget(self.analysisList)
        self.comboBox_types = QtWidgets.QComboBox(SearchDlg)
        self.comboBox_types.setObjectName("comboBox_types")
        self.verticalLayout.addWidget(self.comboBox_types)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okPushButton = QtWidgets.QPushButton(SearchDlg)
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout_2.addWidget(self.okPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(SearchDlg)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout_2.addWidget(self.cancelPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.label.setBuddy(self.searchAnalisisLineEdit)

        self.retranslateUi(SearchDlg)
        self.okPushButton.clicked.connect(SearchDlg.accept)
        self.cancelPushButton.clicked.connect(SearchDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(SearchDlg)
        SearchDlg.setTabOrder(self.searchAnalisisLineEdit, self.searchPushButton)

    def retranslateUi(self, SearchDlg):
        _translate = QtCore.QCoreApplication.translate
        SearchDlg.setWindowTitle(_translate("SearchDlg", "Dialog"))
        self.label.setText(_translate("SearchDlg", "&Search Analysis:"))
        self.searchPushButton.setText(_translate("SearchDlg", "Search"))
        self.okPushButton.setText(_translate("SearchDlg", "Ok"))
        self.cancelPushButton.setText(_translate("SearchDlg", "Cancel"))

